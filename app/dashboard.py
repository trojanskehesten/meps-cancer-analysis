import streamlit as st
import sys
import os
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "modules")))

import plots
import variables as v

st.set_page_config(layout="wide")
st.title('MEPS Cancer Analysis Dashboard')
st.markdown('')

# To run it: `streamlit run app/dashboard.py`
# @st.cache(persist=True)
@st.cache_data
def load_data():
    # Load data:
    df = pd.read_stata(os.path.join(os.path.dirname(__file__), os.pardir, "data", "h216.dta"))

    # Change categorical columns to object type:
    df_cat = df.select_dtypes('category')
    df[df_cat.columns] = df_cat.astype('object')

    # Drop inapplicable answers:
    df = df.loc[~df[v.cancer_feat].isin(v.vals_to_drop), :]

    # Replace answers:
    df[v.cancer_feat] = df[v.cancer_feat].replace({'1 YES': v.yes_ans, '2 NO': v.no_ans})

    # Number of cancer types per patient:
    df[v.cancer_bool_types] = df.loc[:, v.cancer_types] == '1 YES'
    df[v.cancer_mult] = df.loc[:, v.cancer_bool_types].sum(axis=1)
    df[v.mult_col] = df[v.cancer_mult] > 1
    df[v.mult_col] = df[v.mult_col].replace({False: v.no_ans, True: v.yes_ans})
    df[v.cancer_feat_type] = df.loc[:, v.cancer_feat]

    cancer_type_names = np.append(v.cancer_type_names, v.mult_col)
    for bool_type, type_name in zip(v.cancer_bool_types, cancer_type_names):
        df.loc[df[bool_type], v.cancer_feat_type] = f'1. {type_name}'

    df.loc[df.loc[:, v.cancer_mult] > 1, v.cancer_feat_type] = v.mult_ans

    df[v.cancer_feat_type] = df[v.cancer_feat_type].replace({'2 NO': v.no_ans})

    # Add DK or Refused category:
    df[v.cancer_feat_type] = df[v.cancer_feat_type].replace({v.yes_ans: v.dk_refused_ans})

    # Replace invalid or missing values in cancer_type columns with None for proper data handling:
    df[v.cancer_types] = df[v.cancer_types].replace({'-8 DK': None, '-7 REFUSED': None})

    # Inapplicable when CANCERDX is No
    df[v.cancer_types] = df[v.cancer_types].replace({'2 NO': v.no_ans, '-1 INAPPLICABLE': v.no_ans})
    df[v.cancer_types] = df[v.cancer_types].replace({'1 YES': v.yes_ans})

    # Rename the columns to readable names:
    df[cancer_type_names[:-1]] = df[v.cancer_types]  # -1 - to exclude Multiple
    df = df.drop(columns=v.cancer_types)

    # Race values correction:
    df[v.race_col] = df[v.race_col].str.replace(r' - NO OTHER RACE REPORTED$', '', regex=True)
    df[v.race_col] = df[v.race_col].str.replace(r'-NO OTH$', '', regex=True)
    df[v.race_col] = df[v.race_col].str.replace(r'-NO OTHER RACE$', '', regex=True)
    df[v.race_col] = df[v.race_col].replace(
        {
            "3 AMER INDIAN/ALASKA NATIVE": "3 INDIAN/\nALASKA",
            "4 ASIAN/NATV HAWAIIAN/PACFC ISL": "4 ASIAN/\nHAWAIIAN",
            "6 MULTIPLE RACES REPORTED": "6 MULTIPLE",
        }
    )

    return df

df = load_data()

choice = st.radio(
    "Demographic feature",
    ["Age", "Sex", "Race"],
    index=0,
    horizontal=True,
    label_visibility="collapsed",
)
height = 400
dem_feat = {"Age": v.age_col, "Sex": v.sex_col, "Race": v.race_col}[choice]
# 1. Distributions of demographic features

if choice == 'Age':
    fig_dist = px.histogram(df, x=v.age_col, title='Age')
    fig_dist.update_traces(textfont_size=20, textposition="inside",
                          texttemplate="%{y:.0f}")
    fig_dist.update_traces(
        xbins=dict(
            start=df[v.age_col].min(),
            end=df[v.age_col].max() + 1,
            size=2,
        )
    )
    fig_dist.update_layout(height=height)
    st.plotly_chart(fig_dist, use_container_width=True)
# 1.2-3. Sex and Race
else:
    fig_dist = plots.pie(df, dem_feat, return_fig=True, title=choice)
    fig_dist.update_layout(height=height, showlegend=False)  #, width=300, autosize=False)
    st.plotly_chart(fig_dist, use_container_width=True)

