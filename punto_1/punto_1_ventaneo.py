import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import punto_1 as p1

num_sujeto = input("Ingrese el número de sujeto que desea analizar: ")
inicio = float(input("Ingrese el tiempo de inicio (en segundos): "))
fin = float(input("Ingrese el tiempo de fin (en segundos): "))
actividad = input("Ingrese la actividad que desea analizar (sit, walk, run): ")

df_filtrada = p1.extraccion(num_sujeto, actividad, inicio, fin)

ventana = 5  # Duración de la ventana en segundos 
paso = ventana / 2  # Paso de la ventana (50% de superposición)

# Listas vacías para guardar los resultados finales del gráfico
tiempos_grafico = []
frecuencias_ppm = []

inicio = df_filtrada['segundos_transcurridos'].iloc[0]
fin = inicio + ventana

while True:
    segmento = df_filtrada[(df_filtrada['segundos_transcurridos'] >= inicio) & (df_filtrada['segundos_transcurridos'] < fin)]

    fs = 500  
    b, a = signal.butter(2, 0.7 / (fs / 2), btype='highpass')

    plt.figure(figsize=(12, 6))
    plt.plot(segmento['segundos_transcurridos'], segmento['ecg'])
    plt.xlabel('Tiempo (s)')
    plt.ylabel('ECG')
    plt.title(f'Señal ECG vs Tiempo para el sujeto {num_sujeto} (Ventana: {inicio:.2f}s - {fin:.2f}s)')
    plt.grid(True)
    plt.show()

    # Filtrar el segmento sin media
    # segmento_filtrado = signal.filtfilt(b, a, segmento['ecg'].values - np.mean(segmento['ecg'].values))
    segmento_filtrado = segmento['ecg'].values - np.mean(segmento['ecg'].values)

    plt.figure(figsize=(12, 6))
    plt.plot(segmento['segundos_transcurridos'], segmento_filtrado)
    plt.xlabel('Tiempo (s)')
    plt.ylabel('ECG')
    plt.title(f'Señal FILTRADA ECG vs Tiempo para el sujeto {num_sujeto} (Ventana: {inicio:.2f}s - {fin:.2f}s)')
    plt.grid(True)
    plt.show()

    window = signal.windows.hamming(len(segmento))
    segmento_windowed = segmento_filtrado * window

    plt.figure(figsize=(12, 6))
    plt.plot(segmento['segundos_transcurridos'], segmento_windowed)
    plt.xlabel('Tiempo (s)')
    plt.ylabel('ECG (Ventana Hamming)')
    plt.title(f'Señal ECG con Ventana Hamming para el sujeto {num_sujeto} (Ventana: {inicio:.2f}s - {fin:.2f}s)')
    plt.grid(True)
    plt.show()

    l, autocorr = p1.autocorrelacion(segmento_windowed - np.mean(segmento_windowed))  # Se resta la media para centrar la señal en 0
    periodo_estimado, valor_max_autocorr = p1.calculo_maximo(l/500, autocorr)

    # Gráfico de la autocorrelación de la señal ECG
    plt.figure(figsize=(12, 6))
    plt.plot(l/500, autocorr)
    plt.xlabel('Desplazamiento relativo')
    plt.ylabel('Autocorrelación Normalizada')
    plt.title('Autocorrelación de la Señal ECG')
    plt.grid(True)
    plt.show()

    print("Desfase relativo del máximo:", periodo_estimado, "segundos")
    print("Valor máximo de la autocorrelación:", valor_max_autocorr)
    print(f"""
    La señal de ECG tiende a parecerse en un {valor_max_autocorr*100:.2f}% cuando el retardo es de {periodo_estimado}s. 
    Este valor de retardo puede interpretarse como el periodo de la señal, lo cual significa 
    que el estimado de pulso para el sujeto {num_sujeto} en las condiciones descritas es de {60/periodo_estimado:.2f}ppm
    (pulsaciones por minuto).""")


    centro_ventana = inicio + (ventana / 2)
    tiempos_grafico.append(centro_ventana)

    ppm = 60 / periodo_estimado

    frecuencias_ppm.append(ppm)   # Guardar el pulso calculado
    
    # Para desplazar la ventana 
    inicio += paso
    print("Inicio de la ventana:", inicio)
    fin += paso
    print("Fin de la ventana:", fin)

    if fin > df_filtrada['segundos_transcurridos'].max():  # Si la ventana se sale del rango de tiempo de la señal, se detiene el bucle
        break

# Gráfico del pulso estimado vs tiempo
plt.figure(figsize=(12, 6))
plt.plot(tiempos_grafico, frecuencias_ppm)
plt.xlabel('Tiempo (s)')
plt.ylabel('Pulso estimado (ppm)')
plt.title(f'Pulso estimado vs Tiempo para el sujeto {num_sujeto}')
plt.grid(True)
plt.show()