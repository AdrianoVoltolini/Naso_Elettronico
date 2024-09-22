from PySide6 import QtCore
import os
from auto_nos_queuer import get_filenames, split_month, merge_files
from analisi_nos import recupera_interruzioni, elabora_mese


class EmittingStream(QtCore.QObject):

    textWritten = QtCore.Signal(str)

    def write(self, text):
        self.textWritten.emit(str(text))
        
    def flush(self):
        pass


class QueuerWorker(QtCore.QObject):
    
    finished = QtCore.Signal()
    progress = QtCore.Signal(int)

    def __init__(self, anno, posizione_naso, cartella_input, cartella_output, stampa_meta, mesi):
        super().__init__()  

        self.anno = anno
        self.posizione_naso = posizione_naso
        self.cartella_input = cartella_input
        self.cartella_output = cartella_output
        self.stampa_meta = stampa_meta
        self.mesi = mesi


    def run(self):
        
        try:
            os.mkdir(self.cartella_output)
        except:
            pass

        agg_months = get_filenames(self.cartella_input, self.anno)

        cnt = 0


        for m, month_df in agg_months:
            print(f"inizio {self.mesi[m]}...")

            quartet_list, q_starts, q_ends = split_month(month_df)
            cartella_mese = f"{str(m).zfill(2)} {self.posizione_naso}_Misure {self.mesi[m]} {self.anno}"
            try:
                os.mkdir(f"{self.cartella_output}/{cartella_mese}")
            except:
                pass

            for i in range(len(quartet_list)):
                
                q_file, q_metadata = merge_files(self.cartella_input, quartet_list[i])

                if q_starts[i] != q_ends[i]:
                    nome_file = f"{self.cartella_output}/{cartella_mese}/aaa_{self.anno}_{str(m).zfill(2)}_{str(q_starts[i]).zfill(2)}-{str(q_ends[i]).zfill(2)} {self.posizione_naso}.nos"
                    nome_metadata = f"{self.cartella_output}/{cartella_mese}/meta_{self.anno}_{str(m).zfill(2)}_{str(q_starts[i]).zfill(2)}-{str(q_ends[i]).zfill(2)} {self.posizione_naso}.csv"
                else:
                    nome_file = f"{self.cartella_output}/{cartella_mese}/aaa_{self.anno}_{str(m).zfill(2)}_{str(q_starts[i]).zfill(2)} {self.posizione_naso}.nos"
                    nome_metadata = f"{self.cartella_output}/{cartella_mese}/meta_{self.anno}_{str(m).zfill(2)}_{str(q_starts[i]).zfill(2)} {self.posizione_naso}.csv"

                with open(nome_file, "w") as f:
                    f.write(q_file)

                if self.stampa_meta == True:
                    q_metadata.to_csv(nome_metadata, sep=";")
                
                #print(f"{i+1}/{len(quartet_list)} finiti di {self.mesi[m]}")
                cnt_frac = (i+1)/len(quartet_list)
                self.progress.emit(round(((cnt+cnt_frac)/len(agg_months))*100))
            cnt += 1
            self.progress.emit(round((cnt/len(agg_months))*100))

        print("finito!")
        self.finished.emit()



class AnalisiWorker(QtCore.QObject):
    
    finished = QtCore.Signal()
    progress = QtCore.Signal(int)

    def __init__(self, cartella, cartella_meteo, interruzioni, sheet, anno, soglia, max_d, wiggle, delta, mesi):
        super().__init__()  
        self.cartella = cartella
        self.cartella_meteo = cartella_meteo
        self.interruzioni = interruzioni
        self.sheet = sheet
        self.anno = anno
        self.soglia = soglia
        self.max_d = max_d
        self.wiggle = wiggle
        self.delta = delta
        self.mesi = mesi


    def run(self):

        df_interruzioni = recupera_interruzioni(self.interruzioni, self.sheet, self.anno)
        
        cnt = 0
        list_cartella = os.listdir(self.cartella)

        for sub_cartella in list_cartella:
            cnt += 1
            temp_path = f"{self.cartella}/{sub_cartella}/"
            if os.path.isdir(temp_path):
                print(f"inizio {sub_cartella}...")
                em_err = elabora_mese(temp_path, self.anno, self.soglia, self.max_d, df_interruzioni, self.wiggle, self.delta, self.mesi, self.cartella_meteo)
                if em_err != None:
                    print(em_err)
                self.progress.emit(round((cnt/len(list_cartella))*100))

        print("finito!")
        self.finished.emit()