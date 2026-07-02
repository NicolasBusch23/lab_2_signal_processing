def autocorrelacion(x):
    """
    Calcula la autocorrelación normalizada de una señal x.
    
    Parámetros:
    x : Señal de entrada.
        
    Devuelve:
    l : Desplazamientos (lags) de la autocorrelación.
    autocorr : Valores de autocorrelación normalizados.
    """
    l = signal.correlation_lags(len(x), len(x), mode='full')
    autocorr = signal.correlate(x, x, mode='full') / max(signal.correlate(x, x, mode='full'))
    return l, autocorr

def calculo_maximo(l, autocorr):
    """
    Calcula el máximo de una señal de autocorrelación y en qué desfase relativo ocurre.
    Obs: Esta función excluye el pico de autocorrelación en el desfase 0 (que siempre es 1) y busca el siguiente máximo significativo.

    Parámetros:
    autocorr : Valores de autocorrelación normalizados.
    l : Desplazamientos relativos de la autocorrelación.
        
    Devuelve:
    tiempo_maximo : Valor de tiempo en el que ocurre el máximo de la autocorrelación (diferente al 1).
    valor_maximo : Valor máximo de la autocorrelación (diferente al 1).

    """
    # Encontrar los picos en la autocorrelación
    peaks = signal.find_peaks(autocorr, prominence = 0.1)

    list_posicion_pico = []
    list_valores_pico = []
    centinela = False

    for i in range(len(peaks[0])):
        valor_pico = autocorr[peaks[0][i]]
        posicion_pico = l[peaks[0][i]]
        
        # Para excluir aquellos picos que ocurren en desfases negativos y en el desfase 1
        if valor_pico == 1: 
            centinela = True
            continue # El pico == 1, no se considerará

        if centinela == True:
            list_posicion_pico.append(posicion_pico)
            list_valores_pico.append(valor_pico)
    
    valor_maximo = max(list_valores_pico)
    indice_maximo = list_valores_pico.index(valor_maximo)

    tiempo_maximo = list_posicion_pico[indice_maximo]

    return tiempo_maximo, valor_maximo


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

num_sujeto = input("Ingrese el número de sujeto que desea analizar: ")

df_s_run = pd.read_csv(f"datos_csv\\s{num_sujeto}_run.csv")
df_s_run["time"] = pd.to_datetime(df_s_run["time"], format="%Y-%m-%d   %H:%M:%S.%f")

# Para pasar de datetime a tiempo transcurrido desde el inicio del experimento (df_s_run['time'].iloc[0])
tiempo_transcurrido = df_s_run['time'] - df_s_run['time'].iloc[0]
df_s_run['segundos_transcurridos'] = tiempo_transcurrido.dt.total_seconds() # Convierte el tiempo transcurrido a segundos

# Para filtrar los datos de acuerdo a los segundos de interés
df_filtrada = df_s_run.query("segundos_transcurridos >= 300")
t = df_filtrada['segundos_transcurridos']
ecg = df_filtrada['ecg']

# Gráfico de la señal ECG vs tiempo
plt.figure(figsize=(12, 6))
plt.plot(t, ecg)
plt.xlabel('Tiempo (s)')
plt.ylabel('ECG')
plt.title('Señal ECG vs Tiempo')
plt.grid(True)
plt.show()

# Recordar que la correlación cruzada funciona mejor para señales bipolares
l, autocorr = autocorrelacion(ecg - np.mean(ecg))  # Se resta la media para centrar la señal en 0

periodo_estimado, valor_max_autocorr = calculo_maximo(l/500, autocorr)
    
print("Desfase relativo del máximo:", periodo_estimado, "segundos")
print("Valor máximo de la autocorrelación:", valor_max_autocorr)
print(f"""
La señal de ECG tiende a parecerse en un {valor_max_autocorr*100:.2f}% cuando el retardo es de {periodo_estimado}s. 
Este valor de retardo puede interpretarse como el periodo de la señal, lo cual significa 
que el estimado de pulso para el sujeto {num_sujeto} en las condiciones descritas es de {60/periodo_estimado:.2f}ppm
(pulsaciones por minuto).""")

# Gráfico de la autocorrelación de la señal ECG
plt.figure(figsize=(12, 6))
plt.plot(l/500, autocorr)
plt.xlabel('Desplazamiento relativo')
plt.ylabel('Autocorrelación Normalizada')
plt.title('Autocorrelación de la Señal ECG')
plt.grid(True)
plt.show()