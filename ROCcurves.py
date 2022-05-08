# -*- coding: utf-8 -*-
"""
TM2.4 SIRS versus Sepsis ICKG
Author: Marit Verboom
Date: 02/2022 - 05/2022
"""

import numpy as np
from sklearn import metrics
import matplotlib.pyplot as plt

def ROC_all(estimator, test, test_label, tprs, aucs, fig, ax, title):
    """
    Function to plot the ROC curve per fold in the 5-fold crossvalidation.
    https://scikit-learn.org/stable/modules/generated/sklearn.metrics.plot_roc_curve.html

    Returns
    -------
    tprs : True positive rates
    aucs : AUC per fold

    """
    mean_fpr = np.linspace(0, 1, 100)
    
    # plot ROC curve per fold
    visual = metrics.plot_roc_curve(estimator, test, test_label,
                                 name='(ROC)',
                                 alpha=0.5, lw=1, ax=ax)
    ax.set(title=title)
    interp_tpr = np.interp(mean_fpr, visual.fpr, visual.tpr)
    interp_tpr[0] = 0.0
    tprs.append(interp_tpr)
    aucs.append(visual.roc_auc)
    return tprs, aucs



def ROC_mean(tprs, aucs, title):
    """
    Function to plot the mean ROC curve of all folds
    https://scikit-learn.org/stable/modules/generated/sklearn.metrics.plot_roc_curve.html

    """
    mean_fpr = np.linspace(0, 1, 100)

    fig, ax = plt.subplots()
      
    mean_tpr = np.mean(tprs, axis=0)
    mean_tpr[-1] = 1.0
    mean_auc = metrics.auc(mean_fpr, mean_tpr)
    std_auc = np.std(aucs)
    ax.plot(mean_fpr, mean_tpr, color='salmon',
            label=r'Mean ROC (AUC = %0.2f $\pm$ %0.2f)' % (mean_auc, std_auc),
            lw=2, alpha=1)
    ax.set_xlabel('1 - specificity')    
    ax.set_ylabel('sensitivity')

    ax.plot([0, 1], [0, 1], linestyle='--', lw=2, color='grey',
            label='Chance', alpha=.8)

    std_tpr = np.std(tprs, axis=0)
    tprs_upper = np.minimum(mean_tpr + std_tpr, 1)
    tprs_lower = np.maximum(mean_tpr - std_tpr, 0)
    ax.fill_between(mean_fpr, tprs_lower, tprs_upper, color='salmon', alpha=.2,
                label=r'$\pm$ 1 std. dev.')

    ax.set(xlim=[-0.05, 1.05], ylim=[-0.05, 1.05],
       title='Receiver operating characteristic ')
    ax.legend(loc="lower right")
    
    plt.show()
    return 