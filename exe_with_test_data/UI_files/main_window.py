# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import UI_files.resources.resources_rc


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(962, 600)
        MainWindow.setMinimumSize(QtCore.QSize(0, 0))
        MainWindow.setStyleSheet("#centralwidget{\n"
"    background-color: rgba(30, 35, 50, 255);\n"
"}\n"
"\n"
"QPushButton{\n"
"    border: none;\n"
"    border-radius: 10px;\n"
"    padding: 5px, 5px;\n"
"    padding-right: 5px;\n"
"    padding-left: 5px;\n"
"\n"
"    \n"
"    background-color: transparent;\n"
"    color: rgb(255, 255, 255);\n"
"    \n"
"    font: 63 12pt \"Bahnschrift SemiBold SemiConden\";\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: rgba(255, 255, 255, 30);\n"
"    color: rgb(200, 200, 200);\n"
"\n"
"    font: 63 12pt \"Bahnschrift SemiBold SemiConden\";\n"
"}\n"
"\n"
"QLabel{\n"
"    color: rgb(255, 255, 255);\n"
"    font: 63 12pt \"Bahnschrift SemiBold SemiConden\";\n"
"}\n"
"\n"
" QComboBox{\n"
"    border: 2px solid rgb(170, 0, 255);\n"
"    border-radius: 5px;\n"
"    padding: 5px, 5px;\n"
"    padding-right: 5px;\n"
"    padding-left: 5px;\n"
"\n"
"    \n"
"    background-color: rgba(255, 255, 255, 100);\n"
"    color: rgb(255, 255, 255);\n"
"    \n"
"    font: 63 12pt \"Bahnschrift SemiBold SemiConden\";\n"
"}\n"
"\n"
"QComboBox:editable {\n"
"    border: 0px;\n"
"    color: rgb(85, 255, 255);\n"
"}\n"
"\n"
"QComboBox QAbstractItemView {\n"
"    border: 1px solid rgb(85, 255, 255);\n"
"}\n"
"\n"
"QComboBox::drop-down{\n"
"}\n"
"\n"
"")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.header = QtWidgets.QWidget(self.centralwidget)
        self.header.setMinimumSize(QtCore.QSize(0, 0))
        self.header.setObjectName("header")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.header)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame_2 = QtWidgets.QFrame(self.header)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout_3.setContentsMargins(10, 2, 10, 2)
        self.horizontalLayout_3.setSpacing(10)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtWidgets.QLabel(self.frame_2)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label, 0, QtCore.Qt.AlignLeft)
        self.comboBox_for_language = QtWidgets.QComboBox(self.frame_2)
        self.comboBox_for_language.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.comboBox_for_language.setObjectName("comboBox_for_language")
        self.horizontalLayout_3.addWidget(self.comboBox_for_language)
        self.comboBox_for_translation_lang = QtWidgets.QComboBox(self.frame_2)
        self.comboBox_for_translation_lang.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.comboBox_for_translation_lang.setStyleSheet("")
        self.comboBox_for_translation_lang.setObjectName("comboBox_for_translation_lang")
        self.horizontalLayout_3.addWidget(self.comboBox_for_translation_lang)
        self.horizontalLayout.addWidget(self.frame_2, 0, QtCore.Qt.AlignLeft)
        self.frame = QtWidgets.QFrame(self.header)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout.addWidget(self.frame, 0, QtCore.Qt.AlignHCenter)
        self.frame_4 = QtWidgets.QFrame(self.header)
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.frame_4)
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.horizontalLayout.addWidget(self.frame_4, 0, QtCore.Qt.AlignRight)
        self.verticalLayout.addWidget(self.header)
        self.mainBody = QtWidgets.QWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mainBody.sizePolicy().hasHeightForWidth())
        self.mainBody.setSizePolicy(sizePolicy)
        self.mainBody.setObjectName("mainBody")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.mainBody)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.stackedWidget = QtWidgets.QStackedWidget(self.mainBody)
        self.stackedWidget.setStyleSheet("background-color: transparent;")
        self.stackedWidget.setObjectName("stackedWidget")
        self.verticalLayout_2.addWidget(self.stackedWidget)
        self.verticalLayout.addWidget(self.mainBody)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 962, 24))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt; font-weight:600;\">ForLang</span></p></body></html>"))