# %%
#per connettersi a google drive
#from google.colab import drive
#drive.mount('/content/drive')

#per spostarsi nella cartella del naso elettronico
#%cd /content/drive/MyDrive/biomonitoraggio/naso_elettronico

# %%
#per caricare pacchetti
import re
import os
import math
import pandas as pd

from datetime import datetime
from io import StringIO

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# %%
#prende in input nome della cartella dove ci sono i file e anno delle misure
#ritorna in output i nomi dei file divisi per mese sottoforma di DataFrame.groupby
def get_filenames(nome_cartella, anno):

  #recupera nome dei file
  nomi_files = os.listdir(nome_cartella)

  #recupera date e ore dai nomi dei file e salva in dizionario
  diz_files = {}
  for nome in nomi_files:
    if nome.endswith(".nos"):
      temp_list = nome.replace(".","_").split("_")
      diz_files[nome] = "".join(temp_list[-3:-1])

  #trasforma dizionario in pandas DataFrame (più facile da manipolare)
  df_files = pd.DataFrame(diz_files, index=["datetime_raw"], ).T

  #converte stringhe di data e ora in formato datetime (più facile da manipolare).
  df_files["datetime"] = df_files["datetime_raw"].map(lambda x: datetime.strptime(anno+x, "%Y%d%m%H%M%S"))

  #rimuove colonna datetime_raw (non ci serve più)
  df_clean = df_files.drop("datetime_raw",axis=1)

  #mette gli elementi del dataframe in ordine dal più vecchio al più recente
  df_clean = df_clean.sort_values("datetime")

  #rende datetime nuovo indice del dataframe
  df_clean = df_clean.reset_index(names="filename")
  df_clean = df_clean.set_index("datetime")

  #raggruppa righe in base al mese
  grouped_by_month = df_clean.groupby(lambda x: x.month)

  return grouped_by_month


# %%
#prende in input il dataframe di un singolo mese
#divide i giorni del mese in gruppi da 4
#ritorna lista di dataframes
def split_month(grouped_month):

  grouped_by_day = grouped_month.groupby(lambda x: x.day)

  n_days = len(grouped_by_day)

  days = [*grouped_by_day.groups]
  days.sort()
  last_day = days[-1]

  n_splits = math.ceil(n_days/4)

  month_dfs = []
  start_days = []
  end_days = []

  for n in range(n_splits):
    month_dfs.append(pd.DataFrame())

  split_cnt = 0
  active_split = 0


  for day, day_group in grouped_by_day:

    if split_cnt < 4:
      month_dfs[active_split] = pd.concat([month_dfs[active_split], day_group])
      if split_cnt == 0:
        start_days.append(day)
      if split_cnt == 3 or day == last_day:
        end_days.append(day)
      split_cnt += 1
    else:
      split_cnt = 0
      active_split += 1
      month_dfs[active_split] = pd.concat([month_dfs[active_split], day_group])
      start_days.append(day)
      if day == last_day:
        end_days.append(day)
      split_cnt += 1

  return month_dfs, start_days, end_days


# %%
#funzione di supporto alla funzione 'merge_files'
#recupera i metadata dei sensori da un file
#ritorna dataframe di metadata di sensori di un file
def sensor_metadata(text_file, file_datetime):

  #trova inizio dei metadata dei sensori (quando comincia a parlare dei channels)
  for m in re.finditer("[[]Channels[]]", text_file):
    start_meta = m.end()+1
    break

  #trova fine dei metadata dei sensori (quando comincia a parlare di diluition factor)
  for n in re.finditer("Dilution	[(]Factor[)]", text_file):
    end_meta = n.start()-1
    break

  #recupera metadata dal file di testo e lo trasforma in dataframe
  str_metadata = text_file[start_meta:end_meta]
  df_metadata = pd.read_csv(StringIO(str_metadata), sep="\t", header=None)

  df_metadata[3] = df_metadata[1].map(lambda x: f" ({x})") #mette parentesi attorno a nomi delle sostanze che misurano i sensori

  df_metadata.index = df_metadata[0]+df_metadata[3] #nuovo indice è unione del nome del sensore e nome tra parentesi della sostanza

  #diverse funzioni per rendere il dataframe più pulito e leggibile
  df_metadata = df_metadata[[2]]
  df_metadata.columns = [file_datetime]
  df_metadata = df_metadata.T

  return df_metadata


