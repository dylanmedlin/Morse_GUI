from PyQt5 import QtCore, QtGui, QtWidgets
import RPi.GPIO as GPIO
import time

LED = 8
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED, GPIO.OUT)

# Dictionary representing the morse code chart
MORSE_CODE_DICT = { 'A':'.-', 'B':'-...',
                    'C':'-.-.', 'D':'-..', 'E':'.',
                    'F':'..-.', 'G':'--.', 'H':'....',
                    'I':'..', 'J':'.---', 'K':'-.-',
                    'L':'.-..', 'M':'--', 'N':'-.',
                    'O':'---', 'P':'.--.', 'Q':'--.-',
                    'R':'.-.', 'S':'...', 'T':'-',
                    'U':'..-', 'V':'...-', 'W':'.--',
                    'X':'-..-', 'Y':'-.--', 'Z':'--..',
                    '1':'.----', '2':'..---', '3':'...--',
                    '4':'....-', '5':'.....', '6':'-....',
                    '7':'--...', '8':'---..', '9':'----.',
                    '0':'-----', ', ':'--..--', '.':'.-.-.-',
                    '?':'..--..', '/':'-..-.', '-':'-....-',
                    '(':'-.--.', ')':'-.--.-'}

SHORT = 0.5
LONG = SHORT * 3

def convertToMorse(message):
    message = message.upper()
    result = ''
    for letter in message:
        if letter != ' ':
            result += MORSE_CODE_DICT[letter] + ' '
        else:
            result += ' '
    return result

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(360, 150)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(90, 30, 180, 25))
        self.lineEdit.setText("")
        self.lineEdit.setMaxLength(12)
        self.lineEdit.setCursorPosition(0)
        self.lineEdit.setClearButtonEnabled(False)
        self.lineEdit.setObjectName("lineEdit")

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(90, 80, 180, 25))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.blinkMorse)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Blink Morse Code"))
        self.lineEdit.setPlaceholderText(_translate("MainWindow", "Enter a word..."))
        self.pushButton.setText(_translate("MainWindow", "Start Morse Code"))

    def blinkMorse(self):
        morse = convertToMorse(self.lineEdit.text())
        print(morse)
        for symbol in morse:
            if symbol == '.':
                GPIO.output(LED, GPIO.HIGH)
                time.sleep(SHORT)
                GPIO.output(LED, GPIO.LOW)
                time.sleep(SHORT)
            elif symbol == '-':
                GPIO.output(LED, GPIO.HIGH)
                time.sleep(LONG)
                GPIO.output(LED, GPIO.LOW)
                time.sleep(SHORT) 
            elif symbol == ' ':
                time.sleep(LONG)

if __name__ == "__main__":
    try:
        import sys
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)
        MainWindow.show()
        sys.exit(app.exec_())
    finally:
        GPIO.cleanup()