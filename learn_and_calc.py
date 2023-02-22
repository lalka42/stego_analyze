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
from sklearn.metrics import classification_report


def calc(filename, mode):
    df = pd.read_csv(filename)
    outputs = df
    df['ip.dst'].replace('', np.nan, inplace=True)
    df.dropna(subset=['ip.dst'], inplace=True)
    df.replace(np.nan, 0, inplace=True)
    # df = df.dropna(subset=['ip.dst'], inplace=True)
    df['ip.id'] = df['ip.id'].map(lambda x: int(str(x), 16))

    X = df.drop(['ip.src', 'ip.dst'], axis=1)
    svm = load('svm_model.joblib')
    knn = load('knn_model.joblib')
    boost = load('boost_model.joblib')
    y_pred_svm = svm.predict(X)
    outputs['svm_detect'] = y_pred_svm.tolist()
    y_pred_knn = knn.predict(X)
    outputs['knn_detect'] = y_pred_svm.tolist()
    y_pred_boost = boost.predict(X)
    outputs['boost_detect'] = y_pred_svm.tolist()
    if mode == 1:
        save_res(outputs)
        if variable.mean_diag != False or variable.save_diag != False:
            plot(outputs)
    elif mode == 2:
        if outputs.iloc[0]['ip.src'] != 0:
            row = [outputs.iloc[0]['ip.src'], outputs.iloc[0]['ip.dst'], outputs.iloc[0]['svm_detect'], outputs.iloc[0]['knn_detect'], outputs.iloc[0]['boost_detect']]
            variable.change_rts_row(row)


def learn(filename):
    svm = SVC(kernel='linear')
    knn = KNeighborsClassifier(n_neighbors=3)
    boost = HistGradientBoostingClassifier()
    df = pd.read_excel(filename)
    # del df[df.columns[0]]
    check_dump = 'counter' in df.columns

    if not check_dump:
        variable.change_check_learn(False)
        return None
    else:
        df['ip.id'] = df['ip.id'].map(lambda x: int(str(x), 16))
        X = df.drop(['ip.src', 'ip.dst', 'counter'], axis=1)
        y = df['counter']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=float(variable.svm_count), random_state=42)
        svm.fit(X_train, y_train)
        dump(svm, 'svm_model.joblib')
        y_pred = svm.predict(X_test)

        check_test = pd.DataFrame(
            {
                "y_test": y_test,
                "y_pred": y_pred.flatten(),
            })

        report1 = classification_report(check_test["y_pred"], check_test["y_test"])

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=float(variable.knn_count), random_state=42)
        knn.fit(X_train, y_train)
        dump(knn, 'knn_model.joblib')
        y_pred = knn.predict(X_test)

        check_test = pd.DataFrame(
            {
                "y_test": y_test,
                "y_pred": y_pred.flatten(),
            })

        report2 = classification_report(check_test["y_pred"], check_test["y_test"])

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=float(variable.boost_count),
                                                            random_state=42)
        boost.fit(X_train, y_train)
        dump(boost, 'boost_model.joblib')
        y_pred = boost.predict(X_test)

        check_test = pd.DataFrame(
            {
                "y_test": y_test,
                "y_pred": y_pred.flatten(),
            })

        report3 = classification_report(check_test["y_pred"], check_test["y_test"])
        variable.change_metrics(report1, report2, report3)


def plot(df):
    sum_prob_svm = df['svm_detect'].sum()
    sum_prob_knn = df['knn_detect'].sum()
    sum_prob_boost = df['boost_detect'].sum()
    sum_all = df.shape[0]
    x = ['Всего пакетов', 'SVM', 'k-NN', 'Boost']
    y = [sum_all, sum_prob_svm, sum_prob_knn, sum_prob_boost]
    fig, ax = plt.subplots()
    ax.bar(x, y)
    ax.set_facecolor('seashell')
    plt.title("Результаты анализа")
    add_value_labels(ax)
    if variable.mean_diag:
        plt.show()
    if variable.save_diag:
        plt.savefig(variable.path_of_save + '/' + strftime("%Y-%m-%d_%H-%M-%S", localtime()) + '.png')

def add_value_labels(ax, spacing=5):
    """Add labels to the end of each bar in a bar chart.

    Arguments:
        ax (matplotlib.axes.Axes): The matplotlib object containing the axes
            of the plot to annotate.
        spacing (int): The distance between the labels and the bars.
    """

    # For each bar: Place a label
    for rect in ax.patches:
        # Get X and Y placement of label from rect.
        y_value = rect.get_height()
        x_value = rect.get_x() + rect.get_width() / 2

        # Number of points between bar and label. Change to your liking.
        space = spacing
        # Vertical alignment for positive values
        va = 'bottom'

        # If value of bar is negative: Place label below bar
        if y_value < 0:
            # Invert space to place label below
            space *= -1
            # Vertically align label at top
            va = 'top'

        # Use Y value as label and format number with one decimal place
        label = "{:.1f}".format(y_value)

        # Create annotation
        ax.annotate(
            label,                      # Use `label` as label
            (x_value, y_value),         # Place label at end of the bar
            xytext=(0, space),          # Vertically shift label by `space`
            textcoords="offset points", # Interpret `xytext` as offset in points
            ha='center',                # Horizontally center label
            va=va)                      # Vertically align label differently for
                                        # positive and negative values.



def save_res(df):
    df.to_excel(variable.path_of_save + '/' + strftime("%Y-%m-%d_%H-%M-%S", localtime()) + '.xlsx')
