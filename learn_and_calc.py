import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.ensemble import HistGradientBoostingClassifier
from joblib import dump, load
import matplotlib.pyplot as plt
from variable import variable
from time import localtime, strftime
from sklearn.metrics import f1_score, accuracy_score, confusion_matrix, classification_report


def calc(filename):

    df = pd.read_csv(filename)
    outputs = df
    df['ip.dst'].replace('', np.nan, inplace=True)
    df.dropna(subset=['ip.dst'], inplace=True)
    df.replace(np.nan, 0, inplace=True)
    #df = df.dropna(subset=['ip.dst'], inplace=True)
    print(df.to_string())
    print(type(df['ip.id']))
    df['ip.id'] = df['ip.id'].map(lambda x: int(str(x), 16))

    X = df.drop(['ip.src', 'ip.dst'], axis=1)
    svm = load('svm_model.joblib')
    knn = load('knn_model.joblib')
    boost = load('boost_model.joblib')
    y_pred_svm = svm.predict(X)
    outputs['svm_probability'] = y_pred_svm.tolist()
    y_pred_knn = knn.predict(X)
    outputs['knn_probability'] = y_pred_svm.tolist()
    y_pred_boost = boost.predict(X)
    outputs['boost_probability'] = y_pred_svm.tolist()
    save_res(outputs)
    if variable.mean_diag != 0 or variable.save_diag != 0:
     plot(outputs)

def learn(filename):
    svm = SVC(kernel='linear')
    knn = KNeighborsClassifier(n_neighbors=3)
    boost = HistGradientBoostingClassifier()
    df = pd.read_excel(filename)
    df['ip.id'] = df['ip.id'].map(lambda x: int(str(x), 16))
    X = df.drop(['ip.src', 'ip.dst','counter'], axis=1)
    y = df['counter']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=float(variable.svm_count), random_state=42)
    svm.fit(X_train, y_train)
    dump(svm,'svm_model.joblib')
    y_pred = svm.predict(X_test)

    check_test = pd.DataFrame(
        {
            "y_test": y_test,
            "y_pred": y_pred.flatten(),
        })

    report1 = classification_report(check_test["y_pred"], check_test["y_test"])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=float(variable.knn_count), random_state=42)
    knn.fit(X_train, y_train)
    dump(knn,'knn_model.joblib')
    y_pred = knn.predict(X_test)

    check_test = pd.DataFrame(
        {
            "y_test": y_test,
            "y_pred": y_pred.flatten(),
        })

    report2 = classification_report(check_test["y_pred"], check_test["y_test"])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=float(variable.boost_count), random_state=42)
    boost.fit(X_train, y_train)
    dump(boost,'boost_model.joblib')
    y_pred = boost.predict(X_test)

    check_test = pd.DataFrame(
        {
            "y_test": y_test,
            "y_pred": y_pred.flatten(),
        })

    report3 = classification_report(check_test["y_pred"], check_test["y_test"])
    variable.change_metrics(report1, report2, report3)

def plot(df):
    sum_prob_svm = df['svm_probability'].sum()
    sum_prob_knn = df['knn_probability'].sum()
    sum_prob_boost = df['boost_probability'].sum()
    sum_all = df.shape[0]
    labels = ["Всего пакетов", "Обнаружил SVM:", "Обнаружил k-NN:", "Обнаружил Boost:"]
    vals = [sum_all, sum_prob_svm, sum_prob_knn, sum_prob_boost]
    fig, ax = plt.subplots()
    explode = None
    ax.pie(vals, labels=labels, autopct='%1.1f%%', shadow=True, explode=explode)
    plt.title("Вычисление ")
    text_g = 'Всего: ' + str(sum_all) + ' | Обнаружил SVM: ' + str(sum_prob_svm) + ' | Обнаружил k-NN: ' + str(sum_prob_knn) + ' | Обнаружил Boost: ' + str(sum_prob_boost)
    ax.text(-2.2, -1.2, text_g, fontsize=10)
    if variable.mean_diag == 1:
        plt.show()
    if variable.save_diag == 1:
        plt.savefig(variable.path_of_save + '/' + strftime("%Y-%m-%d_%H-%M-%S", localtime()) + '.png')

def save_res(df):
    df.to_excel(variable.path_of_save + '/' + strftime("%Y-%m-%d_%H-%M-%S", localtime()) + '.xlsx')
