from tkinter import messagebox as mb

class Variable():
    def __init__(self, **kwargs):
        self.path = kwargs.get('path')
        self.dataset_path = kwargs.get('path')
        self.combo = kwargs.get('combo')
        self.path_of_save = kwargs.get('path')
        self.quit = 0
        self.save_diag = 0
        self.mean_diag = 0
        self.svm_count=float
        self.knn_count=float
        self.boost_count=float

    def change_path(self, path):
        self.path = path
        '''if self.path is not None:
            self.path = '"' + self.path + '"'''

    def change_dataset_path(self, path):
        self.dataset_path = path
    def change_save_path(self, path):
        self.path_of_save = path

    def change_save_diag(self, diag):
        self.save_diag = diag

    def change_mean_diag(self, diag):
        self.mean_diag = diag

    def change_combo(self, combo):
        self.combo = combo

    def change_svm_count(self, svm):
        self.svm_count = svm

    def change_knn_count(self, knn):
        self.knn_count = knn

    def change_boost_count(self, bost):
        self.boost_count = bost

variable = Variable()