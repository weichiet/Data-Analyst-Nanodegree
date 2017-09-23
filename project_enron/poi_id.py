#!/usr/bin/python
'''
The purpose of this script is to generate the three pickle files 
(classifier, dataset, and list of features) that reflect the final algorithm.
For detail steps on deriving the final model, please refer to 
'identify_fraud.ipynb'. 
'''
# Import libraries necessary for this project

import sys
import pickle
sys.path.append("../tools/")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import warnings;
warnings.simplefilter('ignore')
warnings.filterwarnings("ignore")
import seaborn as sns

from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.cross_validation import StratifiedShuffleSplit
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score, precision_score
from sklearn.metrics import recall_score, f1_score
from sklearn.metrics import make_scorer
from sklearn.grid_search import GridSearchCV
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB

from feature_format import featureFormat, targetFeatureSplit
from tester import test_classifier, dump_classifier_and_data

#%%
### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".

# Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

# Create DataFrame from dictionary
df = pd.DataFrame.from_dict(data_dict, orient='index', dtype=np.float)
df.reset_index(inplace=True)
df.rename(columns={'index': 'name'}, inplace=True)

# Select the features to be used
# Put 'poi' as first features and remove 'email_address' and 'name'
features_list = ['poi']  +  [feature for feature in df if feature != 'poi' 
                              and feature != 'email_address' and feature != 'name']

print '\nFeature List:\n'
print features_list

print "\nTotal number of data points:", df.shape[0]
print "Number of person of interest (POI):", len(df[df['poi']==1])
print "\nPercentage of non-POIs vs POIs:"
print (df['poi']==1).value_counts(normalize=True).round(4)*100
print "\nNumber of selected features:", len(features_list)
#%%
### Task 2: Remove outliers

# Remove the outliers from the dataset
outlier_list = ['TOTAL', 'THE TRAVEL AGENCY IN THE PARK', 'LOCKHART EUGENE E']
df = df[~(df['name'].isin(outlier_list))]
df.reset_index(inplace=True)

print '\nOutliers: "' + (', '.join(outlier_list)) + '" are removed from dataset.'

#%%
### Task 3: Create new feature(s)

# Create the two new features
features_list.append('to_poi_ratio')
features_list.append('from_poi_ratio')

df['to_poi_ratio'] = df['from_this_person_to_poi']/df['from_messages']
df['from_poi_ratio'] = df['from_poi_to_this_person']/df['to_messages']

# Before proceeding to next step, 
# we keep the selected features in the dataframe
# and replace NaN with 0
df = df[features_list]
df.fillna(0, inplace=True)

print '\nTwo new features are created: to_poi_ratio and from_poi_ratio'

#%%
### Feature Selection

# Seperate the label and the features from the dataframe
labels = df['poi']
features = df.drop('poi', axis = 1)

# Scale the features uisng MinMaxScaler function 
features = MinMaxScaler().fit_transform(features)

# Compute the scores of each features
k_best = SelectKBest(k = 'all', score_func = f_classif)
k_best.fit(features,labels)
scores = k_best.scores_

# Sort the scores
sorted_scores = list(sorted(zip(features_list[1:], scores), key=lambda x: x[1], reverse = True))
sorted_scores_df = pd.DataFrame(sorted_scores, columns=['Features','Scores'])

# Select the features with score > 10
selected_features_list = sorted_scores_df[sorted_scores_df['Scores'] > 10]['Features']
selected_features = df[selected_features_list]

# Scale the features uisng MinMaxScaler function 
selected_features = MinMaxScaler().fit_transform(selected_features)

print '\nSelected features based on SelectKBest scores:'
print selected_features_list
#%%
### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html

# Seperate the data into training set and test set
features_train, features_test, labels_train, labels_test = \
    train_test_split(selected_features, labels, test_size=0.3, random_state= 71)
    
random_state = 10
# Initialize the four models
clf_A = GaussianNB()
clf_B = LogisticRegression(random_state = random_state)
clf_C = DecisionTreeClassifier(random_state = random_state)
clf_D = AdaBoostClassifier(random_state = random_state)

# Collect results on the learners
results = {}
for clf in [clf_A, clf_B, clf_C, clf_D]: 
    clf_name = clf.__class__.__name__
    clf.fit(features_train, labels_train)
    predictions = clf.predict(features_test)
        
    results[clf_name] = {}
    results[clf_name]['Accuracy'] = accuracy_score(labels_test,predictions)
    results[clf_name]['F1 Score'] = f1_score(labels_test,predictions)

