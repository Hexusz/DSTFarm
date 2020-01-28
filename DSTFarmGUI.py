from PyQt5 import QtWidgets, uic
import Steam2FA
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtCore import Qt,QThread
from PyQt5.QtWidgets import QWidget, QCheckBox, QApplication
from PyQt5.QtCore import pyqtSlot
from pywinauto.application import Application
import win32api, win32con, win32gui, win32ui
import sys, os
import qtable
import var
import json
import time
#добавить всем for maf in fds: это if maf.endswith(('.maFile')):
data_acc_name=[]
data_acc_check=[]
data_acc_progres=[]
cb=[]
progress=[]
fds = sorted(os.listdir('./maFiles'))
for maf in fds:
    if maf.endswith(('.maFile')):
        with open('./maFiles/'+str(maf), "r") as read_file:
            data = json.load(read_file)
            data_acc_name.append(data["account_name"])
            data_acc_check.append(True)
            data_acc_progres.append(0)

app = QtWidgets.QApplication([])
win = uic.loadUi("design.ui") # расположение вашего файла .ui
win.setWindowTitle('DSTFarm')
win.tableWidget.setColumnCount(3)
win.tableWidget.setRowCount(len(fds))
win.tableWidget.setHorizontalHeaderLabels(('Аккаунт', 'Активен','Выполнено'))

class timer(QThread):

	def run(self):
		i=5
		while i>-1:
			win.label.setText('Автостарт через '+str(i))
			time.sleep(1)
			i-=1
		if win.label.isVisible()==True:
			start_farm()
		win.label.setVisible(False)
		win.pushButton_4.setVisible(False)

timer_inst=timer()	
timer_inst.start()
def add_progress(num,col):
	data_acc_progres[num]=col
	progress[num].setValue(data_acc_progres[num])
	


def change_check(num):
    data_acc_check[num]=(cb[num].isChecked())

def create_check(num):
    cb.append(QCheckBox()) 
    cb[num].stateChanged.connect(lambda:change_check(num))

def create_progress(num):
    progress.append(QtWidgets.QProgressBar()) 
    progress[num].setRange(0,100)
    progress[num].setAlignment(Qt.AlignVCenter)
    progress[num].setValue(data_acc_progres[num])

line = 0
for maf in fds:
	if maf.endswith(('.maFile')):
	    cellinfo = QTableWidgetItem(data_acc_name[line])
	    win.tableWidget.setItem(line, 0, cellinfo)
	    create_check(line)
	    if data_acc_check[line]==True:
	        cb[line].toggle()
	    win.tableWidget.setCellWidget(line, 1, cb[line])
	    create_progress(line)
	    win.tableWidget.setCellWidget(line, 2, progress[line])
	    line += 1
win.pushButton.clicked.connect(lambda:clear_check())
win.pushButton_2.clicked.connect(lambda:all_check())
win.pushButton_3.clicked.connect(lambda:start_farm())
win.pushButton_4.clicked.connect(lambda:autos(False))
def autos(param):
	win.label.setVisible(param)
	win.pushButton_4.setVisible(param)
def clear_check():
    print ("clear_check")
    line = 0
    for maf in fds:
        data_acc_check[line]=False
        cb[line].setChecked(data_acc_check[line])
        line += 1

def all_check():
    print ("all_check")
    line = 0
    for maf in fds:
        data_acc_check[line]=True
        cb[line].setChecked(data_acc_check[line])
        line += 1

def start_farm():
	win.pushButton_3.setEnabled(False)
	StartFarm_inst.start()
class StartFarm(QThread):
	def __init__(self,parent=None):
		super(StartFarm,self).__init__(parent)

	def run(self):
		def runSteam(login, pswd, shared_s,line):
			add_progress(line,10)
			print(u'Запускаем Steam '+login)
			app = Application(backend="uia").start("C:/Program Files (x86)/Steam/steam.exe -silent -login %s %s" % (login, pswd), timeout=30)
			if app.Steam.wait('visible', timeout=20):
				print('Steam run')
				add_progress(line,20)
			if app.Steam.window(title_re=".*Guard").wait('visible', timeout=30):
				print('Steam Guard window opened')
				add_progress(line,30)
			try:
				app.Steam.window(title_re=".*Guard").set_focus()
				add_progress(line,35)
			except:
				time.sleep(2)
				app.Steam.window(title_re=".*Guard").set_focus()
				add_progress(line,35)
			time.sleep(0.3)
			app.Steam.window(title_re=".*Guard").type_keys('%s{ENTER}' % Steam2FA.generate_twofactor_code('%s' % shared_s))
			add_progress(line,40)
			time.sleep(5)
			
		def runDst(line):
			app = Application(backend="win32").start("C:/Program Files (x86)/Steam/Steam.exe -applaunch 322330", timeout=30)
			add_progress(line,50)
			time.sleep(22)
			add_progress(line,70)
			app = Application().connect(title_re="Don't Starve Together", timeout=20)
			try:
				app.window(best_match="Don't Starve Together").set_focus()
				add_progress(line,80)
			except:
				time.sleep(5)
				app.window(best_match="Don't Starve Together").set_focus()
				add_progress(line,80)
			time.sleep(0.5)
			app.window(best_match="Don't Starve Together").type_keys('{LEFT}')
			time.sleep(0.5)
			app.window(best_match="Don't Starve Together").type_keys('{ENTER}')
			time.sleep(0.5)
			app.window(best_match="Don't Starve Together").type_keys('{ENTER}')
			add_progress(line,90)
			time.sleep(8)
			app.window(best_match="Don't Starve Together").type_keys('{ENTER}')
			add_progress(line,99)
			time.sleep(2)
			dstKill()
			time.sleep(2)
			steamKill()
			time.sleep(3)
			
		def pkill (process_name):
		    try:
		        killed = os.system('tskill ' + process_name)
		    except Exception as e:
		        killed = 0
		    return killed

		def dstKill():
			pkill('dontstarve_steam')

		def steamKill():
			pkill('steam')

		dstKill()
		time.sleep(1)
		steamKill()
		time.sleep(1)
		line = 0
		for maf in fds:
			print(line)
			if maf.endswith(('.maFile')) and data_acc_check[line]==True: 
				with open('./maFiles/'+str(maf), "r") as read_file:
					data = json.load(read_file)
					runSteam(data["account_name"],var.Pass[data["account_name"]],data["shared_secret"],line)
					runDst(line)
					line += 1
			else:
				line += 1
		win.pushButton_3.setEnabled(True)
StartFarm_inst=StartFarm()
win.show()

sys.exit(app.exec())
