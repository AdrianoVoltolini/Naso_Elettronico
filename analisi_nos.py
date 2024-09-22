# %%
#per connettersi a google drive
#from google.colab import drive
#drive.mount('/content/drive')

#per spostarsi nella cartella del naso elettronico
#%cd /content/drive/MyDrive/biomonitoraggio/naso_elettronico

# %%
import re
import os
import matplotlib.pyplot as plt
import matplotlib.patheffects as patheffects
import matplotlib as mpl
import numpy as np
import pandas as pd

from io import StringIO
from datetime import datetime, timedelta, time

import warnings
warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)
warnings.simplefilter(action='ignore', category=UserWarning)
warnings.simplefilter(action='ignore', category=SyntaxWarning)

# %%
def round_to_nearest_minute(dt):
  if dt.second >= 30:
    return dt + timedelta(seconds=(60 - dt.second))
  else:
    return dt - timedelta(seconds=dt.second)

def direzione_vento(gradi):
  if gradi < 22.5 or gradi >= 337.5:
    return "NORD"
  elif 22.5 <= gradi < 67.5:
    return "NORD-EST"
  elif 67.5 <= gradi < 112.5:
    return "EST"
  elif 112.5 <= gradi < 157.5:
    return "SUD-EST"
  elif 157.5 <= gradi < 202.5:
    return "SUD"
  elif 202.5 <= gradi < 247.5:
    return "SUD-OVEST"
  elif 247.5 <= gradi < 292.5:
    return "OVEST"
  elif 292.5 <= gradi < 337.5:
    return "NORD-OVEST"


def trova_picchi(filename, soglia, max_d, meteo_df):

  with open(filename, "r") as f:
    text_file = f.read()

  #trova dove cominciano i dati nel file. Ci possono essere più inizi
  data_list = re.findall("\[Data\].*?\n\n", text_file, flags=re.DOTALL)

  picchi_df = pd.DataFrame()
  full_df = pd.DataFrame()

  is_pdf_empty = True
  is_fdf_empty = True

  for b, data in enumerate(data_list):
    data_lines = data.split("\n")

    #per togliere le prime due righe
    clean_lines = "\n".join(data_lines[2:])

    #recupera orario di inizio
    file_datetime = datetime.strptime(data_lines[1], "; %d/%m/%Y %H:%M:%S")

    #trasforma testo in numpy array
    raw_array = np.loadtxt(StringIO(clean_lines), delimiter="\t")

    #trasforma array in pandas dataframe, butta via ultime colonne e metti come indici la data con orario
    clean_df = pd.DataFrame(raw_array[:,:10], columns=range(1,11))
    clean_df.index = clean_df.index.map(lambda x: file_datetime + timedelta(seconds=x))

    #salva i dati in un unico dataframe
    if is_fdf_empty == True:
      full_df = clean_df
      is_fdf_empty = False
    else:
      full_df = pd.concat([full_df, clean_df])

    #guarda se ci sono segnali più grandi del soglia
    mask_df = clean_df > soglia


    if np.any(mask_df):

      #recupera valori sopra il soglia
      picchi = np.argwhere(clean_df > soglia)
      picchi_val = raw_array[picchi[:,0], picchi[:,1]]

      #metti risultati della ricerca in un dataframe
      pd_picchi = pd.DataFrame(picchi, columns=["orario","sensore"], index=clean_df.iloc[picchi[:,0],].index)
      pd_picchi["valore_picco"] = picchi_val

      #ordina i dati per intensità di segnale a parità di orario
      pd_picchi = pd_picchi.sort_values(["orario", "valore_picco"], ascending=[True, False])

      #raggruppa i dati in base all'orario
      gb_picchi = pd_picchi.groupby(pd_picchi.index)
      ag_picchi = gb_picchi.agg({"sensore": lambda x: [y+1 for y in x], "valore_picco": lambda x: [y for y in x]})


      ag_picchi["curva"] = [0] * ag_picchi.shape[0]

      if is_pdf_empty == True:
        picchi_df = ag_picchi
        is_pdf_empty = False
      else:
        picchi_df = pd.concat([picchi_df, ag_picchi])


  final_df = pd.DataFrame(index=["inizio", "fine", "picchi", "sensori", "ora picco max", "durata (s)", "aveWDIR", "aveWVEL", "vento cardinali"])

  if is_pdf_empty == False:
    curva = 0

    #classifica i picchi in curve di segnale in base al sensore ed alla distanza in secondi tra i picchi
    for i in range(1, picchi_df.shape[0]):
      same_sensor = False
      for s in picchi_df.iloc[i,0]:
        if s in picchi_df.iloc[i-1,0]:
          same_sensor = True
      if same_sensor == False:
        curva += 1
        picchi_df.iat[i,-1] = curva
      else:
        time_diff = picchi_df.index[i] - picchi_df.index[i-1]
        if time_diff.total_seconds() < max_d:
          picchi_df.iat[i,-1] = curva
        else:
          curva +=1
          picchi_df.iat[i,-1] = curva


    ag_df = picchi_df.groupby("curva")

    #per ogni curva: salva l'orario d'inizio, di fine, la durata in secondi,
    #i sensori in ordine di intensità decrescente assieme ai loro segnali più grandi misurati,
    #e l'ora in cui c'è stato il segnale più intenso in assoluto.
    for i,j in ag_df:
      start = j.index[0]
      end = j.index[-1]
      temp_diff = end-start

      s_diz = {}
      max_val = 0
      max_val_orario = datetime(2000,1,1)
      for l in range(j.shape[0]):
        for s in range(len(j.iloc[l,0])):
          val = j.iloc[l,1][s]
          if val > max_val:
            max_val = val
            max_val_orario = j.index[l]
          if j.iloc[l,0][s] not in s_diz.keys():
            s_diz[j.iloc[l,0][s]] = [val]
          else:
            s_diz[j.iloc[l,0][s]].append(val)

      max_diz = {}



      for k in s_diz.keys():
        max_diz[k] = max(s_diz[k])

      max_df = pd.DataFrame(max_diz, index=[0]).sort_values([0], axis=1, ascending=False)

      temp_series = pd.Series({"inizio":start,
                              "fine":end,
                              "picchi": max_df.iloc[0,:].tolist(),
                              "sensori": max_df.columns.tolist(),
                              "ora picco max": max_val_orario,
                              "durata (s)": temp_diff.total_seconds()},
                              name=i)

      rounded_max_val_orario = round_to_nearest_minute(max_val_orario)

      try:
        max_val_meteo = meteo_df.loc[rounded_max_val_orario]
        temp_concat = pd.concat([temp_series,max_val_meteo])
        final_df = pd.concat([final_df, temp_concat], axis=1)
      except:
        if meteo_df.shape[0] > 0:
          print(f"misure del vento non trovate per {rounded_max_val_orario}")
        final_df = pd.concat([final_df, temp_series], axis=1)

    final_df.loc["vento cardinali"] = final_df.loc["aveWDIR"].map(lambda x: direzione_vento(float(x)))
  final_df.rename(index={"aveWDIR":"vento dir (°)", "aveWVEL": "vento vel (m/s)"}, inplace=True)

  return full_df, final_df.T

