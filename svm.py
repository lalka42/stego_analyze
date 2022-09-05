import pandas as pd
import numpy as np
from sklearn.metrics import recall_score
import tkinter.filedialog as fd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from joblib import dump, load
import matplotlib.pyplot as plt
from variable import variable

def tcp_svm(filename):
    #Чтение преобразованного дампа
    df = pd.read_csv(filename)
    X = df.drop(['ip.src','ip.dst'],axis = 1)
    
    #Работа ML
    svclassifier = load('svm_tcp_train.joblib')
    y_pred = svclassifier.predict(X)
    df['probability'] = y_pred.tolist()
    
    #Построение графика
    sum_prob = df['probability'].sum()
    sum_all = df.shape[0]
    labels = ["Всего пакетов","С вложениями"]
    vals = [sum_all,sum_prob]
    fig, ax = plt.subplots()
    explode = (0.1, 0)
    ax.pie(vals,labels = labels,autopct='%1.1f%%', shadow=True,explode=explode)
    plt.title("Метод SVM для TCP")
    text_g = 'Всего пакетов: ' + str(sum_all) + ' | Пакетов с вложениями: ' + str(sum_prob)
    ax.text(-1.25,-1.2,text_g,fontsize=10)
    plt.show()
    if variable.check():
        saved = fd.asksaveasfilename(
                filetypes=(("Excel files", "*.xlsx"),
                           ("All files", "*.*")))
        print(saved)
        if saved!='':
            df.to_excel(saved + '.xlsx')

def udp_svm(filename):
    df = pd.read_csv(filename)
    X = df.drop(['ip.src','ip.dst'],axis = 1)
    
    svclassifier = load('svm_udp_train.joblib')
    y_pred = svclassifier.predict(X)
    df['probability'] = y_pred.tolist()
    
    #Построение графика
    sum_prob = df['probability'].sum()
    sum_all = df.shape[0]
    labels = ["Всего пакетов","С вложениями"]
    vals = [sum_all,sum_prob]
    fig, ax = plt.subplots()
    explode = (0.1, 0)
    ax.pie(vals,labels = labels,autopct='%1.1f%%', shadow=True,explode=explode)
    plt.title("Метод SVM для UDP")
    text_g = 'Всего пакетов: ' + str(sum_all) + ' | Пакетов с вложениями: ' + str(sum_prob)
    ax.text(-1.25,-1.2,text_g,fontsize=10)
    plt.show()
    
    if variable.check():
        saved = fd.asksaveasfilename(
                filetypes=(("Excel files", "*.xlsx"),
                           ("All files", "*.*")))
        if savedsaved!='':
            df.to_excel(saved + '.xlsx')
            
def ipv4_svm(filename):
    df = pd.read_csv(filename)
    df['ip.dst'].replace('',np.nan, inplace = True)
    df.dropna(subset=['ip.dst'], inplace=True)
    df['ip.id'] = df['ip.id'].map(lambda x: int(x, 16))
    X = df.drop(['ip.src','ip.dst'],axis = 1)
    
    svclassifier = load('svm_ipv4_train.joblib')
    y_pred = svclassifier.predict(X)
    df['probability'] = y_pred.tolist()
    
    #Построение графика
    sum_prob = df['probability'].sum()
    sum_all = df.shape[0]
    labels = ["Всего пакетов","С вложениями"]
    vals = [sum_all,sum_prob]
    fig, ax = plt.subplots()
    explode = (0.1, 0)
    ax.pie(vals,labels = labels,autopct='%1.1f%%', shadow=True,explode=explode)
    plt.title("Метод SVM для IPv4")
    text_g = 'Всего пакетов: ' + str(sum_all) + ' | Пакетов с вложениями: ' + str(sum_prob)
    ax.text(-1.25,-1.2,text_g,fontsize=10)
    plt.show()
    
    if variable.check():
        saved = fd.asksaveasfilename(
                filetypes=(("Excel files", "*.xlsx"),
                           ("All files", "*.*")))
        if savedsaved!='':
            df.to_excel(saved + '.xlsx')