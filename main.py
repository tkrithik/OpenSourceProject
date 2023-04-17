import rec
import requests
import json
from cs50 import SQL
from PySide2.QtCore import *
from PySide2.QtWidgets import *
import sys
from beepy import *

db = SQL("sqlite:///inventory.db")
app = QApplication(sys.argv)


note = '''---------------------------------------
88888 for new customer
99999 to terminate bar code scan
12345, 23456, 34567 are available barcode'''

print(note)

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
    beep(sound="ping")
    QTimer.singleShot(2000, lambda : qm.done(0))
    if qm.exec_() == QMessageBox.Yes:
        print("Yes!")
    else:
        print("No!")

def promptboxred(message):
    #app = QApplication(sys.argv)
    beep(sound="error")
    qm = QMessageBox()
    #qm.setStyleSheet("QPushButton {color:red; font-family: Arial; font-size:50px;}")
    qm.setStyleSheet("QLabel{min-width:600 px; font-size: 80px; color: red;} QPushButton{ width:25px; font-size: 13px; }");

    #qm.setText("Continue?")
    qm.setText(message)
    qm.setStandardButtons(QMessageBox.Yes)
    qm.addButton(QMessageBox.No)
    qm.setDefaultButton(QMessageBox.No)
    QTimer.singleShot(2000, lambda : qm.done(0))
    if qm.exec_() == QMessageBox.Yes:
        print("Yes!")
    else:
        print("No!")

while True:

    promptbox('Next Customer')
    proceed = input('----------next customer?')

    if proceed != '88888':
        break

    promptbox('Begin Face Regonition')

    print('------begin face regonition------')
    name = rec.detect()
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

    while True:
        promptbox('Scan Barcode')
        barcode = input('---------input barcode----->')

        if barcode == '99999':
            break

        rows = db.execute("SELECT * FROM inventory WHERE barcode = ?", barcode)

        content = json.loads(rows[0]['content'])
        print(content['ingredient'])

        trigger = set(allergy_list) & set(content['ingredient'])

        if len(trigger) == 0:
            promptbox('Safe')
            print('OK')
        else:
            promptboxred('Allergy')
            print('Warning')



 