# %%

#funzioni per formattare la data

def accorcia_datetime(my_dt):
  return " ".join([str(my_dt.date()), str(my_dt.time())[:-3]])

def time_to_delta(t):
  out = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)
  return out


#legge foglio excel con le interruzioni e le salva in dataframe
def recupera_interruzioni(filename, sheet, anno):

  raw_df = pd.read_excel(filename, sheet_name=sheet)

  start_row = raw_df.index[raw_df.iloc[:,0] == anno][0]

  possible_ends = raw_df.iloc[start_row:,:].index[raw_df.iloc[start_row:,0].isnull() == True]

  if len(possible_ends) > 1:
    end_row = possible_ends[1]
  else:
    end_row = -1

  #bisognerebbe ottimizzare da qui al return, ma il numero delle righe è così piccolo di solito che non ne vale la pena
  df_output = raw_df.iloc[start_row+1:end_row,:8]

  df_output.columns = ["posizione", "data_inizio", "ora_inizio", "data_stop", "ora_stop", "data_riavvio", "ora_riavvio", "note"]
  df_output = df_output.drop(df_output.index[0]).dropna(subset="data_stop").reset_index(drop=True)

  df_output["ora_delta_stop"] = df_output["ora_stop"].map(time_to_delta)
  df_output["ora_delta_riavvio"] = df_output["ora_riavvio"].map(time_to_delta)

  df_output["stop"] = df_output["data_stop"] + df_output["ora_delta_stop"]
  df_output["riavvio"] = df_output["data_riavvio"] + df_output["ora_delta_riavvio"]

  return df_output[["posizione", "stop", "riavvio", "note"]]


