import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

def autocorrelacion(x):
    """
    Calcula la autocorrelación normalizada de una señal x.
    
    Parámetros:
    x : Señal de entrada.
        
    Devuelve:
    l : Desplazamientos relativos de la autocorrelación (en muestras).
    autocorr : Valores de autocorrelación normalizados.
    """
    l = signal.correlation_lags(len(x), len(x), mode='full')
    autocorr = signal.correlate(x, x, mode='full') / max(signal.correlate(x, x, mode='full'))
    return l, autocorr

import numpy as np
import scipy.signal as signal

def calculo_maximo(l, autocorr, F_s):
    """
    Calcula el máximo de una señal de autocorrelación limitando la búsqueda a una 
    ventana fisiológicamente posible para el período cardíaco (aprox. 40 a 200 lpm).

    Parámetros:
    autocorr : Valores de autocorrelación normalizados.
    l : Desplazamientos relativos de la autocorrelación (en muestras).
    F_s : Frecuencia de muestreo.
        
    Devuelve:
    tiempo_maximo : Valor de tiempo en el que ocurre el primer pico significativo.
    valor_maximo : Valor de la autocorrelación en ese punto.
    """

    t = l / F_s

    # 1. Límites fisiológicos (0.3s a 1.5s)
    min_ppm = 40
    max_ppm = 200

    min_t = 60 / max_ppm
    max_t = 60 / min_ppm
    
    # 2. Recortar la señal a la zona donde sabemos que DEBE estar el latido real
    mascara = (t >= min_t) & (t <= max_t)

    if not np.any(mascara):
        plt.figure(figsize=(12, 6))
        plt.plot(t, autocorr)
        plt.xlabel('Desplazamiento relativo')
        plt.ylabel('Autocorrelación Normalizada')
        plt.grid(True)
        plt.show()
        return np.nan, np.nan
    
    t_ventana = t[mascara]
    autocorr_ventana = autocorr[mascara]
    
    # 3. Encontrar picos solo dentro de esa ventana limpia
    peaks, properties = signal.find_peaks(autocorr_ventana, prominence = 0.05)
    
    # 4. Validar que se hayan encontrado picos
    if len(peaks) > 0:
        # Extraer los valores en Y de los picos encontrados
        valores_picos = autocorr_ventana[peaks]
        
        # Encontrar el valor máximo absoluto en la ventana para establecer un umbral
        max_absoluto = np.max(valores_picos)
        
        # Establecer un umbral (ej. 50% del pico máximo encontrado en la ventana)
        umbral_amplitud = max_absoluto * 0.50
        
        # Filtrar solo los picos que superen este umbral
        picos_validos_idx = np.where(valores_picos >= umbral_amplitud)[0]
        
        if len(picos_validos_idx) > 0:
            # Seleccionar el PRIMER pico que supera el umbral (el período fundamental T)
            idx_seleccionado = picos_validos_idx[0]
        else:
            # Fallback de seguridad por si ningún pico cumple (poco probable)
            idx_seleccionado = np.argmax(valores_picos)
            
        # Mapear ese índice local al índice real dentro de nuestra ventana
        indice_pico_principal = peaks[idx_seleccionado]
        
        # Extraer los resultados finales
        tiempo_maximo = t_ventana[indice_pico_principal]
        valor_maximo = autocorr_ventana[indice_pico_principal]
        
        return tiempo_maximo, valor_maximo
    
    else:
        plt.figure(figsize=(12, 6))
        plt.plot(t, autocorr)
        plt.xlabel('Desplazamiento relativo')
        plt.ylabel('Autocorrelación Normalizada')
        plt.grid(True)
        plt.show()
        return np.nan, np.nan

    
def extraccion(num_sujeto, actividad, inicio, fin):
    df_s_run = pd.read_csv(f"datos_csv\\s{num_sujeto}_{actividad}.csv")
    df_s_run["time"] = pd.to_datetime(df_s_run["time"], format="%Y-%m-%d   %H:%M:%S.%f")

    # Para pasar de datetime a tiempo transcurrido desde el inicio del experimento (df_s_run['time'].iloc[0])
    tiempo_transcurrido = df_s_run['time'] - df_s_run['time'].iloc[0]
    df_s_run['segundos_transcurridos'] = tiempo_transcurrido.dt.total_seconds() # Convierte el tiempo transcurrido a segundos

    # Para filtrar los datos de acuerdo a los segundos de interés
    df_filtrada = df_s_run.query(f"segundos_transcurridos >= {inicio} and segundos_transcurridos <= {fin}")
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

    return df_filtrada

# Recordar que la correlación cruzada funciona mejor para señales bipolares
# l, autocorr = autocorrelacion(ecg - np.mean(ecg))  # Se resta la media para centrar la señal en 0

# periodo_estimado, valor_max_autocorr = calculo_maximo(l/500, autocorr)
    
# print("Desfase relativo del máximo:", periodo_estimado, "segundos")
# print("Valor máximo de la autocorrelación:", valor_max_autocorr)
# print(f"""
# La señal de ECG tiende a parecerse en un {valor_max_autocorr*100:.2f}% cuando el retardo es de {periodo_estimado}s. 
# Este valor de retardo puede interpretarse como el periodo de la señal, lo cual significa 
# que el estimado de pulso para el sujeto {num_sujeto} en las condiciones descritas es de {60/periodo_estimado:.2f}ppm
# (pulsaciones por minuto).""")

# Gráfico de la autocorrelación de la señal ECG
# plt.figure(figsize=(12, 6))
# plt.plot(l/500, autocorr)
# plt.xlabel('Desplazamiento relativo')
# plt.ylabel('Autocorrelación Normalizada')
# plt.title('Autocorrelación de la Señal ECG')
# plt.grid(True)
# plt.show()