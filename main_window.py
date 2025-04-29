import sys
from PySide6.QtWidgets import QApplication, QMainWindow , QFileDialog
from PySide6.QtCore import QThread
from PySide6.QtGui import QTextCursor
from GUI import Ui_MainWindow
from datetime import datetime

from utils import EmittingStream, QueuerWorker, AnalisiWorker

import warnings
warnings.simplefilter(action='ignore', category=SyntaxWarning)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setFixedSize(self.size()) 

        #self.ui.plainTextEdit_queuer.setDisabled(True)
        #self.ui.plainTextEdit_analisi.setDisabled(True)

        txt_intro = "Auto Nos 0.3 - Sviluppato da Adriano Voltolini per la Fondazione Museo Civico di Rovereto"
        self.ui.plainTextEdit_queuer.setPlainText(txt_intro)
        self.ui.plainTextEdit_analisi.setPlainText(txt_intro)

        self.mesi = {
            1:"GENNAIO",
            2:"FEBBRAIO",
            3:"MARZO",
            4:"APRILE",
            5:"MAGGIO",
            6:"GIUGNO",
            7:"LUGLIO",
            8:"AGOSTO",
            9:"SETTEMBRE",
            10:"OTTOBRE",
            11:"NOVEMBRE",
            12:"DICEMBRE"}

        #cambia massimi e minimi degli spinbox
        self.ui.spinBox_anno.setMinimum(1900)
        self.ui.spinBox_anno.setMaximum(2100)
        self.ui.spinBox_analisi_anno.setMinimum(1900)
        self.ui.spinBox_analisi_anno.setMaximum(2100)
        self.ui.doubleSpinBox_analisi_max_d.setMaximum(9999)

        #setta valori iniziali
        self.ui.spinBox_anno.setValue(datetime.now().year)
        self.ui.spinBox_analisi_anno.setValue(datetime.now().year)
        self.ui.doubleSpinBox_analisi_max_d.setValue(400)
        self.ui.doubleSpinBox_analisi_soglia.setValue(2)
        self.ui.lineEdit_posizione_naso.setText("Simoncelli")

        #connette pulsanti scegli
        self.ui.pushButton_scegli_input.pressed.connect(self.scegli_input_directory)
        self.ui.pushButton_scegli_output.pressed.connect(self.scegli_output_directory)
        self.ui.pushButton_analisi_scegli_input.pressed.connect(self.scegli_input_analisi_directory)
        self.ui.pushButton_analisi_scegli_file_interruz.pressed.connect(self.scegli_file_interruzioni)
        self.ui.pushButton_analisi_cartella_meteo.pressed.connect(self.scegli_cartella_meteo)

        #connette lineEdit output_queuer con lineEdit di input_analisi
        self.ui.lineEdit_cartella_output.textChanged.connect(self.cambia_input_analisi_directory)
        self.ui.spinBox_anno.valueChanged.connect(self.cambia_input_analisi_anno)

        #aggiungi tooltip ai vari label
        self.ui.label_cartella_input.setToolTip("cartella dove sono tutti i file NOS che si vogliono concatenare")
        self.ui.label_cartella_output.setToolTip("cartella dove verranno salvati i file NOS concatenati, suddivisi per mesi")
        self.ui.label_posizione_naso.setToolTip("suffisso per i file NOS concatenati")
        self.ui.label_anno.setToolTip("Anno in cui sono state effettuate <b>TUTTE</b> le misurazioni nei file NOS")
        self.ui.checkBox_stampa_meta.setToolTip("scegli se salvare i metadata dei sensori, in formato csv")
        self.ui.label_analisi_cartella_input.setToolTip("cartella dove sono le sottocartelle dei NOS divisi per mese")
        self.ui.label_analisi_cartella_meteo.setToolTip("cartella dove sono i file CSV riguardanti la direzione e velocità del vento dell'anno scelto")
        self.ui.label_analisi_file_interruz.setToolTip("file csv creato dal queuer dove sono annotate le interruzioni di misurazione")
        self.ui.label_analisi_anno.setToolTip("Anno in cui sono state effettuate <b>TUTTE</b> le misurazioni nei file NOS")
        self.ui.label_analisi_soglia.setToolTip("soglia dei segnali affinché vengano considerati come picchi")
        self.ui.label_analisi_max_d.setToolTip("distanza massima affinché due picchi vengano considerati della stessa curva")


        # per scrivere output del terminale nei textedit
        sys.stdout = EmittingStream(textWritten=self.normalOutputWritten)
        sys.stderr = EmittingStream(textWritten=self.normalOutputWritten)

        #connette bottoni di start
        self.ui.bottone_start_queuer.pressed.connect(self.inizia_queuer)
        self.ui.bottone_start_analisi.pressed.connect(self.inizia_analisi)
        

    def normalOutputWritten(self, text):
        if self.ui.tabWidget.currentIndex() == 0:
            self.ui.plainTextEdit_queuer.appendPlainText(text)
            #self.ui.plainTextEdit_queuer.moveCursor(QTextCursor.EndOfBlock)
            #self.ui.plainTextEdit_queuer.ensureCursorVisible()
        else:
            self.ui.plainTextEdit_analisi.appendPlainText(text)
            #self.ui.plainTextEdit_analisi.moveCursor(QTextCursor.EndOfBlock)
            #self.ui.plainTextEdit_analisi.ensureCursorVisible()

    def scegli_input_directory(self):
        dir = QFileDialog.getExistingDirectory(self)
        self.ui.lineEdit_cartella_input.setText(dir)

    def scegli_output_directory(self):
        dir = QFileDialog.getExistingDirectory(self)
        self.ui.lineEdit_cartella_output.setText(dir)

    def scegli_input_analisi_directory(self):
        dir = QFileDialog.getExistingDirectory(self)
        self.ui.lineEdit_analisi_cartella_input.setText(dir)
    
    def scegli_cartella_meteo(self):
        dir = QFileDialog.getExistingDirectory(self)
        self.ui.lineEdit_analisi_cartella_meteo.setText(dir)

    def scegli_file_interruzioni(self):
        dir = QFileDialog.getOpenFileName(self)
        self.ui.lineEdit_analisi_file_interruz.setText(dir[0])

    def cambia_input_analisi_directory(self):
        self.ui.lineEdit_analisi_cartella_input.setText(self.ui.lineEdit_cartella_output.text())
    
    def cambia_input_analisi_anno(self):
        self.ui.spinBox_analisi_anno.setValue(self.ui.spinBox_anno.value())
    
    def inizia_queuer(self):

        da_disattivare = [
            self.ui.lineEdit_cartella_input,
            self.ui.pushButton_scegli_input,
            self.ui.lineEdit_cartella_output,
            self.ui.pushButton_scegli_output,
            self.ui.lineEdit_posizione_naso,
            self.ui.spinBox_anno,
            self.ui.checkBox_stampa_meta,
            self.ui.bottone_start_queuer]

        for x in da_disattivare:
            x.setDisabled(True)

        self.ui.progressBar_queuer.setValue(0)

        anno = str(self.ui.spinBox_anno.value())
        posizione_naso = self.ui.lineEdit_posizione_naso.text()
        cartella_input = self.ui.lineEdit_cartella_input.text()
        cartella_output = self.ui.lineEdit_cartella_output.text()
        stampa_meta = self.ui.checkBox_stampa_meta.isChecked()

        self.worker = QueuerWorker(anno, posizione_naso, cartella_input, cartella_output, stampa_meta, self.mesi)
        self.mythread = QThread()
        self.worker.moveToThread(self.mythread)
        self.mythread.started.connect(self.worker.run)

        self.worker.progress.connect(lambda x: self.ui.progressBar_queuer.setValue(x))
        self.worker.finished.connect(self.mythread.quit)

        self.worker.finished.connect(lambda: self.ui.lineEdit_cartella_input.setDisabled(False))
        self.worker.finished.connect(lambda: self.ui.pushButton_scegli_input.setDisabled(False))
        self.worker.finished.connect(lambda: self.ui.lineEdit_cartella_output.setDisabled(False))
        self.worker.finished.connect(lambda: self.ui.pushButton_scegli_output.setDisabled(False))
        self.worker.finished.connect(lambda: self.ui.lineEdit_posizione_naso.setDisabled(False))
        self.worker.finished.connect(lambda: self.ui.spinBox_anno.setDisabled(False))
        self.worker.finished.connect(lambda: self.ui.checkBox_stampa_meta.setDisabled(False))
        self.worker.finished.connect(lambda: self.ui.bottone_start_queuer.setDisabled(False))

        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.finished.connect(self.mythread.deleteLater)

        self.mythread.start()

    def inizia_analisi(self):
        #self.ui.tabWidget.setDisabled(True)
        self.ui.progressBar_analisi.setValue(0)

        cartella = self.ui.lineEdit_analisi_cartella_input.text()
        cartella_meteo = self.ui.lineEdit_analisi_cartella_meteo.text()
        interruzioni = self.ui.lineEdit_analisi_file_interruz.text()
        anno = self.ui.spinBox_anno.value()
        soglia = self.ui.doubleSpinBox_analisi_soglia.value()
        max_d = self.ui.doubleSpinBox_analisi_max_d.value()

        self.worker = AnalisiWorker(cartella, cartella_meteo, interruzioni, anno, soglia, max_d, self.mesi)
        self.mythread = QThread()
        self.worker.moveToThread(self.mythread)
        self.mythread.started.connect(self.worker.run)

        self.worker.progress.connect(lambda x: self.ui.progressBar_analisi.setValue(x))
        self.worker.finished.connect(self.mythread.quit)
        self.worker.finished.connect(lambda: self.ui.tabWidget.setDisabled(False))
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.finished.connect(self.mythread.deleteLater)

        self.mythread.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())