# %%
#trova dove bisogna disegnare linee verticali:
#a mezzogiorno, mezzanotte e alle interruzioni
def posiziona_verticali(raw, df_interruzioni, wiggle, delta):

  mezzi_giorni = []
  mezzi_pos = []

  stops = []
  stop_pos = []

  riavvii = []

  #trova interruzioni che influenza dati considerati
  for i, r in df_interruzioni.iterrows():

    stop = r["stop"] + timedelta(seconds=delta) #aggiungi all'ora di stop un ammontare di secondi pari al numero di secondi che dura la misurazione
    riavvio = r["riavvio"]
    inizio_riavvio_diff = riavvio - raw.index[0]
    fine_stop_diff = raw.index[-1] - stop

    if raw.index[0] <= stop and riavvio <= raw.index[-1]:
      stops.append(stop)
      riavvii.append(riavvio)
      #print("\nnel mezzo", stops[-1], riavvii[-1])

    elif abs(inizio_riavvio_diff.total_seconds()) < wiggle: # considera anche se interruzione è molto vicino all'inizio
      stops.append(stop)
      riavvii.append(raw.index[0])
      #print("\noltre l'inizio", riavvii[-1])
    elif abs(fine_stop_diff.total_seconds()) < wiggle: # considera anche se interruzione è molto vicino alla fine
      stops.append(raw.index[-1])
      riavvii.append(riavvio)
      #print("\noltre la fine", stops[-1])
    else:
      #print("no interruzioni")
      pass

  #trova i punti più vicini al mezzogiorno e mezzanotte
  for i in range(1,raw.shape[0]):
    prev_dt = raw.index[i-1]
    curr_dt = raw.index[i]
    if i == 1 and prev_dt.hour == 12 and prev_dt.minute < 10: #se primo elemento è vicino a mezzogiorno
      mezzi_giorni.append(accorcia_datetime(prev_dt))
      mezzi_pos.append(i-1)
    elif i == 1 and prev_dt.hour == 0 and prev_dt.minute < 10: #se primo elemento è vicino a mezzanotte
      mezzi_giorni.append(accorcia_datetime(prev_dt))
      mezzi_pos.append(i-1)
    elif prev_dt.hour == 11 and curr_dt.hour == 12: #se c'è passaggio dalle 11 alle 12
      mezzi_giorni.append(accorcia_datetime(curr_dt))
      mezzi_pos.append(i)
    elif prev_dt.hour == 23 and curr_dt.hour == 0: #se c'è passaggio dalle 23 alle 00
      mezzi_giorni.append(accorcia_datetime(curr_dt))
      mezzi_pos.append(i)
    elif i == raw.shape[0]-1 and curr_dt.hour == 11 and curr_dt.minute > 50: #se ultimo elemento è vicino a mezzogiorno
      mezzi_giorni.append(accorcia_datetime(curr_dt))
      mezzi_pos.append(i)
    elif i == raw.shape[0]-1 and curr_dt.hour == 23 and curr_dt.minute > 50: #se ultimo elemento è vicino a mezzanotte
      mezzi_giorni.append(accorcia_datetime(curr_dt))
      mezzi_pos.append(i)

    #salva la posizione delle interruzioni
    for s in stops:
      if i == 1 and prev_dt >= s:
        stop_pos.append(0)
      elif prev_dt <= s and curr_dt > s:
        stop_pos.append(i)
      elif i == raw.shape[0]-1 and curr_dt <= s:
        stop_pos.append(i)

  return mezzi_giorni, mezzi_pos, stops, stop_pos, riavvii

# %%

