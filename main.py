# -*- coding: utf-8 -*-

from sympy import *
import numpy as np
from scipy.optimize import minimize
from scipy import optimize
from math import *
from PyQt5 import QtWidgets
from Ui_frmMain import Ui_MainWindow
import requests
from bs4 import BeautifulSoup
from lxml import html
import csv

MassNumb = []
MassData = [] 
Model = 1

def bagSharp(alpha, beta, gamma, delta, covInv, r):
    bag = (1 / beta) * covInv.dot(r)
    Dohod = gamma / beta
    risk = sqrt(gamma / (beta ** 2))
    print("\n Шарп : ")
    print("Акция 1 доля: %s, доходность: %s"%(bag[0],r[0]*bag[0]))
    print("Акция 2 доля: %s, доходность: %s"%(bag[1],r[1]*bag[1]))
    print("Доходность портфеля : \n %s"%Dohod)
    print("Риск : \n %s"%risk)
    return bag, Dohod, risk

def minRisk(alpha, beta, gamma, delta, covInv, one, r):
    bag = (1 / alpha) * covInv.dot(one)
    Dohod = beta / alpha
    risk = sqrt(1 / alpha)
    print("\n minРиск : ")
    print("Акция 1 доля: %s, доходность: %s"%(bag[0],r[0]*bag[0]))
    print("Акция 2 доля: %s, доходность: %s"%(bag[1],r[1]*bag[1]))
    print("Доходность портфеля : \n %s"%Dohod)
    print("Риск : \n %s"%risk)
    return bag, Dohod, risk

def bagMarket(alpha, beta, gamma, delta, covInv, one, self, r):
    r0 = float(self.lineEdit.text()) / 100
    bag = (1 / (beta - alpha * r0)) * (covInv.dot(r - r0 * one))
    Dohod = (gamma - beta * r0) / (beta - alpha *r0)
    risk = sqrt(delta / ((beta - alpha * r0) ** 2))
    print("\n Рыночный : ")
    print("Акция 1 доля: %s, доходность: %s"%(bag[0],r[0]*bag[0]))
    print("Акция 2 доля: %s, доходность: %s"%(bag[1],r[1]*bag[1]))
    print("Доходность портфеля : \n %s"%Dohod)
    print("Риск : \n %s"%risk)
    return bag, Dohod, risk

def f(x, alpha, beta, gamma, delta):
         f = np.zeros([2])
         f[0] = alpha/(delta*x[0]**2)*((x[1]-beta/alpha)**2)+(1/(alpha*x[0]**2))
         f[1] = (2*x[1]*alpha*(beta-alpha*x[1]))/((((alpha*x[1]-beta)**2)+delta)*x[0])
         return f

def cov(Ra, Rb):
    if len(Ra) != len(Rb):
        return

    Ra_mean = np.mean(Ra)
    Rb_mean = np.mean(Rb)
    sum = 0
    for i in range(0, len(Ra)):
        sum += ((Ra[i] - Ra_mean) * (Rb[i] - Rb_mean))
    return sum/(len(Ra)-1)