# 2. Cancer dependency
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
    st.text(str(exclude_no))

cancer_feat = {"Cancer diagnosis": v.cancer_feat, "Cancer types": v.cancer_feat_type}[cancer_choice]

if exclude_no:
    df_sub = df[df[v.cancer_feat_type] != v.no_ans]
else:
    df_sub = df
if choice == 'Age':
    if cancer_choice == cancer_options[0]:
        category_orders = np.sort(list(v.cancer_colors.keys()))
        color_discrete_map = v.cancer_colors
    else:
        category_orders = v.cancer_type_order
        color_discrete_map = v.cancer_type_colors

    fig = px.box(
        df_sub,
        x=dem_feat,
        y=cancer_feat,
        orientation="h",
        color=cancer_feat,
        category_orders={cancer_feat: category_orders},
        color_discrete_map=color_discrete_map,
        points=False,
    )

    fig.update_layout(showlegend=False)

else:
    feat1, feat2 = cancer_feat, dem_feat

    ct_abs = pd.crosstab(df_sub[feat1], df_sub[feat2])
    counts = ct_abs.to_numpy()[..., None]
    ct_h = pd.crosstab(df_sub[feat1], df_sub[feat2], normalize="index")
    ct_v = pd.crosstab(df_sub[feat1], df_sub[feat2], normalize="columns")

    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=("Row-normalized (horizontal)", "Column-normalized (vertical)"),
        horizontal_spacing=0.08
    )

    z_text_h = (ct_h.values * 100)
    z_text_v = (ct_v.values * 100)

    fig.add_trace(
        go.Heatmap(
            z=ct_h.values,
            x=ct_h.columns.astype(str),
            y=ct_h.index.astype(str),
            text=np.round(z_text_h, 1).astype(str) + "%",
            texttemplate="%{text}",
            customdata=counts,
            hovertemplate="%{y} / %{x}<br>%{customdata[0]} patients (%{z:.2%})<extra></extra>",
            # hovertemplate="feat1=%{y}<br>feat2=%{x}<br>percent=%{z:.2%}<br>count=%{customdata}<extra></extra>",
            zmin=0, zmax=1,
            colorbar=dict(title="Share (row)")
        ),
        row=1, col=1
    )

    fig.add_trace(
        go.Heatmap(
            z=ct_v.values,
            x=ct_v.columns.astype(str),
            y=ct_v.index.astype(str),
            text=np.round(z_text_v, 1).astype(str) + "%",
            texttemplate="%{text}",
            customdata=counts,
            hovertemplate="%{y} / %{x}<br>%{customdata[0]} patients (%{z:.2%})<extra></extra>",
            zmin=0, zmax=1,
            colorbar=dict(title="Share (col)")
        ),
        row=1, col=2
    )

    fig.update_yaxes(visible=False, row=1, col=2, autorange="reversed")
    # fig.update_yaxes(showticklabels=False, row=1, col=2)

st.plotly_chart(fig, use_container_width=True)

# 3. Filters
col1, col2 = st.columns(2)
cancer_types = df[v.cancer_feat_type].unique()
cancer_types = np.concatenate((cancer_types, ['1. ANY', v.no_filter]))
dem_types = df[dem_feat].unique()
dem_types = np.append(dem_types, v.no_filter)

with col1:
    cancer_option = st.selectbox(
        "Cancer type",
        cancer_types,
        index=0,  # какая выбрана по умолчанию
    )
with col2:
    dem_option = st.selectbox(
        choice,
        dem_types,
        index=0,  # какая выбрана по умолчанию
    )

if cancer_option == v.no_filter:
    cols = st.columns(3)
    # Distribution of cancer:

    with (cols[0]):
        yes_no_counts = df[v.cancer_feat].value_counts()
        yes_no_prop =  df[v.cancer_feat].value_counts(normalize=True)
        yes_no_prop = (yes_no_prop * 100).round(1)
        title = 'Cancer types<br>'
        title += f'No: {yes_no_counts.loc[v.no_ans]} ({yes_no_prop.loc[v.no_ans]} %) /<br>'
        title += f'Yes: {yes_no_counts.loc[v.yes_ans]} ({yes_no_prop.loc[v.yes_ans]} %)'
        fig_cancer = plots.pie(df[df[v.cancer_feat_type] != v.no_ans], v.cancer_feat_type, title, v.cancer_type_colors,
                  v.cancer_type_order, return_fig=True)
        fig_cancer.update_layout(height=height, showlegend=False)
        st.plotly_chart(fig_cancer, use_container_width=True)
else:
    cols = st.columns(2)
