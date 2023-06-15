# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI_Window.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1101, 779)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.graphicsView_QuiverCanvas = PlotWidget(self.centralwidget)
        self.graphicsView_QuiverCanvas.setGeometry(QtCore.QRect(5, 5, 700, 700))
        self.graphicsView_QuiverCanvas.setObjectName("graphicsView_QuiverCanvas")
        self.pushButton_DeleteQuiver = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_DeleteQuiver.setGeometry(QtCore.QRect(300, 705, 113, 32))
        self.pushButton_DeleteQuiver.setObjectName("pushButton_DeleteQuiver")
        self.radioButton_DrawQuiver = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_DrawQuiver.setGeometry(QtCore.QRect(720, 20, 200, 20))
        self.radioButton_DrawQuiver.setChecked(True)
        self.radioButton_DrawQuiver.setObjectName("radioButton_DrawQuiver")
        self.textBrowser_HowDoYouWritePaths = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_HowDoYouWritePaths.setGeometry(QtCore.QRect(85, 100, 541, 91))
        self.textBrowser_HowDoYouWritePaths.setObjectName("textBrowser_HowDoYouWritePaths")
        self.pushButton_PathsLeftToRight = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_PathsLeftToRight.setGeometry(QtCore.QRect(150, 190, 181, 41))
        self.pushButton_PathsLeftToRight.setObjectName("pushButton_PathsLeftToRight")
        self.pushButton_PathsRightToLeft = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_PathsRightToLeft.setGeometry(QtCore.QRect(370, 190, 181, 41))
        self.pushButton_PathsRightToLeft.setObjectName("pushButton_PathsRightToLeft")
        self.listWidget_RecordedPaths = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget_RecordedPaths.setGeometry(QtCore.QRect(710, 110, 380, 190))
        self.listWidget_RecordedPaths.setEditTriggers(QtWidgets.QAbstractItemView.AnyKeyPressed|QtWidgets.QAbstractItemView.DoubleClicked|QtWidgets.QAbstractItemView.EditKeyPressed)
        self.listWidget_RecordedPaths.setAlternatingRowColors(True)
        self.listWidget_RecordedPaths.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.listWidget_RecordedPaths.setObjectName("listWidget_RecordedPaths")
        self.pushButton_AddPathToFormRelation = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_AddPathToFormRelation.setGeometry(QtCore.QRect(710, 310, 125, 32))
        self.pushButton_AddPathToFormRelation.setObjectName("pushButton_AddPathToFormRelation")
        self.radioButton_RecordPathsAndRelations = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_RecordPathsAndRelations.setGeometry(QtCore.QRect(720, 50, 191, 20))
        self.radioButton_RecordPathsAndRelations.setObjectName("radioButton_RecordPathsAndRelations")
        self.listWidget_Coefficient = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget_Coefficient.setGeometry(QtCore.QRect(710, 370, 80, 192))
        self.listWidget_Coefficient.setEditTriggers(QtWidgets.QAbstractItemView.SelectedClicked)
        self.listWidget_Coefficient.setObjectName("listWidget_Coefficient")
        self.label_Coefficient = QtWidgets.QLabel(self.centralwidget)
        self.label_Coefficient.setGeometry(QtCore.QRect(720, 350, 70, 16))
        self.label_Coefficient.setObjectName("label_Coefficient")
        self.label_Path = QtWidgets.QLabel(self.centralwidget)
        self.label_Path.setGeometry(QtCore.QRect(810, 350, 31, 16))
        self.label_Path.setObjectName("label_Path")
        self.listWidget_Path = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget_Path.setGeometry(QtCore.QRect(800, 370, 291, 192))
        self.listWidget_Path.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.listWidget_Path.setObjectName("listWidget_Path")
        self.label_RecordedPaths = QtWidgets.QLabel(self.centralwidget)
        self.label_RecordedPaths.setGeometry(QtCore.QRect(720, 90, 101, 16))
        self.label_RecordedPaths.setObjectName("label_RecordedPaths")
        self.pushButton_deleteSelectedRecordedPaths = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_deleteSelectedRecordedPaths.setGeometry(QtCore.QRect(840, 310, 125, 32))
        self.pushButton_deleteSelectedRecordedPaths.setObjectName("pushButton_deleteSelectedRecordedPaths")
        self.pushButton_deleteAllSelectedPaths = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_deleteAllSelectedPaths.setGeometry(QtCore.QRect(970, 310, 125, 32))
        self.pushButton_deleteAllSelectedPaths.setObjectName("pushButton_deleteAllSelectedPaths")
        self.pushButton_deleteSelectedRowInRelationBeingFormed = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_deleteSelectedRowInRelationBeingFormed.setGeometry(QtCore.QRect(840, 570, 125, 32))
        self.pushButton_deleteSelectedRowInRelationBeingFormed.setObjectName("pushButton_deleteSelectedRowInRelationBeingFormed")
        self.pushButton_deleteAllRowsFromRelationBeingFormed = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_deleteAllRowsFromRelationBeingFormed.setGeometry(QtCore.QRect(970, 570, 125, 32))
        self.pushButton_deleteAllRowsFromRelationBeingFormed.setObjectName("pushButton_deleteAllRowsFromRelationBeingFormed")
        self.pushButton_formRelation = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_formRelation.setGeometry(QtCore.QRect(710, 570, 125, 32))
        self.pushButton_formRelation.setObjectName("pushButton_formRelation")
 #       MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1101, 22))
        self.menubar.setObjectName("menubar")
    #    MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
     #   MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.pushButton_PathsLeftToRight.clicked.connect(self.pushButton_PathsLeftToRight.close)
        self.pushButton_PathsLeftToRight.clicked.connect(self.pushButton_PathsRightToLeft.close)
        self.pushButton_PathsRightToLeft.clicked.connect(self.pushButton_PathsLeftToRight.close)
        self.pushButton_PathsRightToLeft.clicked.connect(self.pushButton_PathsRightToLeft.close)
        self.pushButton_PathsRightToLeft.clicked.connect(self.textBrowser_HowDoYouWritePaths.close)
        self.pushButton_PathsLeftToRight.clicked.connect(self.textBrowser_HowDoYouWritePaths.close)
        self.pushButton_deleteAllSelectedPaths.clicked.connect(self.listWidget_RecordedPaths.clear)
        self.pushButton_deleteAllRowsFromRelationBeingFormed.clicked.connect(self.listWidget_Path.clear)
        self.pushButton_deleteAllRowsFromRelationBeingFormed.clicked.connect(self.listWidget_Coefficient.clear)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_DeleteQuiver.setText(_translate("MainWindow", "Delete quiver"))
        self.radioButton_DrawQuiver.setText(_translate("MainWindow", "Draw quiver"))
        self.textBrowser_HowDoYouWritePaths.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'.AppleSystemUIFont\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'.SF NS Text\'; font-size:24pt;\">How do you write paths?</span></p></body></html>"))
        self.pushButton_PathsLeftToRight.setText(_translate("MainWindow", "From left to right"))
        self.pushButton_PathsRightToLeft.setText(_translate("MainWindow", "From right to left"))
        self.pushButton_AddPathToFormRelation.setText(_translate("MainWindow", "Pass down sel"))
        self.radioButton_RecordPathsAndRelations.setText(_translate("MainWindow", "Record paths and relations"))
        self.label_Coefficient.setText(_translate("MainWindow", "Coefficient"))
        self.label_Path.setText(_translate("MainWindow", "Path"))
        self.label_RecordedPaths.setText(_translate("MainWindow", "Recorded paths"))
        self.pushButton_deleteSelectedRecordedPaths.setText(_translate("MainWindow", "Delete sel"))
        self.pushButton_deleteAllSelectedPaths.setText(_translate("MainWindow", "Delete all"))
        self.pushButton_deleteSelectedRowInRelationBeingFormed.setText(_translate("MainWindow", "Delete sel"))
        self.pushButton_deleteAllRowsFromRelationBeingFormed.setText(_translate("MainWindow", "Delete all"))
        self.pushButton_formRelation.setText(_translate("MainWindow", "Form relation"))

from pyqtgraph import PlotWidget

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

