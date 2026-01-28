# Custom plots functions for Notebooks
from pltstat import cm
import pandas as pd
import numpy as np
import pingouin as pg
import seaborn as sns
from matplotlib import pyplot as plt

from scipy.stats import mannwhitneyu
from matplotlib.patches import Rectangle
from matplotlib.colors import ListedColormap, BoundaryNorm, LinearSegmentedColormap
from matplotlib.ticker import FormatStrFormatter
import plotly.express as px
import plotly.io as pio
pio.renderers.default = "notebook"  # or "iframe", "svg", ""notebook_connected


def pairwise_mw(df, features, key_value, cont_feat, alpha=0.05):
    # Create empty matrix for p-value
    p_matrix = pd.DataFrame(index=features, columns=features, dtype=float)
    diff_matrix = pd.DataFrame(index=features, columns=features, dtype=float)
    
    # Run through all pairs of columns
    for i in features:
        for j in features:
            if i == j:
                p_matrix.loc[i, j] = np.nan
                diff_matrix.loc[i, j] = 0
                continue
            
            # Choose only cases where both features are not missing
            subset = df[[i, j, cont_feat]].dropna()
            
            # Group by Yes/No → 1/0
            group1 = subset.loc[subset[i] == key_value, cont_feat]
            group2 = subset.loc[subset[j] == key_value, cont_feat]
            
            # If subset is small → skip it
            if len(group1) < 10 or len(group2) < 10:
                p_matrix.loc[i, j] = np.nan
                diff_matrix.loc[i, j] = np.nan
                continue

            # Mann–Whitney U test
            stat, p = mannwhitneyu(group1, group2, alternative='two-sided')
            p_matrix.loc[i, j] = p
            diff_matrix.loc[i, j] = group2.median() - group1.median()
    
    mask = p_matrix.fillna(1)>alpha
    diff_matrix = diff_matrix.mask(mask)
    
    # cmap, cbar_kws = cm.get_pval_legend_thr_cmap(alpha=alpha)

    bounds = [0., alpha, 1.]
    cmap = ListedColormap(["green", "lightgray"])
    norm = BoundaryNorm(bounds, cmap.N)
    # cbar_kws = {'ticks': [0.0, alpha, 1.0]}

    fig, ax = plt.subplots(1, 2, figsize=(24, 6))
    hm0 = sns.heatmap(p_matrix, vmin=0, vmax=1, cmap=cmap, norm=norm, annot=True, fmt='.4f', cbar=False, ax=ax[0])  # cbar_kws=cbar_kws
    sns.heatmap(diff_matrix, annot=True, center=0, cmap='vlag', fmt='.0f', ax=ax[1])
    cbar = fig.colorbar(
        hm0.collections[0],
        ax=ax[0],
        spacing='proportional',
        ticks=[0, alpha, 1]
    )
    cbar.set_ticks(bounds)
    cbar.ax.yaxis.set_major_formatter(FormatStrFormatter('%.4f'))
    
    return ax


def _add_titles_mw_pairwise_age(ax):
    """Add titles"""
    ax[0].set_title("Mann–Whitney U Test: p-values for Age Comparison Between Cancer Types")
    ax[1].set_title("Pairwise Median Age Differences Between Cancer Types");


def _add_legend_mw_pairwise_age(ax):
    """Custom legend"""
    warm_patch = Rectangle((0, 0), 1, 1, facecolor='#f4a582', edgecolor='black', label='Row < Column (older)')
    cool_patch = Rectangle((0, 0), 1, 1, facecolor='#92c5de', edgecolor='black', label='Row > Column (younger)')
    neutral_patch = Rectangle((0, 0), 1, 1, facecolor='white', edgecolor='black', linewidth=1.5, label='Not significant or N<10')
    
    ax[1].legend(handles=[warm_patch, cool_patch, neutral_patch], 
                 title='Δ Median Age (Column-Row)', 
                 loc='upper center', 
                 bbox_to_anchor=(0.5, -0.3), 
                 ncol=3, 
                 frameon=True
    );


def customize_mw_pairwise_age(ax):
    """Add titles and legend to the plot"""
    _add_titles_mw_pairwise_age(ax)
    _add_legend_mw_pairwise_age(ax)


def pie(df, feat, title=None, colors=None, order=None, return_fig=False):
    """Plot a pie chart for a categorical column with counts and percentages."""
    if title is None:
        title = feat

    category_orders = {feat: order} if order is not None else None

    fig = px.pie(
        df,
        names=feat,
        color=feat,
        title=title,
        color_discrete_map=colors,
        category_orders=category_orders,
    )

    fig.update_traces(
        textinfo='label+percent+value',
        texttemplate='%{label}<br>%{percent:.1%}<br>(%{value})',
        hovertemplate='%{label}: <b>%{value}</b> (%{percent:.1%})'
    )
    fig.show()

    if return_fig is True:
        return fig


def plot_posthoc_heatmap(df, dv, between, alpha=0.05, multiple_comparison=True, figsize=(10, 8), **kwargs):
    """
    Perform pairwise post-hoc tests using Pingouin and plot a heatmap of corrected p-values.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe.
    dv : str
        Dependent variable column.
    between : str
        Between-groups factor column.
    alpha : float
        Significance threshold.
    multiple_comparison : bool
        If True, use corrected p-values ('p-corr'). If False, use uncorrected p-values ('p-unc').
    figsize : tuple of two ints, optional
        Figure size in inches (width, height) for the heatmap plot. Default is (10, 8).
    **kwargs : dict
        Additional arguments passed to pg.pairwise_tests.

    Returns
    -------
    pivot_table : pd.DataFrame
        Symmetric pivot table of corrected p-values.
    """
    p_val_col = {False: 'p-unc', True: 'p-corr'}[multiple_comparison]
    # Run pairwise posthoc
    posthoc = pg.pairwise_tests(data=df, dv=dv, between=between, **kwargs)

    # Create symmetric table
    posthoc_dbl = pd.concat([posthoc, posthoc.rename(columns={'A': 'B', 'B': 'A'})], ignore_index=True)

    # Pivot table to matrix form
    pivot_table = posthoc_dbl[['A', 'B', p_val_col]].pivot(index='A', columns='B', values=p_val_col)

    # Heatmap color mapping
    sign_col = "green"
    insign_col = "lightgray"
    cmap = [
        (0, sign_col),
        (alpha, sign_col),
        (alpha, insign_col),
        (1, insign_col),
    ]
    cmap = LinearSegmentedColormap.from_list("custom", cmap)
    label = {False: 'Uncorrected p-value', True: 'Corrected p-value'}[multiple_comparison]

    plt.figure(figsize=figsize)
    sns.heatmap(
        pivot_table,
        annot=True,
        fmt=".3f",
        cmap=cmap,
        linewidths=0.5,
        cbar_kws={'ticks': [0.0, alpha, 1.0], 'label': label},
    )
    plt.title(f'Heatmap of Posthoc Corrected p-values ({dv})')
    plt.show()

    return pivot_table
