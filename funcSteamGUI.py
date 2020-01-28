# -*- coding: utf-8 -*-
from Steam2FA import *
import sys, traceback, os
import time
import psutil
import win32api, win32con, win32gui, win32ui
from pywinauto.application import Application

def runSteam(login, pswd, shared_s):
	print(u'Запускаем Steam '+login)
	app = Application(backend="uia").start("C:/Program Files (x86)/Steam/steam.exe -silent -login %s %s" % (login, pswd), timeout=30)
	if app.Steam.wait('visible', timeout=20):
		print('Steam run')
	if app.Steam.window(title_re=".*Guard").wait('visible', timeout=30):
		print('Steam Guard window opened')
	try:
		app.Steam.window(title_re=".*Guard").set_focus()
	except:
		time.sleep(2)
		app.Steam.window(title_re=".*Guard").set_focus()

	time.sleep(0.3)
	app.Steam.window(title_re=".*Guard").type_keys('%s{ENTER}' % generate_twofactor_code('%s' % shared_s))
	time.sleep(5)
def runDst():

	app = Application(backend="win32").start("C:/Program Files (x86)/Steam/Steam.exe -applaunch 322330", timeout=30)
	time.sleep(25)
	app = Application().connect(title_re="Don't Starve Together", timeout=20)
	try:
		app.window(best_match="Don't Starve Together").set_focus()
	except:
		time.sleep(5)
		app.window(best_match="Don't Starve Together").set_focus()
	time.sleep(0.5)
	app.window(best_match="Don't Starve Together").type_keys('{LEFT}')
	time.sleep(0.5)
	app.window(best_match="Don't Starve Together").type_keys('{ENTER}')
	time.sleep(0.5)
	app.window(best_match="Don't Starve Together").type_keys('{ENTER}')
	time.sleep(8)
	app.window(best_match="Don't Starve Together").type_keys('{ENTER}')
	time.sleep(3)
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



