# -*- coding: utf-8 -*-
"""
TM2.4 SIRS versus Sepsis ICKG
Author: Marit Verboom
Date: 02/2022 - 05/2022
"""

import pandas as pd 
import matplotlib.pyplot as plt


def bar_plots(important_features, title=''):
    """Create barplots with the most important features"""
    
    # Calculate mean of the feature importances per fold 
    important_features = important_features.fillna(0)
    importance_mean = important_features.mean(axis=1)
    important_features = pd.concat([important_features,importance_mean],axis=1)
    important_features.columns = ['Specs','Scores1','Scores2','Scores3','Scores4','Scores5','Mean'] 
    important_features = important_features.sort_values('Mean', ascending=False)
    
    # score should be higher than thresh to be plotted
    thresh = 0.1

    important_plot_pos = important_features[important_features['Mean'] > thresh]
    ax = important_plot_pos.plot.barh(x ='Specs', y='Mean', color='salmon', legend=None)
    ax.invert_yaxis()
    ax.set(xlabel = 'Feature importance score', ylabel = '')
    ax.set_title('Feature importances "Sepsis"'+ title, fontdict={'fontsize':12}, pad=12)
    plt.tight_layout()
    plt.show()
    
    important_plot_neg = important_features[important_features['Mean'] < -thresh]
    ax = important_plot_neg.plot.barh(x='Specs', y='Mean', color='salmon', legend=None)
    ax.set(xlabel = 'Feature importance score', ylabel = '')
    ax.set_title('Feature importances "SIRS"'+ title, fontdict={'fontsize':12}, pad=12)
    plt.tight_layout()
    plt.show()
    
    return important_features, important_plot_pos