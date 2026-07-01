def autocorrelacion(x):
    """
    Calcula la autocorrelación normalizada de una señal x.
    
    Parámetros:
    x : Señal de entrada.
        
    Retorna:
    l : Desplazamientos (lags) de la autocorrelación.
    autocorr : Valores de autocorrelación normalizados.
    """
    l = signal.correlation_lags(len(x), len(x), mode='full')
    autocorr = signal.correlate(x, x, mode='full') / max(signal.correlate(x, x, mode='full'))
    return l, autocorr

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

df_s1_run = pd.read_csv("datos_csv\\s10_run.csv")
df_s1_run["time"] = pd.to_datetime(df_s1_run["time"], format="%Y-%m-%d   %H:%M:%S.%f")

# Para pasar de datetime a tiempo transcurrido desde el inicio del experimento (df_s1_run['time'].iloc[0])
tiempo_transcurrido = df_s1_run['time'] - df_s1_run['time'].iloc[0]
df_s1_run['segundos_transcurridos'] = tiempo_transcurrido.dt.total_seconds() # Convierte el tiempo transcurrido a segundos

# Para filtrar los datos de acuerdo a los segundos de interés
df_filtrada = df_s1_run.query("segundos_transcurridos >= 300 and segundos_transcurridos <= 303")
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

# Gráfico de la autocorrelación de la señal ECG
plt.figure(figsize=(12, 6))
plt.plot(l/500, autocorr)
plt.xlabel('Desplazamiento relativo')
plt.ylabel('Autocorrelación Normalizada')
plt.title('Autocorrelación de la Señal ECG')
plt.grid(True)
plt.show()