#prende in input un dataframe e nome della cartella dove si vogliono salvare i files
#unisce i files descritti nel dataframe in un unico documento
#ritorna documento finale e df di metadata dei sensori di tutti i file
def merge_files(nome_cartella, quartet_df):
  check = False
  cnt = 0
  for i, riga in quartet_df.iterrows():
    if check == False:
      with open(nome_cartella+"/"+riga.iloc[0], "r") as f:
        final_file = f.read()[:-1]

      split_file = final_file.split("\n\n")

      nos_Channels = split_file[1]

      metadata = sensor_metadata(nos_Channels, i)

      check = True
    else:
      with open(nome_cartella+"/"+riga.iloc[0], "r") as f:
        temp_file = f.read()

      temp_split_file = temp_file.split("\n\n")
      t_nos_Channels = temp_split_file[1]
      t_nos_Data = temp_split_file[-2]

      temp_metadata = sensor_metadata(t_nos_Channels, i)

      final_file += "\n\n"+t_nos_Data
      metadata = pd.concat([metadata, temp_metadata])

      cnt +=1
  final_file += "\n\n"
  return (final_file, metadata)

# %%
def main(anno, posizione_naso, cartella_input, cartella_output, stampa_meta):

  mesi = {
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
      12:"DICEMBRE"
  }

  if cartella_output not in os.listdir():
    os.mkdir(cartella_output)

  agg_months = get_filenames(cartella_input, anno)

  for m, month_df in agg_months:
    print(f"inizio {mesi[m]}...")
    quartet_list, q_starts, q_ends = split_month(month_df)
    cartella_mese = f"{str(m).zfill(2)} {posizione_naso}_Misure {mesi[m]} {anno}"
    try:
      os.mkdir(f"{cartella_output}/{cartella_mese}")
    except:
      pass

    for i in range(len(quartet_list)):
      q_file, q_metadata = merge_files(cartella_input, quartet_list[i])

      if q_starts[i] != q_ends[i]:
        nome_file = f"{cartella_output}/{cartella_mese}/aaa_{anno}_{str(m).zfill(2)}_{str(q_starts[i]).zfill(2)}-{str(q_ends[i]).zfill(2)} {posizione_naso}.nos"
        nome_metadata = f"{cartella_output}/{cartella_mese}/meta_{anno}_{str(m).zfill(2)}_{str(q_starts[i]).zfill(2)}-{str(q_ends[i]).zfill(2)} {posizione_naso}.csv"
      else:
        nome_file = f"{cartella_output}/{cartella_mese}/aaa_{anno}_{str(m).zfill(2)}_{str(q_starts[i]).zfill(2)} {posizione_naso}.nos"
        nome_metadata = f"{cartella_output}/{cartella_mese}/meta_{anno}_{str(m).zfill(2)}_{str(q_starts[i]).zfill(2)} {posizione_naso}.csv"

      with open(nome_file, "w") as f:
        f.write(q_file)

      if stampa_meta == True:
        q_metadata.to_csv(nome_metadata, sep=";")

  print("\nfinished!")


# %%
if __name__ == "__main__":
  anno = "2024"
  posizione_naso = "Simoncelli"
  cartella_input = "Simoncelli_2024_ZI MISURE FEB (raw)"
  cartella_output = "ogni 4 gg"
  stampa_meta = False

  main(anno, posizione_naso, cartella_input, cartella_output, stampa_meta)


