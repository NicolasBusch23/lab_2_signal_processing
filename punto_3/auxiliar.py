from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
import punto_1.punto_1 as p1

f_s =   500 # Frecuencia de muestreo en Hz

def caracteristicas_a(datos):

    # Características de la señal de aceleración en magnitud
    media = datos.mean()
    sd = datos.std()
    rms = np.sqrt(np.mean(datos**2))
    maximo = datos.max()
    minimo = datos.min()
    rango = maximo - minimo
    energia = np.sum(datos**2)

    n = len(datos)

    frec = np.fft.rfftfreq(n, d = 1/f_s)  # Frecuencias de la FFT
    fft = np.abs(np.fft.rfft(datos))
    espectro_energia = fft**2 

    # 1. Ignorar las frecuencias menores a 0.5 Hz (Elimina el pico de gravedad en 0 Hz)
    indices_validos = np.where(frec > 0.5)[0] 
    
    # Si la ventana es muy corta y no hay frecuencias > 0.5, evitamos un error
    if len(indices_validos) > 0:
        frec_validas = frec[indices_validos]
        espectro_energia_valido = espectro_energia[indices_validos]

        # 2. Buscar directamente el índice del valor máximo
        indice_max = np.argmax(espectro_energia_valido)
        
        # 3. Extraer la frecuencia dominante
        f_dom = frec_validas[indice_max]
    else:
        f_dom = 0.0 # Valor por defecto si algo falla

    # Gráfica para comprobación visual
    plt.figure()
    plt.plot(frec, espectro_energia)
    # Marcar el pico dominante en la gráfica con un punto rojo
    plt.plot(f_dom, espectro_energia_valido[indice_max], 'ro', label=f'F. Dom: {f_dom:.2f} Hz')
    plt.title('Espectro de Energía de la Señal de Aceleración')
    plt.xlabel('Frecuencia (Hz)')
    plt.ylabel('Espectro de Energía')
    plt.xlim(0, 10) # Te sugiero hacer zoom a los primeros 10 Hz, el movimiento humano no pasa de ahí
    plt.legend()
    plt.show()

    # Recuerda retornar la f_dom para poder usarla en tu clasificador
    return media, sd, rms, maximo, minimo, rango, energia, f_dom

def ppm(datos, F_s):
    l, autocorr = p1.autocorrelacion(datos - np.mean(datos))  # Se resta la media para centrar la señal en 0
    periodo_estimado, valor_max_autocorr = p1.calculo_maximo(l/F_s, autocorr)

    # Gráfico de la autocorrelación de la señal ECG
    # plt.figure(figsize=(12, 6))
    # plt.plot(l/F_s, autocorr)
    # plt.xlabel('Desplazamiento relativo')
    # plt.ylabel('Autocorrelación Normalizada')
    # plt.title('Autocorrelación de la Señal ECG')
    # plt.grid(True)
    # plt.show()

    ppm = 60 / periodo_estimado

    # print("Desfase relativo del máximo:", periodo_estimado, "segundos")
    # print("Valor máximo de la autocorrelación:", valor_max_autocorr)
    # print(f"""
    # La señal de ECG tiende a parecerse en un {valor_max_autocorr*100:.2f}% cuando el retardo es de {periodo_estimado}s. 
    # Este valor de retardo puede interpretarse como el periodo de la señal, lo cual significa 
    # que el estimado de pulso para el sujeto en las condiciones descritas es de {ppm:.2f} ppm
    # (pulsaciones por minuto).""")

    return ppm