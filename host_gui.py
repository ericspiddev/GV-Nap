from nis import match
import sys
from PySide6 import QtCore, QtWidgets, QtGui
from common import recvStr, sendStr
from napster_host import NapsterHost
from threading import Thread, Event

class HostGui(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        # widgets for specifying the central server's host
        self.csHostLabel = QtWidgets.QLabel('Server HostName:')
        self.csHostName = QtWidgets.QLineEdit()
        self.csPortLabel = QtWidgets.QLabel('Port')
        self.csPortNumber = QtWidgets.QLineEdit()
        self.csButton = QtWidgets.QPushButton('Connect')
        self.csButton.clicked.connect(self.connectToCentralServer)

        self.connTop = QtWidgets.QWidget()
        self.connTopLayout = QtWidgets.QHBoxLayout()
        self.connTopLayout.addWidget(self.csHostLabel)
        self.connTopLayout.addWidget(self.csHostName)
        self.connTopLayout.addWidget(self.csPortLabel)
        self.connTopLayout.addWidget(self.csPortNumber)
        self.connTopLayout.addWidget(self.csButton)
        self.connTop.setLayout(self.connTopLayout)

        #widgets for taking in user information
        self.uiUserLabel = QtWidgets.QLabel('Username')
        self.uiUserName = QtWidgets.QLineEdit()
        self.uiHostLabel = QtWidgets.QLabel('Hostname:')
        self.uiHostName = QtWidgets.QLineEdit()
        self.uiPortLabel = QtWidgets.QLabel('Port')
        self.uiPortNum = QtWidgets.QLineEdit()
        self.uiSpeedLabel = QtWidgets.QLabel('Speed:')
        self.uiSpeedChoice = QtWidgets.QComboBox()
        self.uiSpeedChoice.addItem('Slow')
        self.uiSpeedChoice.addItem('Average')
        self.uiSpeedChoice.addItem('Fast')

        self.connBottom = QtWidgets.QWidget()
        self.connBottomLayout = QtWidgets.QHBoxLayout()
        self.connBottomLayout.addWidget(self.uiUserLabel)
        self.connBottomLayout.addWidget(self.uiUserName)
        self.connBottomLayout.addWidget(self.uiHostLabel)
        self.connBottomLayout.addWidget(self.uiHostName)
        self.connBottomLayout.addWidget(self.uiPortLabel)
        self.connBottomLayout.addWidget(self.uiPortNum)
        self.connBottomLayout.addWidget(self.uiSpeedLabel)
        self.connBottomLayout.addWidget(self.uiSpeedChoice)
        self.connBottom.setLayout(self.connBottomLayout)


        self.connectionSection = QtWidgets.QWidget()
        self.connSecLayout = QtWidgets.QVBoxLayout()
        self.connSecLayout.addWidget(self.connTop)
        self.connSecLayout.addWidget(self.connBottom)
        self.connectionSection.setLayout(self.connSecLayout)


        #widgets for keyword search
        ksLabel = QtWidgets.QLabel('Keyword Search:')
        self.ksText = QtWidgets.QLineEdit()
        ksButton = QtWidgets.QPushButton('Search')
        ksButton.clicked.connect(self.keyWordSearch)

        self.searchTop = QtWidgets.QWidget()
        self.searchTopLayout = QtWidgets.QHBoxLayout()
        self.searchTopLayout.addWidget(ksLabel)
        self.searchTopLayout.addWidget(self.ksText)
        self.searchTopLayout.addWidget(ksButton)
        self.searchTop.setLayout(self.searchTopLayout)

        #widgets to display results
        self.ksTable = QtWidgets.QTableWidget(12, 4)
        self.ksTable.setHorizontalHeaderLabels(['Filename', 'Hostname', 'Port', 'Speed'])
        ksHeaders = self.ksTable.horizontalHeader()
        ksHeaders.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.Stretch)
        ksHeaders.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.Stretch)
        ksHeaders.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        ksHeaders.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)


        self.searchBottom = QtWidgets.QWidget()
        self.searchBottomLayout = QtWidgets.QHBoxLayout()
        self.searchBottomLayout.addWidget(self.ksTable)
        self.searchBottom.setLayout(self.searchBottomLayout)

        self.searchSection = QtWidgets.QWidget()
        self.searchSecLayout = QtWidgets.QVBoxLayout()
        self.searchSecLayout.addWidget(self.searchTop)
        self.searchSecLayout.addWidget(self.searchBottom)
        self.searchSection.setLayout(self.searchSecLayout)

        ftLabel = QtWidgets.QLabel('Enter Command:')
        self.ftCommand = QtWidgets.QLineEdit()
        ftButton = QtWidgets.QPushButton('Execute')
        ftButton.clicked.connect(self.executeFtpCommand)

        self.ftpTop = QtWidgets.QWidget()
        self.ftpTopLayout = QtWidgets.QHBoxLayout()
        self.ftpTopLayout.addWidget(ftLabel)
        self.ftpTopLayout.addWidget(self.ftCommand)
        self.ftpTopLayout.addWidget(ftButton)
        self.ftpTop.setLayout(self.ftpTopLayout)

        self.ftText = QtWidgets.QPlainTextEdit()
        self.ftText.setReadOnly(True)
        self.ftpBottom = QtWidgets.QWidget()
        self.ftpBottomLayout = QtWidgets.QHBoxLayout()
        self.ftpBottomLayout.addWidget(self.ftText)
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


        self.executeEvent = Event()
        self.updateText = Event()
        self.result = ""

        self.host = NapsterHost()
        self.initFtpText()
        self.shouldExecuteFtpCommand = False

        self.clientThread = Thread(target=self.ftpClientThread)
        self.serverThread = Thread(target=self.startFtpServer)

        self.clientThread.start()
        self.serverThread.start()

    def connectToCentralServer(self):
        centralServerHostName = self.csHostName.text()
        centralServerPort = int(self.csPortNumber.text())
        userName = self.uiUserName.text()
        userHostName = self.uiHostName.text()
        userSpeedChoice = self.uiSpeedChoice.currentText()
        userPort = int(self.uiPortNum.text())
        self.host.connectToCentralServer(centralServerHostName, userName, userHostName, userSpeedChoice, centralServerPort, userPort)

    def executeFtpCommand(self):
        self.executeEvent.set()
        self.updateText.wait()
        self.ftText.appendPlainText(self.result)
        self.updateText.clear()

    def startFtpServer(self):
        self.host.startServer()

    def ftpClientThread(self):
        while True:
            self.executeEvent.wait()
            userCmd = self.ftCommand.text() + "\n"
            self.result = self.host.runFtpClientCmd(userCmd)
            self.updateText.set()
            self.executeEvent.clear()

    def keyWordSearch(self):
        self.ksTable.setRowCount(0)
        self.ksTable.setRowCount(12)
        searchStr = self.ksText.text() + "\n"
        sendStr(self.host.centralServerSocket, searchStr)
        matches = recvStr(self.host.centralServerSocket)
        print(matches)
        matches = matches.rsplit('\n')
        matches = int(matches[0])
        for i in range(matches):
            fileLine = recvStr(self.host.centralServerSocket)
            fileLine = fileLine.rsplit('\n')
            splitLines = fileLine[0].split(',')
            self.ksTable.setItem(i, 0,  QtWidgets.QTableWidgetItem(splitLines[0]))
            self.ksTable.setItem(i, 1, QtWidgets.QTableWidgetItem(splitLines[2]))
            self.ksTable.setItem(i, 2, QtWidgets.QTableWidgetItem(splitLines[3]))

            print(fileLine)
    def initFtpText(self):
        self.ftText.appendPlainText("Welcome to FTP Client!\n")

    # @QtCore.Slot()
    # def magic(self):
    #     self.text.setText(random.choice(self.hello))

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    gui = HostGui()
    gui.resize(900, 700)
    gui.show()
    app.exec()
    print("sending breakout string")
    sendStr(gui.host.centralServerSocket, "testitoutbreakstr\n")


