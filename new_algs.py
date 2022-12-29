import pandas as pd
import numpy as np
from sklearn.metrics import recall_score
import tkinter.filedialog as fd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from joblib import dump, load
import matplotlib.pyplot as plt
from variable import variable
import datetime


def knn(filename):
    df = pd.read_csv(filename)
    #df['ip.dst'].replace('', np.nan, inplace=True)
    #df.dropna(subset=['ip.dst'], inplace=True)
    #df['ip.id'] = df['ip.id'].map(lambda x: int(x, 16))
    X = df.drop(['ip.src', 'ip.dst'], axis=1)
    knn = load('knn_udp_train.joblib')
    y_pred = knn.predict(X)
    df['probability'] = y_pred.tolist()
    if variable.mean_diag != 0 or variable.save_diag != 0:
     plot(df)



def svm(filename):
    df = pd.read_csv(filename)
    df['ip.id'] = df['ip.id'].map(lambda x: int(x, 16))
    X = df.drop(['ip.src', 'ip.dst'], axis=1)
    svm = load('svm_tcp_train.joblib')
    y_pred = svm.predict(X)
    df['probability'] = y_pred.tolist()



def plot(df):
    sum_prob = df['probability'].sum()
    sum_all = df.shape[0]
    labels = ["Всего пакетов", "С вложениями"]
    vals = [sum_all, sum_prob]
    fig, ax = plt.subplots()
    explode = (0.1, 0)
    ax.pie(vals, labels=labels, autopct='%1.1f%%', shadow=True, explode=explode)
    plt.title("Вычисление ")
    text_g = 'Всего пакетов: ' + str(sum_all) + ' | Пакетов с вложениями: ' + str(sum_prob)
    ax.text(-1.25, -1.2, text_g, fontsize=10)
    if variable.mean_diag == 1:
        plt.show()
    if variable.save_diag == 1:
        plt.savefig(datetime.strftime.now("%d-%m-%Y %H:%M") + '.png')

def save_res(df):
    df.to_excel(variable.path_of_save + datetime.strftime.now("%d-%m-%Y %H:%M") + '.xlsx')
