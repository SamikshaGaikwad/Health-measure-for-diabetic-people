#IMPORTING THE LIBRARIES
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
#%matplotlib inline
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.cross_validation import train_test_split, cross_val_score
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import accuracy_score, roc_auc_score, roc_curve
from sklearn.preprocessing import binarize
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

#LOADING THE DATASET
dataset = pd.read_csv('diabetes.csv')
print(dataset.head())
print(dataset.describe())

data = dataset.iloc[:,0:8]
outcome = dataset.iloc[:,8]
x,y = data,outcome

#DISTRIBUTION OF DATASET INTO TRAINING AND TESTING SETS
x_train,x_test,y_train,y_test = train_test_split(x,y,random_state=0)

#COUNTING THE POSITIVE AND NEGATIVE VALUES
print("test values",y_test.value_counts())
#MEAN OF THE TESTING DISTRIBUTION
#print(1- y_test.mean())

#PARAMETER EVALUATION WITH GSC VALIDATION
print("Building Model")
gbe = GradientBoostingClassifier(random_state=0)
parameters={
    'learning_rate': [0.05, 0.1, 0.5],
    'max_features': [0.5, 1],
    'max_depth': [3, 4, 5]
}
gridsearch=GridSearchCV(gbe,parameters,cv=100,scoring='roc_auc')
gridsearch.fit(x,y)
#print(gridsearch.best_params_)
#print(gridsearch.best_score_)

#ADJUSTING DEVELOPMENT THRESHOLD
gbi = GradientBoostingClassifier(learning_rate=0.05,max_depth=3,max_features=0.5,random_state=0)
x_train,x_test,y_train,y_test = train_test_split(x,y,random_state=0)
gbi.fit(x_train,y_train)

#STORING THE PREDICTION
yprediction = gbi.predict_proba(x_test)[:,1]
print("Prediction raw output:")
print(yprediction)
#PLOTTING THE PREDICTIONS
plt.hist(yprediction,bins=10)
plt.xlim(0,1)
plt.xlabel("Predicted Proababilities")
plt.ylabel("Frequency")
plt.show() # display result
