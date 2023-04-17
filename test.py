import sys

from PySide6.QtCore import *
from PySide6.QtWidgets import *


def promptbox(message):
    app = QApplication(sys.argv)

    qm = QMessageBox()
    #qm.setStyleSheet("QPushButton {color:red; font-family: Arial; font-size:50px;}")
    qm.setStyleSheet("QLabel{min-width:600 px; font-size: 80px; color: red;} QPushButton{ width:25px; font-size: 13px; }");

    #qm.setText("Continue?")
    qm.setText(message)
    qm.setStandardButtons(QMessageBox.Yes)
    qm.addButton(QMessageBox.No)
    qm.setDefaultButton(QMessageBox.No)
    QTimer.singleShot(40000, lambda : qm.done(0))
    if qm.exec() == QMessageBox.Yes:
        print("Yes!")
    else:
        print("No!")

promptbox("try")