#fa il grafico
def disegnatore(raw, titolo, soglia, mezzi_giorni, mezzi_pos, stops, stop_pos, riavvii):

  # crea la "cornice" del grafico
  fig, ax = plt.subplots()

  # colori scelti per il plot
  my_colors = [
      "darkred",
      "forestgreen",
      "darkblue",
      "red",
      "limegreen",
      "blue",
      "indigo",
      "darkviolet",
      "olive",
      "darkslategray",
      "teal",
      "black",
      "blueviolet",
      "gray",
      "darkseagreen",
      "royalblue"
  ]
  ax.set_prop_cycle("color", my_colors)

  ax.plot(raw.to_numpy(), linewidth=0.4, label=range(1,11)) #disegna il plot

  plt.grid(linestyle="--") #griglia in background

  plt.axhline(soglia, color="red") # linea della soglia

  #disegna le righe verticali per il mezzogiorno e mezzanotte
  #mette in grassetto se sono alle estremità del grafico
  for l in range(len(mezzi_pos)):
    if mezzi_giorni[l][-5:-1] in ["00:0","23:5"]:
      if l == 0:
        if len(stop_pos) == 0:
          plt.axvline(mezzi_pos[l], color="red", linewidth=3)
        else:
          if mezzi_pos[l] < stop_pos[0]:
            plt.axvline(mezzi_pos[l], color="red", linewidth=3)
          else:
            plt.axvline(mezzi_pos[l], color="red")
      elif l == len(mezzi_pos)-1:
        if len(stop_pos) == 0:
          plt.axvline(mezzi_pos[l], color="red", linewidth=3)
        else:
          if mezzi_pos[l] > stop_pos[-1]:
            plt.axvline(mezzi_pos[l], color="red", linewidth=3)
          else:
            plt.axvline(mezzi_pos[l], color="red")
      else:
        plt.axvline(mezzi_pos[l], color="red")

    elif mezzi_giorni[l][-5:-1] in ["12:0","11:5"]:
      if l == 0:
        if len(stop_pos) == 0:
          plt.axvline(mezzi_pos[l], linewidth=3)
        else:
          if mezzi_pos[l] < stop_pos[0]:
            plt.axvline(mezzi_pos[l], linewidth=3)
          else:
            plt.axvline(mezzi_pos[l])
      elif l == len(mezzi_pos)-1:
        if len(stop_pos) == 0:
          plt.axvline(mezzi_pos[l], linewidth=3)
        else:
          if mezzi_pos[l] > stop_pos[-1]:
            plt.axvline(mezzi_pos[l], linewidth=3)
          else:
            plt.axvline(mezzi_pos[l])
      else:
        plt.axvline(mezzi_pos[l])


  #disegna linee delle interruzioni (se ce ne sono)
  for s in range(len(stop_pos)):
    if stop_pos[s] == 0:
      plt.axvline(stop_pos[s], color="orange", linewidth=3)
      plt.annotate(accorcia_datetime(stops[s]), [stop_pos[s]-raw.shape[0]/50, 2.15], size=7, rotation=90, color="orange", annotation_clip=False,)
                    #path_effects=[patheffects.withStroke(linewidth=0.5, foreground='lightgray', capstyle="round")]) # contorni
      plt.annotate(accorcia_datetime(riavvii[s]), [stop_pos[s]+raw.shape[0]/150, 2.15], size=7, rotation=90, color="orange", annotation_clip=False,)
                    #path_effects=[patheffects.withStroke(linewidth=0.5, foreground='lightgray', capstyle="round")]) # contorni
      #print("ciao_s1")
    elif 0 < stop_pos[s] < raw.shape[0]-1:
      plt.axvline(stop_pos[s], color="orange")
      plt.annotate(accorcia_datetime(stops[s]), [stop_pos[s]-raw.shape[0]/50, 2.15], size=7, rotation=90, color="orange", annotation_clip=False,)
                    #path_effects=[patheffects.withStroke(linewidth=0.5, foreground='lightgray', capstyle="round")]) # contorni
      plt.annotate(accorcia_datetime(riavvii[s]), [stop_pos[s]+raw.shape[0]/150, 2.15], size=7, rotation=90, color="orange", annotation_clip=False,)
                    #path_effects=[patheffects.withStroke(linewidth=0.5, foreground='lightgray', capstyle="round")]) # contorni
      #print("ciao_s2")
    else:
      plt.axvline(stop_pos[s], color="orange", linewidth=3)
      plt.annotate(accorcia_datetime(stops[s]), [stop_pos[s]-raw.shape[0]/45, 2.15], size=7, rotation=90, color="orange", annotation_clip=False,)
                    #path_effects=[patheffects.withStroke(linewidth=0.5, foreground='lightgray', capstyle="round")]) # contorni
      plt.annotate(accorcia_datetime(riavvii[s]), [stop_pos[s]+raw.shape[0]/160, 2.15], size=7, rotation=90, color="orange", annotation_clip=False,)
                    #path_effects=[patheffects.withStroke(linewidth=0.5, foreground='lightgray', capstyle="round")]) # contorni
      #print("ciao_s3")

  #limiti del grafico
  plt.xlim(-1, raw.shape[0]+1)
  plt.ylim(0,3)

  #print(mezzi_giorni)

  #scritte sull'asse x
  x_ticks = mezzi_pos
  x_labels = mezzi_giorni
  ax.set_xticks(x_ticks, labels=x_labels, size=4)
  fig.autofmt_xdate()
  mpl.rcParams['ytick.labelsize'] = 4

  plt.suptitle(titolo) #aggiunge titolo

  return None


