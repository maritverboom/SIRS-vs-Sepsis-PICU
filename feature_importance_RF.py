# -*- coding: utf-8 -*-
"""
TM2.4 SIRS versus Sepsis ICKG
Author: Marit Verboom
Date: 02/2022 - 05/2022
"""

import pandas as pd

def feature_importance_RF(randomf, feature_names):
    """
    Function to calculate a score representing the importance of features used
    in the Random Forest classifier
    
    Parameters
    ----------
    randomf : Random Forest model.
    feature_names : DataFrame containing all feature names

    Returns
    -------
    mean_coef : DataFrame containing mean score of all trees of RF classifier

    """
    feature_names = feature_names.sort_index()
    feature_names = feature_names.reset_index(drop=True)  
    dict_sign = dict()
    
    # number of trees used in the Random Forest estimator
    n_trees = len(randomf.estimators_)    
    
    # for every tree in the RF classifier
    for clf in randomf.estimators_:           
        
        # Parameters of RF classifier
        # For explanation see: https://scikit-learn.org/stable/auto_examples/tree/plot_unveil_tree_structure.html
        n_nodes = clf.tree_.node_count
        children_left = clf.tree_.children_left
        children_right = clf.tree_.children_right
        feature = clf.tree_.feature
        threshold = clf.tree_.threshold
        value = clf.tree_.value
        
        # for every node
        for i in range(n_nodes):   
            # if threshold = (-)2, the node is a resulting leaf
            if abs(threshold[i]) != 2:      
                classes_left = value[children_left[i]]
                classes_right = value[children_right[i]]
                
                # is left node SIRS node?
                if classes_left[0][1] > 0 and classes_right[0][1] > 0: 
                    # Left and right node are mixed leaves, containing both 0 and 1 labels 
                    # is_SIRS is True if: ratio SIRS/sepsis is higher in left node than in right node    
                    is_SIRS = classes_left[0][0]/classes_left[0][1] > classes_right[0][0]/classes_right[0][1]
                elif classes_left[0][1] == 0 and classes_right[0][1] > 0:
                    # left node =  SIRS
                    is_SIRS = True
                elif classes_left[0][1] > 0 and classes_right[0][1] == 0:
                    # right node =  SIRS
                    is_SIRS = False
      
                
                # Weight of feature based on the remaining patients in the smallest childnode 
                weight = min([classes_left[0][0]+classes_left[0][1], classes_right[0][0]+classes_right[0][1]])
                if is_SIRS:
                    # lower values (left node) of the feature are linked to class SIRS (0)
                    coef = weight
                else:
                    # higher value (right node)  of the feature is linked to class sepsis (1)
                    coef = -1*weight
                    
                # Feature importance per feature
                key = feature_names[feature[i]]
                try: 
                    feature_list = dict_sign[key]
                except KeyError:
                    feature_list = []
                feature_list.append(coef)
                dict_sign[key] = feature_list
    
    # mean feature importance of all trees
    mean_sign = dict()
    for feature in dict_sign:
        mean_sign[feature] = sum(dict_sign[feature])/n_trees
    
    mean_coef = pd.DataFrame.from_dict(mean_sign, orient='index', columns=['Scores'])
    mean_coef['Specs'] = mean_coef.index
    
    return mean_coef