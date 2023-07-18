#!pip install sklearn
#!pip install pandas
#!pip install imblearn
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE, ADASYN
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.neighbors import KNeighborsClassifier

from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB

data = pd.read_csv("Application_Data.csv")

# DATA EXPLORATORY
data['Status'].value_counts(normalize=True)
data.info()


# DATA PROCESSING
# transform categorical attributes to numeric

objectCol = ['Applicant_Gender','Income_Type','Education_Type','Family_Status','Housing_Type']
for i in objectCol:
    label = LabelEncoder()
    data[i]= label.fit_transform(data[i].values)

# mapping occupations to numbers
occupation_dct = {'Security staff':0, 'Sales staff':1, 
                  'Accountants':2, 'Laborers':3, 
                  'Managers':4,'Drivers':5, 
                  'Core staff':6, 'High skill tech staff':7, 
                  'Cleaning staff':8,'Private service staff':9,
                  'Cooking staff':10, 'Low-skill Laborers':11,
                  'Medicine staff':12, 'Secretaries':13,
                  'Waiters/barmen staff':14, 'HR staff':15,
                  'Realty agents':16, "IT staff":17}
data['Job_Title']= data['Job_Title'].str.rstrip()
data['Job_Title'] = data['Job_Title'].map(occupation_dct).values

#data after convertion
data.info()

# dropping label and status
x = data.iloc[:,1:-1] # X value contains all the variables except labels
y = data.iloc[:,-1]

# TRAINING - TESTING DATA SPLIT

x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=0.2, random_state=123)

#standardize data

ss = StandardScaler()
X_scaled = pd.DataFrame(ss.fit_transform(x_train), columns=x_train.columns)
X_test_scaled = pd.DataFrame(ss.transform(x_test), columns=x_test.columns)

# OVERSAMPLE the minor class using ADASYN - SMOTE

# adasyn
sm = ADASYN()
x_train_ada, y_train_ada = sm.fit_resample(x_train, y_train)
x_test_ada, y_test_ada = sm.fit_resample(X_test_scaled, y_test)
# smote
oversamp = SMOTE()
X_train_bal, y_train_bal = oversamp.fit_resample(X_scaled, y_train)
X_test_balanced, y_test_balanced = oversamp.fit_resample(X_test_scaled, y_test)

# counting number of 1 and 0 in lables 
# comparing ADASYN and SMOTE oversampled training
print('original train data label: ',y_train.value_counts())
print('oversampled train label - ADASYN: ', y_train_ada.value_counts())
print('oversampled train label - SMOTE: ', y_train_bal.value_counts())

# CLASSIFICATIONS

# SVM classifier


model = SVC(C=1, gamma = 0.001)
model.fit(X_train_bal, y_train_bal)
y_pred_svm = model.predict(X_test_balanced)
SVM_accuracy = accuracy_score(y_test_balanced,y_pred_svm)
print('SVM Accuracy (SMOTE) ', SVM_accuracy)

model.fit(x_train_ada, y_train_ada)
y_ada_pred_svm =model.predict(x_test_ada)
print('SVM Accuracy (ADASYN) ',accuracy_score(y_test_ada, y_ada_pred_svm))

# ROC AUC can be calculated using the code below, however, it takes ~15min to compute

#model = SVC(C=1, gamma = 'scale', probability= True)
# roc_svm = model.predict_proba(X_test_balanced)[:,1]
# print('SVM ROC AUC (SMOTE) ', roc_auc_score(y_test_balanced, roc_svm))
# roc_svm_ada = model.predict_proba(X_test_balanced)[:,1]
# print('SVM ROC AUC (ADASYN) ', roc_auc_score(y_test_ada, roc_svm_ada))

# Random Forest classifier

model = RandomForestClassifier(random_state = 0)
model.fit(X_train_bal, y_train_bal)
y_predict = model.predict(X_test_balanced)
random_forest_accuracy = accuracy_score(y_test_balanced, y_predict)
print("Random Forest Accuracy (SMOTE) " ,random_forest_accuracy )
roc_rf = model.predict_proba(X_test_balanced)[:,1]
print('Random Forest ROC AUC (SMOTE) ', roc_auc_score(y_test_balanced, roc_rf))

model.fit(x_train_ada, y_train_ada)
y_ada_predict = model.predict(x_test_ada)
ada_random_forest_accuracy = accuracy_score(y_test_ada, y_ada_predict)
print("Random Forest Accuracy (ADASYN) ", ada_random_forest_accuracy)

roc_rf_ada = model.predict_proba(x_test_ada)[:,1]
print('Random Forest ROC AUC (ADASYN) ', roc_auc_score(y_test_ada, roc_rf_ada))


# KNN classifier

knn = KNeighborsClassifier(n_neighbors=15)
knn.fit(X_train_bal, y_train_bal)
y_pred_knn = knn.predict(X_test_balanced)
knn_accuracy = accuracy_score(y_test_balanced, y_pred_knn)
print("KNN Accuracy (SMOTE) ", knn_accuracy)

roc_knn = knn.predict_proba(X_test_balanced)[:,1]
print('KNN ROC AUC (SMOTE) ', roc_auc_score(y_test_balanced, roc_knn))

knn.fit(x_train_ada, y_train_ada)
y_ada_pred_knn = knn.predict(x_test_ada)
ada_knn_accuracy = accuracy_score(y_test_ada, y_ada_predict)
print("KNN Accuracy (ADSYN) ", ada_knn_accuracy)

roc_knn_ada = knn.predict_proba(x_test_ada)[:,1]
print('KNN ROC AUC (ADASYN) ', roc_auc_score(y_test_ada, roc_knn_ada))

# Naive Bayes classifier

bayes = GaussianNB()
bayes.fit(X_train_bal, y_train_bal)
y_pred_bayes = bayes.predict(X_test_balanced)
bayes_accuracy = accuracy_score(y_test_balanced, y_pred_bayes)
print('Naive Bayes Accuracy (SMOTE) ', bayes_accuracy)

roc_bayes = bayes.predict_proba(X_test_balanced)[:,1]
print('Naive Bayes ROC AUC (SMOTE) ', roc_auc_score(y_test_balanced, roc_bayes))

bayes.fit(x_train_ada, y_train_ada)
y_ada_pred_bayes = bayes.predict(x_test_ada)
ada_bayes_accuracy = accuracy_score(y_test_ada, y_ada_pred_bayes)
print("Naive Bayes Accuracy (ADASYN) ", ada_bayes_accuracy)

roc_bayes = bayes.predict_proba(x_test_ada)[:,1]
roc_bayes_ada_acc = roc_auc_score(y_test_ada, roc_bayes)
print('Naive Bayes ROC AUC (ADASYN) ', roc_bayes_ada_acc)


