import os
import sys
import streamlit as st
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
import numpy as np
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "modules")))

import plots
import variables as v


# @st.cache(persist=True)
@st.cache_data
def load_data():
    # Load data:
    cols = [v.cancer_feat, v.age_col, v.sex_col, v.race_col]
    cols = np.concatenate((cols, v.cancer_types))
    df = pd.read_stata(os.path.join(os.path.dirname(__file__), os.pardir, "data", "h216.dta"), columns=cols)

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
    # For Age choice, let's create categories (18-39, 40-64, 65-85):
    age_bins = [17, 39, 64, 86]
    age_labels = ["1. Young adults (18-39)", "2. Middle-aged (40-64)", "3. Older adults (65-85)"]
    dem_feat = v.age_col_cat
    df[dem_feat] = pd.cut(
        df[v.age_col],
        bins=age_bins,
        labels=age_labels,
        include_lowest=True
    )

    return df


def plot_hist_age(df, x=v.age_col, title='Age', height=400):
    """Plot age histogram"""
    fig_dist = px.histogram(df, x=x, title=title)
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


def plot_pie(df, x, title=None, height=400, **kwargs):
    if title is None:
        title = x
    fig_dist = plots.pie(df, x, return_fig=True, title=title, **kwargs)
    fig_dist.update_layout(height=height, showlegend=False)  # , width=300, autosize=False)
    st.plotly_chart(fig_dist, use_container_width=True)


def expander_conclusion(conclusion, title="Conclusion"):
    """Print expander with conclusion"""
    with st.expander(title):
        st.write(conclusion)

def boxplot(df, cat_feat, cont_feat, category_orders, color_discrete_map):
    """"""
    fig = px.box(
        df,
        x=cont_feat,
        y=cat_feat,
        orientation="h",
        color=cat_feat,
        category_orders={cat_feat: category_orders},
        color_discrete_map=color_discrete_map,
        points=False,
    )

    fig.update_layout(showlegend=False)

    return fig


def crosstab_plot(df, feat1, feat2):

    ct_abs = pd.crosstab(df[feat1], df[feat2])
    counts = ct_abs.to_numpy()[..., None]
    ct_h = pd.crosstab(df[feat1], df[feat2], normalize="index")
    ct_v = pd.crosstab(df[feat1], df[feat2], normalize="columns")

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

    return fig