class App(Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__()
        
    def setup_Ui(self):
        self.btnReadData.clicked.connect(self.readActiv)
        self.btnReadData_2.clicked.connect(self.readData)
        self.btnProcess.clicked.connect(self.process)
        self.table.setColumnCount(2)
        self.tblProcessed.setColumnCount(2)
        self.tblProcessed_2.setColumnCount(2)
        self.table.setShowGrid(True)
        self.table.setHorizontalHeaderLabels(["cheked", "Firm"])
        self.comboBox.activated[str].connect(self.onActivated)
       
    def onActivated(self, text):
        if text == "Модель Марковица":
            Model = 1
            print ("модель:", Model)
        if text == "Модель Шарпа":
            Model = 2
        if text == "Рыночный портфель":
            Model = 3

    def process(self):
        print("#")
        R = np.loadtxt("price.txt")    # данные о доходностях по акциям за месяц
        print (R)
        R = np.transpose(R)
        m, n = R.shape              #  размерность матрицы доходностей
        print(m, n)
        sZ = m                      #  количества измерений
        sA = n                      #  количества акций
        r = np.zeros([sA])          #  среднии доходности по акциям
        one = np.ones([sA])

        men = np.zeros([sZ,1])      #  наименьший замер по акции
        bol = np.zeros([sZ,1])      #  наибольший замер по акции
        otr = np.zeros([sZ,1])      #  величина отрезка попадания замера
        ver = np.zeros([5,sA])      #  матрица вероятности попадания замера в определенный отрезок
        covMat = np.zeros([sA,sA])     #  ковариационная матрица

        for j in np.arange(0, sA):   #  рассчет men и bol 
            a = R[:,j]
            k = min(a)
            men[j] = k
            k = max(a)
            bol[j] = k
        print(m, n)
        for j in np.arange(0, sA):   #  рассчет otr
            otr[j] = (bol[j]-men[j])/5
        for j in np.arange(0, sA):   #  рассчет матрицы ver
            k=men[j]
            for l in np.arange(0, 5):
                for i in np.arange(0, m):
                    if (R[i,j] >= k and R[i,j] < (k+otr[j])) or (R[i,j] > k and R[i,j] <= (k+otr[j])):
                        ver[l,j] = ver[l,j] + 1/30
                k=k+otr[j]
        print("ver \n", ver )

        for j in np.arange(0, sA):   #  рассчет r
            for i in np.arange(0, sZ):
                r[j]=np.mean(R[:,j])
        print("Средняя доходность акций: \n %s"%r)
        rTr = np.transpose(r)       #  транспонированный вектор r
        oneTr = np.transpose(one)   #  транспонированный единичный вектор

        for i in np.arange(0,n):    #  расчет матрицы cov
            for j in np.arange(0,n):
                x=R[0:m,i]
                y=R[0:m,j]
                covMat[i,j]=cov(x,y)
        print("Ковариационная матрица CV: \n %s"%covMat)
        covInv = np.linalg.inv(covMat) #  обратная матрица cov
        print("InvКовариационная матрица CV: \n %s"%covInv)

        alpha = np.dot(one, np.dot(oneTr, covInv))
        beta = oneTr.dot(np.dot(r, covInv))
        gamma = np.dot(rTr, np.dot(r, covInv))
        delta = alpha*gamma-beta**2
        print("альфа: %s"%alpha)
        print("бета: %s"%beta)
        print("дельта: %s"%delta)
        x0 = [0.1,0.1]
        sol = optimize.root(f,x0, args=(alpha, beta, gamma, delta), method='lm')
        r1=round(sol.x[0], 4)
        ris=round(sol.x[1], 4)
        print("Доходность портфеля : \n %s"%r1)
        print("Риск : \n %s"%ris)
        
        lamd = (gamma - beta * r1) / delta
        mu = (alpha * r1 - beta) / delta
        bagMod = (1 / beta) * covInv.dot(r)
        #np.dot(covInv, (np.dot(lamd, one) + np.dot(mu, r)))

        bSh = bagSharp(alpha, beta, gamma, delta, covInv, r)
        bMr = bagMarket(alpha, beta, gamma, delta, covInv, one, self, r)
        bMin = minRisk(alpha, beta, gamma, delta, covInv, one, r)

        self.tblProcessed.insertRow(0)
        self.tblProcessed.setItem(0, 0, QtWidgets.QTableWidgetItem('Доходность, %:'))
        self.tblProcessed.setItem(0, 1, QtWidgets.QTableWidgetItem(str(round(float(bMin[1]), 4)*100)))
        self.tblProcessed.insertRow(1)
        self.tblProcessed.setItem(1, 0, QtWidgets.QTableWidgetItem('Риск, %:'))
        self.tblProcessed.setItem(1, 1, QtWidgets.QTableWidgetItem(str(round(float(bMin[2]), 4)*100)))
        for i in range(len(bMin[0])):
            self.tblProcessed.insertRow(2 + i)
            self.tblProcessed.setItem(2 + i, 0, QtWidgets.QTableWidgetItem('Доля '+ str(MassNumb[i]) +' акции, %: '))
            self.tblProcessed.setItem(2 + i, 1, QtWidgets.QTableWidgetItem(str(round(float(str(round(float(bMin[0][i]), 4)*100)), 4))))
        #    print("#", i, ", len: ", len(s), "/", s)
        self.table.resizeColumnsToContents()

        self.tblProcessed_2.insertRow(0)
        self.tblProcessed_2.setItem(0, 0, QtWidgets.QTableWidgetItem('Доходность, %:'))
        self.tblProcessed_2.setItem(0, 1, QtWidgets.QTableWidgetItem(str(round(float(r1), 4))))
        self.tblProcessed_2.insertRow(1)
        self.tblProcessed_2.setItem(1, 0, QtWidgets.QTableWidgetItem('Риск, %:'))
        self.tblProcessed_2.setItem(1, 1, QtWidgets.QTableWidgetItem(str(round(float(ris), 4))))
        for i in range(len(bMin[0])):
            self.tblProcessed_2.insertRow(2 + i)
            self.tblProcessed_2.setItem(2 + i, 0, QtWidgets.QTableWidgetItem('Доля '+ str(MassNumb[i]) +' акции, %: '))
            self.tblProcessed_2.setItem(2 + i, 1, QtWidgets.QTableWidgetItem(str(round(float(str(round(float(bagMod[i]), 4)*100)), 4))))
        #    print("#", i, ", len: ", len(s), "/", s)
        self.table.resizeColumnsToContents()

    def readActiv(self):
        fileName = "data.txt"
        try:
            f = open(fileName, "r")
            sLines = f.readlines()
        finally:
            f.close()

        i = 0
        for s in sLines:
            self.table.insertRow(i)
            cb = QtWidgets.QCheckBox(parent = self.table)
            self.table.setCellWidget(i, 0, cb)                          #вставка чекбокса
            self.table.setItem(i, 1, QtWidgets.QTableWidgetItem(s))     #вставка названия фирмы
            i = i + 1
        #    print("#", i, ", len: ", len(s), "/", s)
        self.table.resizeColumnsToContents()
        #QtWidgets.QMessageBox.information(None, "info", "ОК", QtWidgets.QMessageBox.Yes)
        print(i)

    def readData(self):
        print("start func <readData>")
        #print(self.table.rowCount())
        f = open('price.txt', 'w')
        for i in range(self.table.rowCount()):
            it = self.table.cellWidget(i, 0)
            if it.isChecked():
                print(i)
                MassNumb.append(i+1)
                url = 'https://ru.investing.com/equities/'+massActiv[i]+'-historical-data' 
                user_agent = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36')
                r = requests.get(url, headers={'User-Agent':user_agent})
                r = r.text.replace('utf-8', '1251')
                #with open('test.html', 'w', encoding="utf-8") as output_file:
                #    output_file.write(r)
                soup = BeautifulSoup(r, features="lxml")
                data = []
                table = soup.find('table', attrs={'class':'genTbl closedTbl historicalTbl'})
                #print(table)
                try:
                    table_body = table.find('tbody')
                    rows = table_body.find_all('tr')
                    for row in rows:
                        cols = row.find_all('td')
                        cols = [ele.text.strip() for ele in cols]
                        data.append([ele for ele in cols if ele])
                except Exception:
                    QtWidgets.QMessageBox.information(None, "Error!", "Ошибка чтения внешних данных", QtWidgets.QMessageBox.Yes)
                #print(data)
                Zkr = []
                Okr = []
                Pr = []
                Z = []
                O = []
                for j in range(len(data)):
                    Zkr.append(data[j][1])
                for j in range(len(data)):
                    Okr.append(data[j][2])
                for it in range(len(Zkr)):
                    k = Zkr[it]
                    k = k.replace('.', '')
                    k = k.replace(',', '.')
                    Z.append(float(k))
                #print(Z)
                #print(" ")
                for it in range(len(Okr)):
                    k = Okr[it]
                    k = k.replace('.', '')
                    k = k.replace(',', '.')
                    O.append(float(k))
                #print(O)
                #print(" ")
                for i in range(len(data)):
                    Pr.append((Z[i]-O[i])/O[i])
                print(Pr)
                MassData.append(Pr)
                sPr = str(Pr).translate({ord(c): None for c in '!@#$[],'})
                f.write(sPr + '\n')
        QtWidgets.QMessageBox.information(None, "info", "Данные скачены", QtWidgets.QMessageBox.Yes)
        print(MassData)
        f.close()

        

if __name__ == "__main__":
    import sys
    massActiv = np.array(["alrosa-ao","aeroflot","vtb_rts","bashneft_rts","bashneft-(pref)","gazprom_rts","gazprom-neft_rts",
                          "inter-rao-ees_mm","lukoil_rts","mvideo_rts","magnit_rts","megafon-oao","sg-mechel_rts",
                          "moskovskiy-kreditnyi-bank-oao","mmk_rts","moskovskaya-birzha-oao","mostotrest_rts","mosenergo_rts",
                          "mts_rts","nlmk_rts","nmtp_rts","novatek_rts","gmk-noril-nickel_rts","npk-ovk-pao","polyus-zoloto_rts",
                          "raspadskaya","rosgosstrakh-oao","rosneft_rts","rosseti-ao","rostelecom","rostelecom-(pref)",
                          "gidroogk-011d","sberbank_rts","sberbank-p_rts","severstal_rts","afk-sistema_rts","surgutneftegas_rts",
                          "surgutneftegas-p_rts","tatneft_rts","tatneft-p_rts","tmk","transneft-p_rts","uralkaliy_rts","phosagro",
                          "fsk-ees_rts","e.on-russia","yandex?cid=102063"])
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = App()
    ui.setupUi(MainWindow)
    ui.setup_Ui()
    MainWindow.show()
    sys.exit(app.exec_())

