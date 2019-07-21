# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_frmMain.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1014, 655)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.btnReadData = QtWidgets.QPushButton(self.centralwidget)
        self.btnReadData.setGeometry(QtCore.QRect(40, 10, 171, 51))
        self.btnReadData.setObjectName("btnReadData")
        self.table = QtWidgets.QTableWidget(self.centralwidget)
        self.table.setGeometry(QtCore.QRect(350, 30, 321, 531))
        self.table.setObjectName("table")
        self.table.setColumnCount(0)
        self.table.setRowCount(0)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.btnProcess = QtWidgets.QPushButton(self.centralwidget)
        self.btnProcess.setGeometry(QtCore.QRect(40, 260, 171, 51))
        self.btnProcess.setObjectName("btnProcess")
        self.tblProcessed = QtWidgets.QTableWidget(self.centralwidget)
        self.tblProcessed.setGeometry(QtCore.QRect(680, 30, 321, 241))
        self.tblProcessed.setObjectName("tblProcessed")
        self.tblProcessed.setColumnCount(0)
        self.tblProcessed.setRowCount(0)
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(40, 170, 181, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(250, 210, 91, 22))
        self.lineEdit.setObjectName("lineEdit")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 210, 231, 16))
        self.label.setObjectName("label")
        self.btnReadData_2 = QtWidgets.QPushButton(self.centralwidget)
        self.btnReadData_2.setGeometry(QtCore.QRect(40, 90, 171, 51))
        self.btnReadData_2.setObjectName("btnReadData_2")
        self.tblProcessed_2 = QtWidgets.QTableWidget(self.centralwidget)
        self.tblProcessed_2.setGeometry(QtCore.QRect(680, 320, 321, 241))
        self.tblProcessed_2.setObjectName("tblProcessed_2")
        self.tblProcessed_2.setColumnCount(0)
        self.tblProcessed_2.setRowCount(0)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(350, 10, 111, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(680, 10, 271, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(680, 300, 311, 16))
        self.label_4.setObjectName("label_4")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1014, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Формирование инвестиционного портфеля"))
        self.btnReadData.setText(_translate("MainWindow", "Показать список активов"))
        self.btnProcess.setText(_translate("MainWindow", "Рассчет портфеля"))
        self.comboBox.setItemText(0, _translate("MainWindow", "Модель Марковица"))
        self.comboBox.setItemText(1, _translate("MainWindow", "Модель Шарпа"))
        self.comboBox.setItemText(2, _translate("MainWindow", "Рыночный портфель"))
        self.label.setText(_translate("MainWindow", "Доходность безрискового актива, % :"))
        self.btnReadData_2.setText(_translate("MainWindow", "Скачать данные за мессяц"))
        self.label_2.setText(_translate("MainWindow", "Список активов:"))
        self.label_3.setText(_translate("MainWindow", "Структура портфеля классической модели:"))
        self.label_4.setText(_translate("MainWindow", "Структура портфеля модифицированной модели:"))

