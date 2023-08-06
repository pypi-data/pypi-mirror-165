############################################
# imports
############################################

import sys
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from turtle import color

import fgclustering.utils as utils
import fgclustering.statistics as stats


############################################
# functions
############################################

def _plot_global_feature_importance(p_value_of_features, save):
    '''Plot global feature importance based on p-values given as input.

    :param p_value_of_features: dictionary where keys are names of features and values are p-values of these features
    :type p_value_of_features: dict
    :param save: Filename to save plot.
    :type save: str
    '''
    importance = p_value_of_features.copy()
    importance.pop('target')
    importance.pop('cluster')
    importance = pd.DataFrame(importance, index=[0])
    importance = pd.melt(importance)
    importance.sort_values(by='value', ascending=True, inplace=True)
    importance.value = 1 - importance.value

    n_features = importance.shape[0]
    figure_size = max(6.5, int(np.ceil(5*n_features/25)))

    sns.set_theme(style='whitegrid')
    plt.figure(figsize=(6.5, figure_size))  # keep width default, change height depending on the number of features
    plot = sns.barplot(data=importance, x='value', y='variable', color='lightblue')
    plot.set_xlabel('importance')
    plot.set_ylabel('feature')
    plt.title('Global Feature Importance')
    plt.tight_layout()

    if save is not None:
        plt.savefig('{}_global_feature_importance.png'.format(save), bbox_inches='tight', dpi=300)
    plt.show()


def _plot_local_feature_importance(X, bootstraps, thr_pvalue, save, num_cols):
    '''Plot local feature importance to show the importance of each feature for each cluster.

    :param X: Feature matrix.
    :type X: pandas.DataFrame
    :param bootstraps: Number of bootstraps to be drawn for computation of p-value.
    :type bootstraps: int
    :param save: Filename to save plot.
    :type save: str
    :param num_cols: Number of plots in one row.
    :type num_cols: int
    '''
    importance = stats.get_feature_importance_clusterwise(X, bootstraps)

    X_barplot = pd.melt(importance, ignore_index=False)
    X_barplot = X_barplot.rename_axis('feature').reset_index(level=0, inplace=False)
    X_barplot = X_barplot.sort_values('value', ascending=False)

    n_features = importance.shape[0]
    figure_size = max(6.5, int(np.ceil(5*n_features/25)))
    num_cols = min(num_cols, len(importance.columns))

    sns.set_theme(style='whitegrid')
    plot = sns.FacetGrid(X_barplot, col='variable', sharey=False, col_wrap=num_cols, height=figure_size)
    plot.map(sns.barplot, 'value', 'feature', color='lightblue')
    plot.set_axis_labels('importance', 'feature')
    plot.set_titles(col_template="Cluster {col_name}")
    plt.suptitle('Feature Importance per Cluster')
    plt.tight_layout()

    if save is not None:
        plt.savefig('{}_local_feature_importance.png'.format(save), bbox_inches='tight', dpi=300)
    plt.show()