# %%
# prende in input una cartella con dentro file di un singolo mese,
# trova i picchi e li mette tutti in un singolo csv
# e poi fa i grafici dei singoli file
def elabora_mese(cartella, anno, soglia, max_d, df_interruzioni, wiggle, delta, mesi, cartella_meteo):

  df_picchi = pd.DataFrame()

  file_check = False

  mese_str = cartella.split("/")[-2][:2]
  mese_int = int(mese_str)

  try:
    meteo_csv = [x for x in os.listdir(cartella_meteo) if x.endswith(f"{mese_str}.csv")][0]
    meteo_df = pd.read_csv(f"{cartella_meteo}/{meteo_csv}", sep=";", index_col="datetime")
    meteo_df.index = meteo_df.index.map(lambda x: datetime.strptime(x, "%Y-%m-%dT%H:%M:%S+02:00"))
  except:
    print(f"info meteo non trovate per il mese {mese_str}")
    meteo_df = pd.DataFrame(columns=["datetime","aveWDIR","aveWVEL"])

  for f in os.listdir(cartella):

    if f.startswith("aaa"):

      file_name = f.split("_")

      if int(file_name[1]) != anno:
        return f"Errore: file non appartiene all'anno di input o nome non è formattato correttamente: {f}"

      raw, temp_df = trova_picchi(cartella+f, soglia, max_d, meteo_df)
      df_picchi = pd.concat([df_picchi, temp_df])
      file_check = True

      titolo = f"{file_name[3].split(' ')[0]} {mesi[mese_int]} {file_name[1]}"

      #if titolo not in ["21 MAGGIO 2024", "05-06 APRILE 2024", "15-29 FEBBRAIO 2024"]:
        #continue

      mezzi_giorni, mezzi_pos, stops, stop_pos, riavvii = posiziona_verticali(raw, df_interruzioni, wiggle, delta)

      disegnatore(raw, titolo, soglia, mezzi_giorni, mezzi_pos, stops, stop_pos, riavvii)

      #salva grafico creato da disegnatore()
      plt.savefig(f"{cartella}fig_{f[4:-4]}.png", dpi=600)
      plt.close()
    else:
      #print(f"\nignoro file {f} perché non comincia con aaa")
      pass

##################################################################

  if file_check == True:
    df_picchi = df_picchi.reset_index(drop=True)
    df_picchi.to_csv(f"{cartella}Intensità Max Misure Naso {mesi[mese_int]} {file_name[1]}.csv", sep=";")

  return None




# %%
def main(cartella, cartella_meteo, interruzioni, sheet, anno, soglia, max_d, wiggle, delta):
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

  df_interruzioni = recupera_interruzioni(interruzioni, sheet, anno)

  for sub_cartella in os.listdir(cartella):
    temp_path = f"{cartella}/{sub_cartella}/"
    if os.path.isdir(temp_path) and temp_path.endswith(f"{anno}/"):
      em_err = elabora_mese(temp_path, anno, soglia, max_d, df_interruzioni, wiggle, delta, mesi, cartella_meteo)
      if em_err != None:
        print(em_err)


# %%
if __name__ == "__main__":

  cartella = "Simoncelli 2024 MISURE ogni 2-4 gg"
  #cartella = "ogni 4 gg"
  cartella_meteo = "meteo_naso_2024"
  interruzioni = "MISURE-MALFUNZ.-MANUTENZ. PEN3.xlsx"
  #interruzioni = "Fasullo-MALFUNZ.-MANUTENZ. PEN3.xlsx"
  sheet = "misure e interruz"
  anno = 2024
  soglia = 2 # soglia dei segnali affinché vengano considerati come picchi
  max_d = 400 # distanza massima affinché due picchi vengano considerati della stessa curva
  wiggle = 300 # distanza massima tra il momento d'interruzione e un'estremità del grafico affinché l'interruzione venga disegnata alle estremità
  delta = 100 # num di secondi che dura (di solito) una misurazione

  main(cartella, cartella_meteo, interruzioni, sheet, anno, soglia, max_d, wiggle, delta)



