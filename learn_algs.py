import pandas as pd
import numpy as np
import tkinter.filedialog as fd

#Алгоритмы обучения
from sklearn.svm import SVC
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
#Разделение на тренировочные наборы
from sklearn.model_selection import train_test_split
#Проверка работы алгоритма
from sklearn.metrics import recall_score
from sklearn.metrics import classification_report, confusion_matrix
#Сохранение и загрузка результатов обучения
from joblib import dump, load



#df = pd.read_excel("D:/Desktop/")
df['ip.dst'].replace('',np.nan, inplace = True)
df.dropna(subset=['ip.dst'], inplace=True)
df['ip.id'] = df['ip.id'].map(lambda x: int(x, 16))
X = df.drop(['ip.src','ip.dst','counter'],axis = 1)
y = df['counter']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20)

#boost

boost = HistGradientBoostingClassifier()
boost.fit(X_train, y_train)

#svm = load('svm_ipv4_train.joblib')
dump(boost,'boost_all_train.joblib')

y_pred = boost.predict(X_test)


#kNN
'''
knn = KNeighborsClassifier(n_neighbors = 4)
knn.fit(X_train, y_train)

#knn = load('knn_ipv4_train.joblib')
#dump(knn,'knn_ipv4_train.joblib')
y_pred = knn.predict(X_test)
'''
#Вывод результатов

#df['probability'] = y_pred.tolist()
    
#df.to_excel("D:/Desktop/IP_3_res.xlsx")

print('Матрица неточности:')
print(confusion_matrix(y_test,y_pred))
print('Отчёт о модели:')
print(classification_report(y_test,y_pred))
#print(svm.score(X_train,y_train))
#print(knn.score(X_train,y_train))
