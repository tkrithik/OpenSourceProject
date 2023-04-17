#import rec
import scan_app
import requests
import json
from cs50 import SQL
from PySide6.QtCore import *
from PySide6.QtWidgets import *
import sys
from beepy import *
import scan_object
import faceclassification

db = SQL("sqlite:///inventory.db")

app = QApplication(sys.argv)


# note = '''---------------------------------------
# 88888 for new customer
# 99999 to terminate bar code scan
# 12345, 23456, 34567 are available barcode
# '''

# print(note)

def promptbox(message):
    #app = QApplication(sys.argv)
    qm = QMessageBox()
    #qm.setStyleSheet("QPushButton {color:red; font-family: Arial; font-size:50px;}")
    qm.setStyleSheet("QLabel{min-width:600 px; font-size: 80px;} QPushButton{ width:25px; font-size: 13px; }");

    #qm.setText("Continue?")
    qm.setText(message)
    qm.setStandardButtons(QMessageBox.Yes)
    qm.addButton(QMessageBox.No)
    qm.setDefaultButton(QMessageBox.No)
    #beep(sound="ping")
    #QTimer.singleShot(80000, lambda : qm.done(0))
    if qm.exec() == QMessageBox.Yes:
        return('y')
    else:
        return('n')

def promptboxred(message):
    #app = QApplication(sys.argv)
    #beep(sound="error")
    qm = QMessageBox()
    #qm.setStyleSheet("QPushButton {color:red; font-family: Arial; font-size:50px;}")
    qm.setStyleSheet("QLabel{min-width:600 px; font-size: 80px; color: red;} QPushButton{ width:25px; font-size: 13px; }");

    #qm.setText("Continue?")
    qm.setText(message)
    qm.setStandardButtons(QMessageBox.Yes)
    qm.addButton(QMessageBox.No)
    qm.setDefaultButton(QMessageBox.No)
    #QTimer.singleShot(800000, lambda : qm.done(0))
    if qm.exec() == QMessageBox.Yes:
        return("y")
    else:
        return("n")
while True:
    #proceed = input('----------next customer? (y/n)')
    customerproceed = promptbox("Next customer?")
    if customerproceed != 'y':
        break
    faceproceed = promptbox('Begin Face Recognition?')
    if faceproceed != 'y':
          break
    #name = rec.detect()
    name = faceclassification.detect()
    if name == "n":
        break
    if len(name) != 0:
        print('---------regonized name is ---->', name)
    response = requests.post(
        'http://127.0.0.1:5000/query',
        data = json.dumps({'username': name}),
        headers = {"Content-Type": "application/json"} )
    print(response)

    response = requests.get('http://127.0.0.1:5000/query')
    res = response.json()
    print('---------personal allergy------>', res)

    allergy_list = res['allergy']
    print(allergy_list)

    while True:
        objectproceed = promptbox('Scan object?')
        if objectproceed != 'y':
            break
        #food = scan_object.scan()
        food = scan_app.scan()
        trigger = []
        if food != None:
            #print(allergy_list)
            #print(food)
            trigger = set(allergy_list) & set(food['ingredients'])

        if len(trigger) == 0:
            promptbox('Safe')
            print('OK')
        else:
            promptboxred('Allergy Detected')
            print('Warning')

        proceed = promptbox("Next object?")
        if proceed != 'y':
            break


 
