# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'GUI.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QDoubleSpinBox, QHBoxLayout,
    QLabel, QLineEdit, QMainWindow, QPlainTextEdit,
    QProgressBar, QPushButton, QSizePolicy, QSpinBox,
    QTabWidget, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(349, 506)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setAutoFillBackground(False)
        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(6, 8, 341, 491))
        self.centralLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.centralLayout.setObjectName(u"centralLayout")
        self.centralLayout.setContentsMargins(0, 0, 0, 0)
        self.tabWidget = QTabWidget(self.verticalLayoutWidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab_queuer = QWidget()
        self.tab_queuer.setObjectName(u"tab_queuer")
        self.layoutWidget_2 = QWidget(self.tab_queuer)
        self.layoutWidget_2.setObjectName(u"layoutWidget_2")
        self.layoutWidget_2.setGeometry(QRect(2, -1, 331, 461))
        self.lista_input_queuer = QVBoxLayout(self.layoutWidget_2)
        self.lista_input_queuer.setSpacing(10)
        self.lista_input_queuer.setObjectName(u"lista_input_queuer")
        self.lista_input_queuer.setContentsMargins(2, 10, 4, 2)
        self.layout_cartella_input = QHBoxLayout()
        self.layout_cartella_input.setObjectName(u"layout_cartella_input")
        self.label_cartella_input = QLabel(self.layoutWidget_2)
        self.label_cartella_input.setObjectName(u"label_cartella_input")

        self.layout_cartella_input.addWidget(self.label_cartella_input)

        self.lineEdit_cartella_input = QLineEdit(self.layoutWidget_2)
        self.lineEdit_cartella_input.setObjectName(u"lineEdit_cartella_input")

        self.layout_cartella_input.addWidget(self.lineEdit_cartella_input)

        self.pushButton_scegli_input = QPushButton(self.layoutWidget_2)
        self.pushButton_scegli_input.setObjectName(u"pushButton_scegli_input")

        self.layout_cartella_input.addWidget(self.pushButton_scegli_input)


        self.lista_input_queuer.addLayout(self.layout_cartella_input)

        self.layout_cartella_output = QHBoxLayout()
        self.layout_cartella_output.setObjectName(u"layout_cartella_output")
        self.label_cartella_output = QLabel(self.layoutWidget_2)
        self.label_cartella_output.setObjectName(u"label_cartella_output")

        self.layout_cartella_output.addWidget(self.label_cartella_output)

        self.lineEdit_cartella_output = QLineEdit(self.layoutWidget_2)
        self.lineEdit_cartella_output.setObjectName(u"lineEdit_cartella_output")

        self.layout_cartella_output.addWidget(self.lineEdit_cartella_output)

        self.pushButton_scegli_output = QPushButton(self.layoutWidget_2)
        self.pushButton_scegli_output.setObjectName(u"pushButton_scegli_output")

        self.layout_cartella_output.addWidget(self.pushButton_scegli_output)


        self.lista_input_queuer.addLayout(self.layout_cartella_output)

        self.layout_posizione_naso = QHBoxLayout()
        self.layout_posizione_naso.setObjectName(u"layout_posizione_naso")
        self.label_posizione_naso = QLabel(self.layoutWidget_2)
        self.label_posizione_naso.setObjectName(u"label_posizione_naso")

        self.layout_posizione_naso.addWidget(self.label_posizione_naso)

        self.lineEdit_posizione_naso = QLineEdit(self.layoutWidget_2)
        self.lineEdit_posizione_naso.setObjectName(u"lineEdit_posizione_naso")

        self.layout_posizione_naso.addWidget(self.lineEdit_posizione_naso)


        self.lista_input_queuer.addLayout(self.layout_posizione_naso)

        self.layout_anno = QHBoxLayout()
        self.layout_anno.setObjectName(u"layout_anno")
        self.label_anno = QLabel(self.layoutWidget_2)
        self.label_anno.setObjectName(u"label_anno")
        self.label_anno.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.layout_anno.addWidget(self.label_anno)

        self.spinBox_anno = QSpinBox(self.layoutWidget_2)
        self.spinBox_anno.setObjectName(u"spinBox_anno")

        self.layout_anno.addWidget(self.spinBox_anno)


        self.lista_input_queuer.addLayout(self.layout_anno)

        self.layout_stampa_meta = QHBoxLayout()
        self.layout_stampa_meta.setObjectName(u"layout_stampa_meta")
        self.checkBox_stampa_meta = QCheckBox(self.layoutWidget_2)
        self.checkBox_stampa_meta.setObjectName(u"checkBox_stampa_meta")

        self.layout_stampa_meta.addWidget(self.checkBox_stampa_meta, 0, Qt.AlignmentFlag.AlignHCenter)


        self.lista_input_queuer.addLayout(self.layout_stampa_meta)

        self.bottone_start_queuer = QPushButton(self.layoutWidget_2)
        self.bottone_start_queuer.setObjectName(u"bottone_start_queuer")
        self.bottone_start_queuer.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

        self.lista_input_queuer.addWidget(self.bottone_start_queuer)

        self.progressBar_queuer = QProgressBar(self.layoutWidget_2)
        self.progressBar_queuer.setObjectName(u"progressBar_queuer")
        self.progressBar_queuer.setValue(0)

        self.lista_input_queuer.addWidget(self.progressBar_queuer)

        self.plainTextEdit_queuer = QPlainTextEdit(self.layoutWidget_2)
        self.plainTextEdit_queuer.setObjectName(u"plainTextEdit_queuer")

        self.lista_input_queuer.addWidget(self.plainTextEdit_queuer)

        self.tabWidget.addTab(self.tab_queuer, "")
        self.tab_analisi = QWidget()
        self.tab_analisi.setObjectName(u"tab_analisi")
        self.layoutWidget = QWidget(self.tab_analisi)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(0, 0, 331, 461))
        self.lista_input_analisi = QVBoxLayout(self.layoutWidget)
        self.lista_input_analisi.setSpacing(10)
        self.lista_input_analisi.setObjectName(u"lista_input_analisi")
        self.lista_input_analisi.setContentsMargins(2, 10, 4, 2)
        self.layout_analisi_cartella_input = QHBoxLayout()
        self.layout_analisi_cartella_input.setObjectName(u"layout_analisi_cartella_input")
        self.label_analisi_cartella_input = QLabel(self.layoutWidget)
        self.label_analisi_cartella_input.setObjectName(u"label_analisi_cartella_input")

        self.layout_analisi_cartella_input.addWidget(self.label_analisi_cartella_input)

        self.lineEdit_analisi_cartella_input = QLineEdit(self.layoutWidget)
        self.lineEdit_analisi_cartella_input.setObjectName(u"lineEdit_analisi_cartella_input")

        self.layout_analisi_cartella_input.addWidget(self.lineEdit_analisi_cartella_input)

        self.pushButton_analisi_scegli_input = QPushButton(self.layoutWidget)
        self.pushButton_analisi_scegli_input.setObjectName(u"pushButton_analisi_scegli_input")

        self.layout_analisi_cartella_input.addWidget(self.pushButton_analisi_scegli_input)


        self.lista_input_analisi.addLayout(self.layout_analisi_cartella_input)

        self.layout_analisi_cartella_meteo = QHBoxLayout()
        self.layout_analisi_cartella_meteo.setObjectName(u"layout_analisi_cartella_meteo")
        self.label_analisi_cartella_meteo = QLabel(self.layoutWidget)
        self.label_analisi_cartella_meteo.setObjectName(u"label_analisi_cartella_meteo")

        self.layout_analisi_cartella_meteo.addWidget(self.label_analisi_cartella_meteo)

        self.lineEdit_analisi_cartella_meteo = QLineEdit(self.layoutWidget)
        self.lineEdit_analisi_cartella_meteo.setObjectName(u"lineEdit_analisi_cartella_meteo")

        self.layout_analisi_cartella_meteo.addWidget(self.lineEdit_analisi_cartella_meteo)

        self.pushButton_analisi_cartella_meteo = QPushButton(self.layoutWidget)
        self.pushButton_analisi_cartella_meteo.setObjectName(u"pushButton_analisi_cartella_meteo")

        self.layout_analisi_cartella_meteo.addWidget(self.pushButton_analisi_cartella_meteo)


        self.lista_input_analisi.addLayout(self.layout_analisi_cartella_meteo)

        self.layout_analisi_file_interruz = QHBoxLayout()
        self.layout_analisi_file_interruz.setObjectName(u"layout_analisi_file_interruz")
        self.label_analisi_file_interruz = QLabel(self.layoutWidget)
        self.label_analisi_file_interruz.setObjectName(u"label_analisi_file_interruz")

        self.layout_analisi_file_interruz.addWidget(self.label_analisi_file_interruz)

        self.lineEdit_analisi_file_interruz = QLineEdit(self.layoutWidget)
        self.lineEdit_analisi_file_interruz.setObjectName(u"lineEdit_analisi_file_interruz")

        self.layout_analisi_file_interruz.addWidget(self.lineEdit_analisi_file_interruz)

        self.pushButton_analisi_scegli_file_interruz = QPushButton(self.layoutWidget)
        self.pushButton_analisi_scegli_file_interruz.setObjectName(u"pushButton_analisi_scegli_file_interruz")

        self.layout_analisi_file_interruz.addWidget(self.pushButton_analisi_scegli_file_interruz)


        self.lista_input_analisi.addLayout(self.layout_analisi_file_interruz)

        self.layout_analisi_foglio_interruz = QHBoxLayout()
        self.layout_analisi_foglio_interruz.setObjectName(u"layout_analisi_foglio_interruz")
        self.label_analisi_foglio_interruz = QLabel(self.layoutWidget)
        self.label_analisi_foglio_interruz.setObjectName(u"label_analisi_foglio_interruz")

        self.layout_analisi_foglio_interruz.addWidget(self.label_analisi_foglio_interruz)

        self.lineEdit_analisi_foglio_interruz = QLineEdit(self.layoutWidget)
        self.lineEdit_analisi_foglio_interruz.setObjectName(u"lineEdit_analisi_foglio_interruz")

        self.layout_analisi_foglio_interruz.addWidget(self.lineEdit_analisi_foglio_interruz)


        self.lista_input_analisi.addLayout(self.layout_analisi_foglio_interruz)

        self.layout_analisi_anno = QHBoxLayout()
        self.layout_analisi_anno.setObjectName(u"layout_analisi_anno")
        self.label_analisi_anno = QLabel(self.layoutWidget)
        self.label_analisi_anno.setObjectName(u"label_analisi_anno")
        self.label_analisi_anno.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.label_analisi_anno.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.layout_analisi_anno.addWidget(self.label_analisi_anno)

        self.spinBox_analisi_anno = QSpinBox(self.layoutWidget)
        self.spinBox_analisi_anno.setObjectName(u"spinBox_analisi_anno")

        self.layout_analisi_anno.addWidget(self.spinBox_analisi_anno)


        self.lista_input_analisi.addLayout(self.layout_analisi_anno)

        self.layout_analisi_soglia = QHBoxLayout()
        self.layout_analisi_soglia.setObjectName(u"layout_analisi_soglia")
        self.label_analisi_soglia = QLabel(self.layoutWidget)
        self.label_analisi_soglia.setObjectName(u"label_analisi_soglia")
        self.label_analisi_soglia.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.layout_analisi_soglia.addWidget(self.label_analisi_soglia)

        self.doubleSpinBox_analisi_soglia = QDoubleSpinBox(self.layoutWidget)
        self.doubleSpinBox_analisi_soglia.setObjectName(u"doubleSpinBox_analisi_soglia")

        self.layout_analisi_soglia.addWidget(self.doubleSpinBox_analisi_soglia)


        self.lista_input_analisi.addLayout(self.layout_analisi_soglia)

        self.layout_analisi_max_d = QHBoxLayout()
        self.layout_analisi_max_d.setObjectName(u"layout_analisi_max_d")
        self.label_analisi_max_d = QLabel(self.layoutWidget)
        self.label_analisi_max_d.setObjectName(u"label_analisi_max_d")
        self.label_analisi_max_d.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.layout_analisi_max_d.addWidget(self.label_analisi_max_d)

        self.doubleSpinBox_analisi_max_d = QDoubleSpinBox(self.layoutWidget)
        self.doubleSpinBox_analisi_max_d.setObjectName(u"doubleSpinBox_analisi_max_d")

        self.layout_analisi_max_d.addWidget(self.doubleSpinBox_analisi_max_d)


        self.lista_input_analisi.addLayout(self.layout_analisi_max_d)

        self.layout_analisi_wiggle = QHBoxLayout()
        self.layout_analisi_wiggle.setObjectName(u"layout_analisi_wiggle")
        self.label_analisi_wiggle = QLabel(self.layoutWidget)
        self.label_analisi_wiggle.setObjectName(u"label_analisi_wiggle")
        self.label_analisi_wiggle.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.layout_analisi_wiggle.addWidget(self.label_analisi_wiggle)

        self.doubleSpinBox_analisi_wiggle = QDoubleSpinBox(self.layoutWidget)
        self.doubleSpinBox_analisi_wiggle.setObjectName(u"doubleSpinBox_analisi_wiggle")

        self.layout_analisi_wiggle.addWidget(self.doubleSpinBox_analisi_wiggle)


        self.lista_input_analisi.addLayout(self.layout_analisi_wiggle)

        self.layout_analisi_delta = QHBoxLayout()
        self.layout_analisi_delta.setObjectName(u"layout_analisi_delta")
        self.label_analisi_delta = QLabel(self.layoutWidget)
        self.label_analisi_delta.setObjectName(u"label_analisi_delta")
        self.label_analisi_delta.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.layout_analisi_delta.addWidget(self.label_analisi_delta)

        self.doubleSpinBox_analisi_delta = QDoubleSpinBox(self.layoutWidget)
        self.doubleSpinBox_analisi_delta.setObjectName(u"doubleSpinBox_analisi_delta")

        self.layout_analisi_delta.addWidget(self.doubleSpinBox_analisi_delta)


        self.lista_input_analisi.addLayout(self.layout_analisi_delta)

        self.bottone_start_analisi = QPushButton(self.layoutWidget)
        self.bottone_start_analisi.setObjectName(u"bottone_start_analisi")

        self.lista_input_analisi.addWidget(self.bottone_start_analisi)

        self.progressBar_analisi = QProgressBar(self.layoutWidget)
        self.progressBar_analisi.setObjectName(u"progressBar_analisi")
        self.progressBar_analisi.setValue(0)

        self.lista_input_analisi.addWidget(self.progressBar_analisi)

        self.plainTextEdit_analisi = QPlainTextEdit(self.layoutWidget)
        self.plainTextEdit_analisi.setObjectName(u"plainTextEdit_analisi")
        self.plainTextEdit_analisi.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        self.lista_input_analisi.addWidget(self.plainTextEdit_analisi)

        self.tabWidget.addTab(self.tab_analisi, "")

        self.centralLayout.addWidget(self.tabWidget)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Auto Nos", None))
        self.label_cartella_input.setText(QCoreApplication.translate("MainWindow", u"Cartella Input", None))
        self.pushButton_scegli_input.setText(QCoreApplication.translate("MainWindow", u"Scegli...", None))
        self.label_cartella_output.setText(QCoreApplication.translate("MainWindow", u"Cartella Output", None))
        self.pushButton_scegli_output.setText(QCoreApplication.translate("MainWindow", u"Scegli...", None))
        self.label_posizione_naso.setText(QCoreApplication.translate("MainWindow", u"Posizione Naso Elettronico", None))
        self.label_anno.setText(QCoreApplication.translate("MainWindow", u"Anno", None))
        self.checkBox_stampa_meta.setText(QCoreApplication.translate("MainWindow", u"Stampa Metadati sui sensori", None))
        self.bottone_start_queuer.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_queuer), QCoreApplication.translate("MainWindow", u"Queuer", None))
        self.label_analisi_cartella_input.setText(QCoreApplication.translate("MainWindow", u"Cartella Input", None))
        self.pushButton_analisi_scegli_input.setText(QCoreApplication.translate("MainWindow", u"Scegli...", None))
        self.label_analisi_cartella_meteo.setText(QCoreApplication.translate("MainWindow", u"Cartella Meteo", None))
        self.pushButton_analisi_cartella_meteo.setText(QCoreApplication.translate("MainWindow", u"Scegli...", None))
        self.label_analisi_file_interruz.setText(QCoreApplication.translate("MainWindow", u"File Interruzioni", None))
        self.pushButton_analisi_scegli_file_interruz.setText(QCoreApplication.translate("MainWindow", u"Scegli...", None))
        self.label_analisi_foglio_interruz.setText(QCoreApplication.translate("MainWindow", u"Nome Foglio Interruzioni", None))
        self.label_analisi_anno.setText(QCoreApplication.translate("MainWindow", u"Anno", None))
        self.label_analisi_soglia.setText(QCoreApplication.translate("MainWindow", u"Soglia", None))
        self.label_analisi_max_d.setText(QCoreApplication.translate("MainWindow", u"max_d", None))
        self.label_analisi_wiggle.setText(QCoreApplication.translate("MainWindow", u"wiggle", None))
        self.label_analisi_delta.setText(QCoreApplication.translate("MainWindow", u"delta", None))
        self.bottone_start_analisi.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_analisi), QCoreApplication.translate("MainWindow", u"Analisi", None))
    # retranslateUi

