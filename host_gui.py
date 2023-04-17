from ctypes import alignment
import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui

class HostGui(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()


        self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]

        self.button = QtWidgets.QPushButton("Click me!")
        self.text = QtWidgets.QLabel("Hello World",
                                     alignment=QtCore.Qt.AlignCenter)

        # widgets for specifying the central server's host
        csLabel = QtWidgets.QLabel('Server HostName:')
        csHostName = QtWidgets.QLineEdit()
        csButton = QtWidgets.QPushButton('Connect')

        self.connTop = QtWidgets.QWidget()
        self.connTopLayout = QtWidgets.QHBoxLayout()
        self.connTopLayout.addWidget(csLabel)
        self.connTopLayout.addWidget(csHostName)
        self.connTopLayout.addWidget(csButton)
        self.connTop.setLayout(self.connTopLayout)

        #widgets for taking in user information
        uiUserLabel = QtWidgets.QLabel('Username')
        uiUserName = QtWidgets.QLineEdit()
        uiHostLabel = QtWidgets.QLabel('Hostname:')
        uiHostName = QtWidgets.QLineEdit()
        uiSpeedLabel = QtWidgets.QLabel('Speed:')
        uiSpeedChoice = QtWidgets.QComboBox()
        uiSpeedChoice.addItem('Slow')
        uiSpeedChoice.addItem('Average')
        uiSpeedChoice.addItem('Fast')

        self.connBottom = QtWidgets.QWidget()
        self.connBottomLayout = QtWidgets.QHBoxLayout()
        self.connBottomLayout.addWidget(uiUserLabel)
        self.connBottomLayout.addWidget(uiUserName)
        self.connBottomLayout.addWidget(uiHostLabel)
        self.connBottomLayout.addWidget(uiHostName)
        self.connBottomLayout.addWidget(uiSpeedLabel)
        self.connBottomLayout.addWidget(uiSpeedChoice)
        self.connBottom.setLayout(self.connBottomLayout)


        self.connectionSection = QtWidgets.QWidget()
        self.connSecLayout = QtWidgets.QVBoxLayout()
        self.connSecLayout.addWidget(self.connTop)
        self.connSecLayout.addWidget(self.connBottom)
        self.connectionSection.setLayout(self.connSecLayout)


        #widgets for keyword search
        ksLabel = QtWidgets.QLabel('Keyword Search:')
        ksText = QtWidgets.QLineEdit()
        ksButton = QtWidgets.QPushButton('Search')

        self.searchTop = QtWidgets.QWidget()
        self.searchTopLayout = QtWidgets.QHBoxLayout()
        self.searchTopLayout.addWidget(ksLabel)
        self.searchTopLayout.addWidget(ksText)
        self.searchTopLayout.addWidget(ksButton)
        self.searchTop.setLayout(self.searchTopLayout)

        #widgets to display results
        ksTable = QtWidgets.QTableWidget(12, 3)
        ksTable.setHorizontalHeaderLabels(['Speed', 'Hostname', 'Filename'])

        self.searchBottom = QtWidgets.QWidget()
        self.searchBottomLayout = QtWidgets.QHBoxLayout()
        self.searchBottomLayout.addWidget(ksTable)
        self.searchBottom.setLayout(self.searchBottomLayout)

        self.searchSection = QtWidgets.QWidget()
        self.searchSecLayout = QtWidgets.QVBoxLayout()
        self.searchSecLayout.addWidget(self.searchTop)
        self.searchSecLayout.addWidget(self.searchBottom)
        self.searchSection.setLayout(self.searchSecLayout)

        ftLabel = QtWidgets.QLabel('Enter Command:')
        ftCommand = QtWidgets.QLineEdit()
        ftButton = QtWidgets.QPushButton('Execute')

        self.ftpTop = QtWidgets.QWidget()
        self.ftpTopLayout = QtWidgets.QHBoxLayout()
        self.ftpTopLayout.addWidget(ftLabel)
        self.ftpTopLayout.addWidget(ftCommand)
        self.ftpTopLayout.addWidget(ftButton)
        self.ftpTop.setLayout(self.ftpTopLayout)

        ftText = QtWidgets.QPlainTextEdit()
        self.ftpBottom = QtWidgets.QWidget()
        self.ftpBottomLayout = QtWidgets.QHBoxLayout()
        self.ftpBottomLayout.addWidget(ftText)
        self.ftpBottom.setLayout(self.ftpBottomLayout)

        self.ftpSection = QtWidgets.QWidget()
        self.ftpSecLayout = QtWidgets.QVBoxLayout()
        self.ftpSecLayout.addWidget(self.ftpTop)
        self.ftpSecLayout.addWidget(self.ftpBottom)
        self.ftpSection.setLayout(self.ftpSecLayout)

        self.hostGuiWidget = QtWidgets.QWidget(self)
        self.hostGuiLayout = QtWidgets.QVBoxLayout()
        self.hostGuiLayout.addWidget(self.connectionSection)
        self.hostGuiLayout.addWidget(self.searchSection)
        self.hostGuiLayout.addWidget(self.ftpSection)
        self.hostGuiWidget.setLayout(self.hostGuiLayout)



        # self.layout = QtWidgets.QVBoxLayout(self)
        # self.layout.addWidget(self.connectionSection)
        # self.layout.addWidget(self.text)
        # self.layout.addWidget(self.button)

        # self.button.clicked.connect(self.magic)

    # @QtCore.Slot()
    # def magic(self):
    #     self.text.setText(random.choice(self.hello))




if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    gui = HostGui()
    gui.resize(800, 600)
    gui.show()

    sys.exit(app.exec())