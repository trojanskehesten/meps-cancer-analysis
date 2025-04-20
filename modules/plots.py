# Custom plots functions for Notebooks
from pltstat import cm
import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
from scipy.stats import mannwhitneyu
from matplotlib.patches import Rectangle


def pairwise_mw(df, features, key_value, cont_feat):
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
    
    mask = p_matrix.fillna(1)>0.05
    diff_matrix = diff_matrix.mask(mask)
    
    cmap, cbar_kws = cm.get_pval_legend_thr_cmap()
    fig, ax = plt.subplots(1, 2, figsize=(18, 6))
    
    sns.heatmap(p_matrix, cmap=cmap, cbar_kws=cbar_kws, annot=True, fmt='.2f', ax=ax[0]);
    sns.heatmap(diff_matrix, annot=True, center=0, cmap='vlag', fmt='.0f', ax=ax[1])
    
    return ax


def add_titles_mw_pairwise_age(ax):
    # Add titles:
    ax[0].set_title("Mann–Whitney U Test: p-values for Age Comparison Between Cancer Types")
    ax[1].set_title("Pairwise Median Age Differences Between Cancer Types");


def add_legend_mw_pairwise_age(ax):
    # Custom legend:
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
    add_titles_mw_pairwise_age(ax)
    add_legend_mw_pairwise_age(ax)