def _plot_heatmap(X, method, thr_pvalue, save):
    '''Plot feature heatmap sorted by clusters, where features are filtered and ranked
    with statistical tests (ANOVA for continuous featres, chi square for categorical features).

    :param X: Feature matrix.
    :type X: pandas.DataFrame
    :param method: Model type of Random Forest model: classifier or regression.
    :type method: str
    :param save: Filename to save plot.
    :type save: str
    '''
    X_scaled = utils.scale_minmax(X)
    X_heatmap = pd.DataFrame(columns=X_scaled.columns)

    target_values_original = X['target']
    target_values_scaled = X_scaled['target']

    one_percent_of_number_of_samples = int(np.ceil(0.01*len(X)))

    for cluster in X_scaled.cluster.unique():
        X_heatmap = pd.concat([X_heatmap, X_scaled[X_scaled.cluster == cluster]], ignore_index=True)
        X_heatmap = pd.concat([X_heatmap, pd.DataFrame(np.nan,
                                                       index=np.arange(one_percent_of_number_of_samples),
                                                       # blank lines which are 1% of num samples
                                                       columns=X_scaled.columns)], ignore_index=True)
    X_heatmap = X_heatmap[:-5]
    X_heatmap.drop('cluster', axis=1, inplace=True)

    n_samples, n_features = X_heatmap.shape
    heatmap_ = np.zeros((n_features, n_samples, 4))
    cmap_features = matplotlib.cm.get_cmap('coolwarm').copy()
    cmap_target = matplotlib.cm.get_cmap('viridis')  # gist_ncar

    for feature in range(n_features):
        for sample in range(n_samples):
            if feature == 0:
                heatmap_[feature, sample, :] = cmap_target(X_heatmap.iloc[sample, feature])
            else:
                heatmap_[feature, sample, :] = cmap_features(X_heatmap.iloc[sample, feature])

    figure_size = max(6.5, int(np.ceil(5*n_features/25)))

    sns.set_theme(style='white')
    fig = plt.figure(figsize=(figure_size, figure_size))
    img = plt.imshow(heatmap_, interpolation='none', aspect='auto')

    plt.suptitle('Subgroups of instances that follow similar decision paths in the RF model', fontsize=12)
    plt.title(f'Showing features with significance < {thr_pvalue}', fontsize=10, loc='left')
    plt.xticks([], [])
    plt.yticks(range(n_features), X_heatmap.columns)

    # remove bounding box
    for spine in plt.gca().spines.values():
        spine.set_visible(False)

    if method == "regression":
        norm = matplotlib.colors.Normalize(vmin=target_values_original.min(), vmax=target_values_original.max())
        cbar_target = plt.colorbar(matplotlib.cm.ScalarMappable(norm=norm, cmap=cmap_target))
        cbar_target.set_label('target')
    else:
        legend_elements = [Patch(facecolor=cmap_target(tv_n),
                                 edgecolor=cmap_target(tv_n),
                                 label=f'{tv_o}') for tv_n, tv_o in
                           zip(target_values_scaled.unique(), target_values_original.unique())]
        ll = plt.legend(handles=legend_elements,
                        bbox_to_anchor=(0, 0),
                        loc='upper left',
                        ncol=min(6, len(legend_elements)),
                        title="target")

    norm = matplotlib.colors.Normalize(vmin=0, vmax=1)
    cbar_features = plt.colorbar(matplotlib.cm.ScalarMappable(norm=norm, cmap=cmap_features))
    cbar_features.set_label('standardized feature values')

    if save is not None:
        plt.savefig('{}_heatmap.png'.format(save), bbox_inches='tight', dpi=300)
    plt.show()


def _plot_distributions(X, thr_pvalue, save, num_cols):
    '''Plot feature boxplots (for continuous features) or barplots (for categorical features) divided by clusters,
    where features are filtered and ranked with statistical tests (ANOVA for continuous features,
    chi square for categorical features).

    :param X: Feature matrix.
    :type X: pandas.DataFrame
    :param save: Filename to save plot.
    :type save: str
    :param num_cols: Number of plots in one row.
    :type num_cols: int
    '''
    X = X.copy()

    variables_to_plot = X.drop(['target', 'cluster'], axis=1, inplace=False).columns.to_list()
    # adding target, to plot it first
    variables_to_plot = ['target'] + variables_to_plot

    num_rows = int(np.ceil(len(variables_to_plot)/num_cols))
    plt.figure(figsize=(num_cols*4.5, num_rows*4.5))
    plt.tight_layout()
    plt.subplots_adjust(hspace=0.8, wspace=0.8)
    plt.suptitle(f'Distribution of feature values across subgroups with significance < {thr_pvalue}', fontsize=14)

    for n, feature in enumerate(variables_to_plot):
        # add a new subplot iteratively
        ax = plt.subplot(num_rows, num_cols, n + 1)
        if X[feature].nunique() < 5:
            sns.countplot(x='cluster', hue=feature, data=X, ax=ax,
                          palette=sns.color_palette("Blues_r", n_colors=len(np.unique(X[feature]))))
            ax.set_title("Feature: {}".format(feature))
            ax.legend(bbox_to_anchor=(1, 1), loc=2)
        else:
            sns.boxplot(x='cluster', y=feature, data=X, ax=ax, color='lightblue')
            ax.set_title("Feature: {}".format(feature))

    if save is not None:
        plt.savefig('{}_boxplots.png'.format(save), bbox_inches='tight', dpi=300)
    plt.show()