# Convert the classification results to dataframe
results_df = pd.DataFrame.from_dict(results, orient='index', dtype=np.float)
results_df.reset_index(inplace=True)

print '\nClassification performance of four classifiers:\n'
print results_df

#%%
### Task 5: Tune your classifier to achieve better than .3 precision and recall 
### using our testing script. Check the tester.py script in the final project
### folder for details on the evaluation method, especially the test_classifier
### function. Because of the small size of the dataset, the script uses
### stratified shuffle split cross validation. For more info: 
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

# Seperate the data into training set and test set
features_train, features_test, labels_train, labels_test = \
    train_test_split(selected_features, labels, test_size = 0.3, random_state = 789)

# Initialize the classifier
clf = DecisionTreeClassifier(random_state = 485)

# Create the parameters list
parameters  = {'max_depth': np.arange(3, 15),'min_samples_leaf': np.arange(5, 15),
              'criterion': ['gini','entropy'], 'splitter' : ['best','random']}

# Create the scoring function
scorer = make_scorer(f1_score)  

# Generate cross-validation dataset
cv = StratifiedShuffleSplit(labels_train, n_iter = 10, random_state = 42)

# Perform grid search on the classifier using 'scorer' as the scoring method
grid_obj = GridSearchCV(estimator = clf, param_grid = parameters, scoring = scorer, cv = cv)

# Fit the grid search object to the training data and find the optimal parameters
grid_fit = grid_obj.fit(features_train, labels_train)

# Get the best estimator
best_estimator = grid_fit.best_estimator_

# Make predictions using the default and optimized models
predictions = (clf.fit(features_train, labels_train)).predict(features_test)
best_predictions = best_estimator.predict(features_test)
    
# Collect the prediction results
results = {}
results['Unoptimized Model'] = {}
results['Unoptimized Model']['Accuracy'] = accuracy_score(labels_test, predictions)
results['Unoptimized Model']['F1 Score'] = f1_score(labels_test, predictions)
results['Unoptimized Model']['Precision'] = precision_score(labels_test, predictions)
results['Unoptimized Model']['Recall'] = recall_score(labels_test, predictions)

results['Optimized Model'] = {}
results['Optimized Model']['Accuracy'] = accuracy_score(labels_test,best_predictions)
results['Optimized Model']['F1 Score'] = f1_score(labels_test, best_predictions)
results['Optimized Model']['Precision'] = precision_score(labels_test, best_predictions)
results['Optimized Model']['Recall'] = recall_score(labels_test, best_predictions)
#%%
# Report the before-and-after scores
print '\nBest parameters:'
print grid_fit.best_params_
print "\nUnoptimized Model\n------"
print "Accuracy score on testing data: {:.4f}".format(results['Unoptimized Model']['Accuracy'])
print "Precision on testing data: {:.4f}".format(results['Unoptimized Model']['Precision'])
print "Recall on testing data: {:.4f}".format(results['Unoptimized Model']['Recall'])
print "F1-score on testing data: {:.4f}".format(results['Unoptimized Model']['F1 Score'])
print "\nOptimized Model\n------"
print "Final accuracy score on the testing data: {:.4f}".format(results['Optimized Model']['Accuracy'])
print "Final precision on testing data: {:.4f}".format(results['Optimized Model']['Precision'])
print "Final recall on testing data: {:.4f}".format(results['Optimized Model']['Recall'])
print "Final F1-score on the testing data: {:.4f}".format(results['Optimized Model']['F1 Score'])
print '\n'
print classification_report(labels_test, best_predictions)    

#%%
### Evaluate the final model by using 'test_classifier' function in 'tester.py' script.

# Convert the data to dictionary to be compatible with 'test_classifier' input format
selected_features_df = pd.DataFrame(data = selected_features, columns = selected_features_list)
labels_df = pd.DataFrame(data = labels)

my_dataset_df = pd.concat([labels_df, selected_features_df], axis=1)
my_dataset = pd.DataFrame.to_dict(my_dataset_df, orient='index')

print '\nPerformance of the model based on test_classifier function:'
# Pass the optimized model to the 'test_classifier' function
test_classifier(best_estimator, my_dataset, list(my_dataset_df.columns))   
 
#%%
### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

dump_classifier_and_data(best_estimator, my_dataset, list(my_dataset_df.columns))