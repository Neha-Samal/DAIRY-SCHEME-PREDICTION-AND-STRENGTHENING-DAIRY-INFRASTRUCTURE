import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

schemes = ['Rashtriya Gokul Mission,','National Livestock Mission','Livestock Health and Disease Control','National Program for Dairy Development']           #change values here

#Importing the Dataset---------------------
data_set = pd.read_csv('state.csv')
print(data_set.to_string())

#Extract Depenedent & Independent Variables------------
x = data_set.iloc[:,[0,1,2,3,4,5]].values
y = data_set.iloc[:,6].values

print("x=",x)
print("y=",y)

#Splitting the training & test set------------------
from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.25,random_state=0)
#print("x_train=",x_train)
#print("x_test=",x_test)
#print("y_train=",y_train)
#print("y_test=",y_test)

#Feature scaling----------------------------------------
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
x_train = sc.fit_transform(x_train)
x_test = sc.transform(x_test)
#print("x_train",x_train)
#print("x_test",x_test)

#Fitting the Decision Tree classifier----------------------
from sklearn.tree import DecisionTreeClassifier
classifier = DecisionTreeClassifier(criterion='entropy')
classifier.fit(x_train,y_train)

#Prediction-------------------------------------------------
y_pred = classifier.predict(x_test)
#print(y_pred)

#Confusion matrix------------------------------------------
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test,y_pred)
print(cm)

acc = (cm[0,0]+cm[1,1])/np.sum(cm)
print("Accuracy:",acc)

def predScheme(test_sample):
    result = classifier.predict(test_sample)
    result = schemes[result[0]-1]
    return(result)



