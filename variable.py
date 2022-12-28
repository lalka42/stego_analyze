from tkinter import messagebox as mb

class Variable():
    def __init__(self, **kwargs):
        self.path = kwargs.get('path')
        self.combo = kwargs.get('combo')

    def change_path(self, path):
        self.path = path
        '''if self.path is not None:
            self.path = '"' + self.path + '"'''
    
    def change_combo(self, combo):
        self.combo = combo
    
    def check(self):
        answer = mb.askyesno(
        title="Вопрос", 
        message="Сохранить результаты анализа?")
        if answer:
            return True

variable = Variable()