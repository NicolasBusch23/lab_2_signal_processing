import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
import auxiliar as aux
import filtros

F_s =  500 # Frecuencia de muestreo en Hz

# Sujetos de entrenamiento (68% de la base de datos dada)
sujetos_entrenamiento = [1,3,4,5,6,8,9,10,11,12,15,16,17,19,21]

# Clases con las que se pretende asociar las características extraidas de las señales
clases = ["sit", "walk", "run"] # Clases posibles de actividad física

for num_sujeto in sujetos_entrenamiento:

    for actividad in clases:

        df = pd.read_csv(f"datos_csv\\s{num_sujeto}_{actividad}.csv")
        df["time"] = pd.to_datetime(df["time"], format="%Y-%m-%d   %H:%M:%S.%f")

        # Para pasar de datetime a tiempo transcurrido desde el inicio del experimento (df_s['time'].iloc[0])
        tiempo_transcurrido = df['time'] - df['time'].iloc[0]
        df['segundos_transcurridos'] = tiempo_transcurrido.dt.total_seconds() # Convierte el tiempo transcurrido a segundos

        # -- Prueba: En caso de que se desee probar el código para cierto intervalo pequeño:
        # df = df.query(f"segundos_transcurridos >= 20 and segundos_transcurridos <= 30")

        # -- En caso de se desee filtrar señales de acelerometría, TRUE. En caso contrario, FALSE
        desea_filtrar_señales_acelereometria = False

        if desea_filtrar_señales_acelereometria:
            datos = df[["segundos_transcurridos", "ecg"]].copy()

            datos["a_x"] = filtros.aplicar_filtro_pasabanda(df["a_x"], F_s, 
                                                           freq_min = 0.5, freq_max = 10, orden = 4)
            datos["a_y"] = filtros.aplicar_filtro_pasabanda(df["a_y"], F_s, 
                                                           freq_min = 0.5, freq_max = 10, orden = 4)
            datos["a_z"] = filtros.aplicar_filtro_pasabanda(df["a_z"], F_s, 
                                                           freq_min = 0.5, freq_max = 10, orden = 4)

        else:
            datos = df[["segundos_transcurridos", "ecg","a_x", "a_y", "a_z"]].copy()


        datos["a_mag"] = np.sqrt((datos["a_x"]**2 + datos["a_y"]**2 + datos["a_z"]**2))

        # -- Prueba: print(datos.head(10))

        # -- Prueba:
        # plt.figure()
        # plt.plot(datos["segundos_transcurridos"],datos["a_mag"])
        # plt.show()

        ventana = 5 # Duración de la ventana en segundos 
        paso = ventana / 2  # Paso de la ventana (50% de superposición)

        inicio = datos['segundos_transcurridos'].iloc[0]
        fin = inicio + ventana

        caracteristicas = []
        num_ventana = 0

        while True:
            num_ventana += 1 # Cuenta el número de ventana generada
            segmento = datos[(datos['segundos_transcurridos'] >= inicio) & (datos['segundos_transcurridos'] <= fin)]

            t = segmento["segundos_transcurridos"]

            # Para volver las señales bipolares, se resta su media (DUDA)
            a_mag = segmento["a_mag"] - np.mean(segmento["a_mag"].values)
            ecg = segmento["ecg"] - np.mean(segmento["ecg"].values)

            window = signal.windows.hamming(len(segmento))
            a_mag_windowed = a_mag * window
            ecg_windowed = ecg * window

            # -- Extracción de características de la señal de aceleración en magnitud
            media, sd, rms, maximo, minimo, rango, energia, f_dom = aux.caracteristicas_a(a_mag_windowed)

            # -- Extracción de PPM de la señal de ECG
            ppm = aux.ppm(ecg_windowed, F_s)

            # -- Prueba: En caso de que se desee ver las características extraídas de cada ventana.
            # print("----------------------")
            # print("Inicio de la ventana:", inicio)
            # print("Fin de la ventana:", fin)
            # print(f"Ventana: {inicio:.2f}s - {fin:.2f}s")
            # print(f"Media: {media:.4f}")
            # print(f"Desviación estándar: {sd:.4f}")
            # print(f"RMS: {rms:.4f}")
            # print(f"Máximo: {maximo:.4f}")
            # print(f"Mínimo: {minimo:.4f}")
            # print(f"Rango: {rango:.4f}")
            # print(f"Energía: {energia:.4f}")
            # print(f"La mayor concetración de energía se encuentra alrededor de la frecuencia: {f_dom:.4f} Hz")

            # -- Se guarda la información calculada de la ventana
            caracteristicas.append({
            "num_ventana": num_ventana,
            "actividad": actividad,
            "media_a": media,
            "sd_a": sd,
            "rms_a": rms,
            "maximo_a": maximo,
            "minimo_a": minimo,
            "rango_a": rango,
            "energia_a": energia,
            "f_dom_a": f_dom,
            "pppm_ecg": ppm,
            })

            # Para desplazar la ventana 
            inicio += paso
            fin += paso

            if fin > datos['segundos_transcurridos'].max():  # Si la ventana se sale del rango de tiempo de la señal, se detiene el bucle
                break

        # Para incluir las características obtenidas de cada ventana en un solo DataFrame
        df_caracteristicas = pd.DataFrame(caracteristicas)

        # Exporta la informacion en un .csv de acuerdo a la decisión de filtrado de las señales de acelerometría
        if desea_filtrar_señales_acelereometria:
            df_caracteristicas.to_csv(
                f"punto_3/entrenamiento_con_filtro/caracteristicas_s{num_sujeto}_{actividad}.csv",
                index = False)
        else:
            df_caracteristicas.to_csv(
                f"punto_3/entrenamiento_sin_filtro/caracteristicas_s{num_sujeto}_{actividad}.csv",
                index = False)