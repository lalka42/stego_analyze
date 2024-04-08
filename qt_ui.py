from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QFont


# Класс, созданный PyUIC. Определяет интерфейс
class Ui_MainWindow(object):
    # Определяем элементы главного экрана UI
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 620)
        MainWindow.setMinimumSize(QtCore.QSize(1200, 620))
        MainWindow.setMaximumSize(QtCore.QSize(1200, 620))
        MainWindow.setAutoFillBackground(True)
        MainWindow.setStyleSheet('background-image: url("home_background.png")')
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setAutoFillBackground(True)
        self.centralwidget.setStyleSheet('background-image: url("home_background.png")')
        self.centralwidget.setObjectName("centralwidget")

        self.rb1 = QtWidgets.QRadioButton(self.centralwidget)
        self.rb1.setGeometry(QtCore.QRect(95, 150, 70, 20))
        self.rb1.setObjectName("rb1")
        self.rb1.setStyleSheet("background:transparent;")

        self.rb2 = QtWidgets.QRadioButton(self.centralwidget)
        self.rb2.setGeometry(QtCore.QRect(300, 150, 151, 20))
        self.rb2.setObjectName("rb2")
        self.rb2.setStyleSheet("background:transparent;")

        self.rb3 = QtWidgets.QRadioButton(self.centralwidget)
        self.rb3.setGeometry(QtCore.QRect(535, 150, 165, 20))
        self.rb3.setObjectName("rb3")
        self.rb3.setStyleSheet("background:transparent;")

        self.rb4 = QtWidgets.QRadioButton(self.centralwidget)
        self.rb4.setGeometry(QtCore.QRect(880, 150, 201, 20))
        self.rb4.setObjectName("rb4")
        self.rb4.setStyleSheet("background:transparent;")

        self.button_group = QtWidgets.QButtonGroup()
        self.button_group.addButton(self.rb1, 1)
        self.button_group.addButton(self.rb2, 2)
        self.button_group.addButton(self.rb3, 3)
        self.button_group.addButton(self.rb4, 4)


        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(310, 80, 600, 25))
        self.label.setObjectName("label")
        self.label.setFont(QFont('Arial', 14, QtGui.QFont.Bold))
        self.label.setStyleSheet("background:transparent;")

        self.separator_1 = QtWidgets.QFrame(self.centralwidget)
        self.separator_1.setGeometry(QtCore.QRect(240, 130, 5, 411))
        self.separator_1.setFrameShape(QtWidgets.QFrame.VLine)
        self.separator_1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.separator_1.setObjectName("separator_1")

        self.separator_2 = QtWidgets.QFrame(self.centralwidget)
        self.separator_2.setGeometry(QtCore.QRect(480, 130, 5, 411))
        self.separator_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.separator_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.separator_2.setObjectName("separator_2")

        self.separator_3 = QtWidgets.QFrame(self.centralwidget)
        self.separator_3.setGeometry(QtCore.QRect(730, 130, 5, 411))
        self.separator_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.separator_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.separator_3.setObjectName("separator_3")

        self.button_analyze_dump_choice = QtWidgets.QPushButton(self.centralwidget)
        self.button_analyze_dump_choice.setGeometry(QtCore.QRect(80, 250, 93, 28))
        self.button_analyze_dump_choice.setObjectName("button_analyze_dump_choice")
        self.button_analyze_dump_choice.setStyleSheet("background: #415374;")

        self.line_analyze_dump_choice = QtWidgets.QLabel(self.centralwidget)
        self.line_analyze_dump_choice.setGeometry(QtCore.QRect(33, 200, 190, 25))
        self.line_analyze_dump_choice.setObjectName("dump_choice_line")
        self.line_analyze_dump_choice.setWordWrap(True)
        self.line_analyze_dump_choice.setFont(QFont('Arial', 8))
        self.line_analyze_dump_choice.setStyleSheet("background:transparent;")

        self.checkbox_need_mean = QtWidgets.QCheckBox(self.centralwidget)
        self.checkbox_need_mean.setGeometry(QtCore.QRect(20, 310, 211, 20))
        self.checkbox_need_mean.setObjectName("checkbox_need_mean")
        self.checkbox_need_mean.setStyleSheet("background:transparent;")
       # Вырезал опцию сохранения графика, т.к. его можно сохранить при просмотре
        '''
        self.checkbox_need_saved = QtWidgets.QCheckBox(self.centralwidget)
        self.checkbox_need_saved.setGeometry(QtCore.QRect(20, 350, 201, 20))
        self.checkbox_need_saved.setObjectName("checkbox_need_saved")
        self.checkbox_need_saved.setStyleSheet("background:transparent;")
        '''
        self.line_analyze_res_choice = QtWidgets.QLabel(self.centralwidget)
        self.line_analyze_res_choice.setGeometry(QtCore.QRect(33, 420, 190, 22))
        self.line_analyze_res_choice.setObjectName("line_analyze_res_choice")
        self.line_analyze_res_choice.setWordWrap(True)
        self.line_analyze_res_choice.setFont(QFont('Arial', 8))
        self.line_analyze_res_choice.setStyleSheet("background:transparent;")

        self.button_analyze_res_choice = QtWidgets.QPushButton(self.centralwidget)
        self.button_analyze_res_choice.setGeometry(QtCore.QRect(36, 480, 170, 28))
        self.button_analyze_res_choice.setObjectName("dir_choice_button")
        self.button_analyze_res_choice.setStyleSheet("background: #415374;")

        self.line_dataset_dump_choice = QtWidgets.QLabel(self.centralwidget)
        self.line_dataset_dump_choice.setGeometry(QtCore.QRect(275, 200, 190, 22))
        self.line_dataset_dump_choice.setObjectName("dataset_dump_choice_line")
        self.line_dataset_dump_choice.setWordWrap(True)
        self.line_dataset_dump_choice.setFont(QFont('Arial', 8))
        self.line_dataset_dump_choice.setStyleSheet("background:transparent;")

        self.button_dataset_dump_choice = QtWidgets.QPushButton(self.centralwidget)
        self.button_dataset_dump_choice.setGeometry(QtCore.QRect(325, 250, 93, 28))
        self.button_dataset_dump_choice.setObjectName("dataset_dump_choice_button")
        self.button_dataset_dump_choice.setStyleSheet("background: #415374;")

        self.button_dataset_res_choice = QtWidgets.QPushButton(self.centralwidget)
        self.button_dataset_res_choice.setGeometry(QtCore.QRect(275, 480, 170, 28))
        self.button_dataset_res_choice.setObjectName("dataset_dir_choice_button")
        self.button_dataset_res_choice.setStyleSheet("background: #415374;")

        self.line_dataset_res_choice = QtWidgets.QLabel(self.centralwidget)
        self.line_dataset_res_choice.setGeometry(QtCore.QRect(275, 420, 190, 22))
        self.line_dataset_res_choice.setObjectName("dataset_dir_choice_line")
        self.line_dataset_res_choice.setWordWrap(True)
        self.line_dataset_res_choice.setFont(QFont('Arial', 8))
        self.line_dataset_res_choice.setStyleSheet("background:transparent;")

        self.line_new_model_choice = QtWidgets.QLabel(self.centralwidget)
        self.line_new_model_choice.setGeometry(QtCore.QRect(518, 200, 190, 22))
        self.line_new_model_choice.setObjectName("dataset_choice_line")
        self.line_new_model_choice.setWordWrap(True)
        self.line_new_model_choice.setFont(QFont('Arial', 8))
        self.line_new_model_choice.setStyleSheet("background:transparent;")

        self.button_new_model_choice = QtWidgets.QPushButton(self.centralwidget)
        self.button_new_model_choice.setGeometry(QtCore.QRect(540, 250, 135, 28))
        self.button_new_model_choice.setObjectName("dataset_choice_button")
        self.button_new_model_choice.setStyleSheet("background: #415374;")

        # Остатки от машинного обучения. Надо удалить
        '''
        self.svm_variable = QtWidgets.QLineEdit(self.centralwidget)
        self.svm_variable.setGeometry(QtCore.QRect(518, 360, 190, 22))
        self.svm_variable.setObjectName("svm_variable")

        self.knn_variable = QtWidgets.QLineEdit(self.centralwidget)
        self.knn_variable.setGeometry(QtCore.QRect(518, 410, 190, 22))
        self.knn_variable.setObjectName("knn_variable")

        self.boost_variable = QtWidgets.QLineEdit(self.centralwidget)
        self.boost_variable.setGeometry(QtCore.QRect(518, 460, 190, 22))
        self.boost_variable.setObjectName("boost_variable")

        self.default_learn = QtWidgets.QCheckBox(self.centralwidget)
        self.default_learn.setGeometry(QtCore.QRect(500, 290, 231, 41))
        self.default_learn.setObjectName("default_learn")
        self.default_learn.setStyleSheet("background:transparent;")
        '''
        self.table_rts_results = QtWidgets.QTableWidget(self.centralwidget)
        self.table_rts_results.setStyleSheet("background: white")
        self.table_rts_results.setGeometry(QtCore.QRect(780, 240, 392, 300))
        self.table_rts_results.setObjectName("rts_results")

        self.button_rts_analyze = QtWidgets.QPushButton(self.centralwidget)
        self.button_rts_analyze.setGeometry(QtCore.QRect(770, 570, 131, 28))
        self.button_rts_analyze.setObjectName("rts_analyze")
        self.button_rts_analyze.setStyleSheet("background: #1a6dc8; color: white;")

        self.button_rts_stop = QtWidgets.QPushButton(self.centralwidget)
        self.button_rts_stop.setGeometry(QtCore.QRect(1030, 570, 131, 28))
        self.button_rts_stop.setObjectName("rts_stop")
        self.button_rts_stop.setStyleSheet("background: #1a6dc8; color: white;")

        self.combobox_iface_choice = QtWidgets.QComboBox(self.centralwidget)
        self.combobox_iface_choice.setGeometry(QtCore.QRect(780, 200, 392, 28))

        self.combobox_dataset_type_choice = QtWidgets.QComboBox(self.centralwidget)
        self.combobox_dataset_type_choice.setGeometry(QtCore.QRect(295, 370, 135, 28))
        # Ещё остатки от ML
        '''
        self.spravka = QtWidgets.QPushButton(self.centralwidget)
        self.spravka.setGeometry(QtCore.QRect(555, 500, 121, 28))
        self.spravka.setObjectName("spravka")
        self.spravka.setStyleSheet("background: #415374;")
        '''

        self.button_pusk = QtWidgets.QPushButton(self.centralwidget)
        self.button_pusk.setGeometry(QtCore.QRect(300, 550, 131, 35))
        self.button_pusk.setObjectName("pusk")
        self.button_pusk.setStyleSheet("background: #1a6dc8; color: white;")

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        # self.connections()

        # С помощью translate задаём локаль, в нашем случае одну единственную вшитую - русскую

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Стегоанализ"))
        self.rb1.setText(_translate("MainWindow", "Анализ"))
        self.rb2.setText(_translate("MainWindow", "Подготовка датасета"))
        self.rb3.setText(_translate("MainWindow", "Загрузка новой модели"))
        self.rb4.setText(_translate("MainWindow", "Анализ в реальном времени"))
        self.label.setText(_translate("MainWindow", "Пожалуйста, выберите режим работы программы"))
        self.button_analyze_dump_choice.setText(_translate("MainWindow", "Выбор дампа"))
        self.checkbox_need_mean.setText(_translate("MainWindow", "Нужно ли вывести график?"))
        # self.checkbox_need_saved.setText(_translate("MainWindow", "Нужно ли сохранить график?"))
        self.button_analyze_res_choice.setText(_translate("MainWindow", "Куда сохранить результат?"))
        self.button_dataset_dump_choice.setText(_translate("MainWindow", "Выбор дампа"))
        self.button_dataset_res_choice.setText(_translate("MainWindow", "Куда сохранить результат?"))
        self.button_new_model_choice.setText(_translate("MainWindow", "Выбор новой модели"))
        # self.default_learn.setText(_translate("MainWindow", "Настройки обучения по умолчанию"))
        self.button_rts_analyze.setText(_translate("MainWindow", "Запустить анализ"))
        self.button_rts_stop.setText(_translate("MainWindow", "Остановить анализ"))
        # self.spravka.setText(_translate("MainWindow", "Справка"))
        self.button_pusk.setText(_translate("MainWindow", "ПУСК"))