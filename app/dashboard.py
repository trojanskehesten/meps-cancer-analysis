# To run it from root directory: `streamlit run app/dashboard.py`

import streamlit as st
import sys
import os
import numpy as np

import utils as u

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "modules")))

import plots
import variables as v

st.set_page_config(layout="wide")
st.title('MEPS Cancer Analysis Dashboard')
st.markdown('')

# 0. Load data and initial values
df = u.load_data()

# -------
# Block 1
# -------
# 1. Distributions of demographic features
# 1.1 Radio choice

dem_choices = [v.dash_age_feat, v.dash_sex_feat, v.dash_race_feat]
dem_feats = [v.age_col, v.sex_col, v.race_col]

st.subheader("Demographic feature distribution")
dem_choice = st.radio(
    "Demographic feature",
    dem_choices,
    index=0,
    horizontal=True,
    label_visibility="collapsed",
)

dem_feat = dict(zip(dem_choices, dem_feats))[dem_choice]  # {"Age": v.age_col, "Sex": v.sex_col, "Race": v.race_col}

# 1.2.1. Age:
if dem_choice == v.dash_age_feat:
    u.plot_hist_age(df, height=v.dash_plot_height)

# 1.2.2-3. Sex and Race
else:
    u.plot_pie(df=df, x=dem_feat, title=dem_choice, height=v.dash_plot_height)

# -------
# Block 2
# -------
# 2. Cancer dependency
@st.fragment
def block2():
    """Display cancer dependency analysis with demographic features."""
    st.subheader("Cancer dependency")
    # 2.1. Radio buttons area:
    col1, col2 = st.columns(2)
    cancer_options = ["Cancer diagnosis", "Cancer types"]
    with col1:
        cancer_choice = st.radio(
            "Cancer feature",
            cancer_options,
            index=0,
            horizontal=True,
            label_visibility="collapsed",
        )

    exclude_no = False
    if cancer_choice == cancer_options[1]:
        with col2:
            col21, col22 = st.columns([1, 2])
            with col21:
                st.write("Exclude No answer:")
            with col22:
                exclude_no_options = ['Include', 'Exclude']
                exclude_no = st.radio("Exclude No answer", exclude_no_options, horizontal=True, label_visibility="collapsed")
                exclude_no = dict(zip(exclude_no_options, [False, True]))[exclude_no]

    cancer_feat = {"Cancer diagnosis": v.cancer_feat, "Cancer types": v.cancer_feat_type}[cancer_choice]

    # 2.1.1 Exclude No Cancer cases:
    if exclude_no:
        df_sub = df[df[v.cancer_feat_type] != v.no_ans]
    else:
        df_sub = df

    # 2.2. Plot area:
    if dem_choice == v.dash_age_feat:
        if cancer_choice == cancer_options[0]:
            category_orders = np.sort(list(v.cancer_colors.keys()))
            color_discrete_map = v.cancer_colors
        else:
            category_orders = v.cancer_type_order
            color_discrete_map = v.cancer_type_colors

        fig = u.boxplot(df_sub, cancer_feat, dem_feat, category_orders, color_discrete_map)

    else:
        fig = u.crosstab_plot(df_sub, cancer_feat, dem_feat)

    st.plotly_chart(fig, use_container_width=True)

    # 2.3. Conclusion:
    if cancer_feat == v.cancer_feat:
        conclusion2 = v.concl_diag[dem_choice]
    else:
        conclusion2 = v.consl_types[dem_choice]
    u.expander_conclusion(conclusion=conclusion2)

# -------
# Block 3
# -------
# 3. Filters
@st.fragment
def block3(dem_feat):
    """Display filtered demographic distributions based on user selections."""
    st.subheader("Other demographic features dependency")

    # Get non-chosen features:
    other_mask = np.array(dem_feats) != dem_feat
    other_dem_feats = np.array(dem_feats)[other_mask]
    other_dem_feats_types = np.array(v.dash_dem_feats_types)[other_mask]

    # 3.0. If choice is Age, let's create categories (18-39, 40-64, 65-85):
    if dem_feat == v.age_col:
        dem_feat = v.age_col_cat

    # 3.1. Create filters:
    col1, col2 = st.columns(2)
    cancer_types = df[v.cancer_feat_type].unique()
    cancer_types = np.sort(cancer_types)
    dem_types = df[dem_feat].unique()
    dem_types = np.sort(dem_types)

    # 3.2. Selection area:
    with col1:
        cancer_options = st.multiselect(
            "Cancer type(s)",
            cancer_types,
        )

    with col2:
        dem_options = st.multiselect(
            dem_choice,
            dem_types,
        )

    # 3.3. Get subset with chosen filters:
    df_sub = df.copy()
    if len(cancer_options) != 0:
        df_sub = df_sub[df_sub[v.cancer_feat_type].isin(cancer_options)]
    if len(dem_options) != 0:
        df_sub = df_sub[df_sub[dem_feat].isin(dem_options)]

    # 3.4. Plots area:
    st.metric(
        "Number of persons:",
        len(df_sub),
        delta=f"{len(df_sub) / len(df) * 100:.1f}% of all data",
    )

    if len(df_sub) == 0:
        st.warning('No data for selected filters.')
        st.info("Try changing the filter settings.")
        return

    # Create structure with plots:
    # Create cancer plot if cancer option was not chosen:
    if len(cancer_options) == 0:
        cols = st.columns(3)
        col_i_start = 1
        # Distribution of cancer:

        with cols[0]:
            yes_no_counts = df_sub[v.cancer_feat].value_counts()
            yes_no_prop =  df_sub[v.cancer_feat].value_counts(normalize=True)
            yes_no_prop = (yes_no_prop * 100).round(1)
            title = 'Cancer types<br>'
            title += f'No: {yes_no_counts.loc[v.no_ans]} ({yes_no_prop.loc[v.no_ans]} %) /<br>'
            title += f'Yes: {yes_no_counts.loc[v.yes_ans]} ({yes_no_prop.loc[v.yes_ans]} %)'
            fig_cancer = plots.pie(df_sub[df_sub[v.cancer_feat_type] != v.no_ans], v.cancer_feat_type, title, v.cancer_type_colors,
                      v.cancer_type_order, show_fig=False, return_fig=True)
            fig_cancer.update_layout(height=v.dash_plot_height, showlegend=False)
            st.plotly_chart(fig_cancer, use_container_width=True)
    else:
        cols = st.columns(2)
        col_i_start = 0

    # Plot other non_chosen two demographic features distributions:
    for i in range(2):
        with cols[i+col_i_start]:
            if other_dem_feats_types[i] == 'cont':
                u.plot_hist_age(df=df_sub, x=v.age_col, title=v.dash_age_feat, height=v.dash_plot_height)
            elif other_dem_feats_types[i] == 'cat':
                u.plot_pie(df=df_sub, x=other_dem_feats[i], title=None)


block2()

block3(dem_feat)   # Explicit parameter to avoid shadowing
