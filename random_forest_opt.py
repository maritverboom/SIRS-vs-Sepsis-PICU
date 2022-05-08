"""
TM2.4 SIRS versus Sepsis
Author: Marit Verboom
Date: 02/2022 - 05/22
"""

# Import modules
from sklearn.model_selection import RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix

# Created functions
from feature_importance_RF import feature_importance_RF

def random_forest_opt(data_train, data_test, labels_train, labels_test, features):
    """
    Function for the basic optimalization of the Random Forest model. 

    Parameters
    ----------
    data_train :  DataFrame containing parameters of trainset
    data_test : DataFrame containing parameters of testset
    labels_train : DataFrame containing labels of trainset
    labels_test : DataFrame containing labels of testset
    features : DataFrame containing  featurenames

    Returns
    -------
    randomf : optimalised Random Forest classifier
    score_test : accuracy of RF classifier
    sens_test : sensitivity of RF classifier
    spec_test : specificity of RF classifier
    features : DataFrame containing parameters and their importance

    """
    features = features.sort_index()
    features = features.reset_index(drop=True)  
    
   
    # Define hyperparameters for RF
    # Multiple parameters can be optimized, see 
    # https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html
    forest_parameters = {'n_estimators': list(range(100,300))}
        
    # Perform Randomized Search with CV for hyperparameter optimalisation
    # min_samples_leaf set at 2 so at least 2 patients per endpoint remain
    #https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.RandomizedSearchCV.html 
    opti = RandomizedSearchCV(RandomForestClassifier(min_samples_leaf=2), forest_parameters)
            
    # fit optimalisator on train data
    opti.fit(data_train, labels_train)
    # best random forest
    randomf = opti.best_estimator_
    
    # apply to testset
    y_pred = randomf.predict(data_test)
    conf = confusion_matrix(labels_test, y_pred)
    sens_test = conf[0, 0]/(conf[0, 0]+conf[0, 1])
    spec_test = conf[1, 1]/(conf[1, 0]+conf[1, 1])
    score_test = randomf.score(data_test,labels_test)
    
    # DataFrame: importance of the features
    features = feature_importance_RF(randomf, features['Specs'])
    features = features.reset_index(drop=True)    
    
    return randomf, score_test, sens_test, spec_test, features