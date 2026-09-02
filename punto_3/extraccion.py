import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
import auxiliar as aux
import filtros

F_s =  500 # Frecuencia de muestreo en Hz

sujetos = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22]

# Clases con las que se pretende asociar las características extraidas de las señales
clases = ["sit", "walk", "run"] # Clases posibles de actividad física

for num_sujeto in sujetos:

    for actividad in clases:

        df = pd.read_csv(f"datos_csv\\s{num_sujeto}_{actividad}.csv")
        df["time"] = pd.to_datetime(df["time"], format="%Y-%m-%d   %H:%M:%S.%f")

        # Para pasar de datetime a tiempo transcurrido desde el inicio del experimento (df_s['time'].iloc[0])
        tiempo_transcurrido = df['time'] - df['time'].iloc[0]
        df['segundos_transcurridos'] = tiempo_transcurrido.dt.total_seconds() # Convierte el tiempo transcurrido a segundos

        # -- Prueba: En caso de que se desee probar el código para cierto intervalo pequeño:
        # df = df.query(f"segundos_transcurridos >= 20 and segundos_transcurridos <= 30")

        datos = df[["segundos_transcurridos", "ecg", "a_x", "a_y", "a_z"]].copy()

        # -- En caso de se desee filtrar señales de acelerometría, TRUE. En caso contrario, FALSE
        desea_filtrar_señales_acelerometria = False

        # -- En caso de se desee filtrar ECG, TRUE. En caso contrario, FALSE
        desea_filtrar_señal_ecg = True

        if desea_filtrar_señales_acelerometria:
            datos["a_x"] = filtros.aplicar_filtro_pasabanda(df["a_x"], F_s, 
                                                           freq_min = 0.5, freq_max = 20, orden = 6)
            datos["a_y"] = filtros.aplicar_filtro_pasabanda(df["a_y"], F_s, 
                                                           freq_min = 0.5, freq_max = 20, orden = 6)
            datos["a_z"] = filtros.aplicar_filtro_pasabanda(df["a_z"], F_s, 
                                                           freq_min = 0.5, freq_max = 20, orden = 6)
        elif desea_filtrar_señal_ecg:
            datos["ecg"] = filtros.aplicar_filtro_pasabanda(df["ecg"], F_s, 
                                                           freq_min = 0.5, freq_max = 150, orden = 6)


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
            print(f"---- Número de Ventana: {num_ventana} para s_{num_sujeto}_{actividad}. Duración: {inicio} - {fin}")
            segmento = datos[(datos['segundos_transcurridos'] >= inicio) & (datos['segundos_transcurridos'] <= fin)]

            t = segmento["segundos_transcurridos"]

            a_mag = segmento["a_mag"]
            
            # Para volver las señales bipolares, se resta su media
            # a_mag = segmento["a_mag"] - np.mean(segmento["a_mag"])
            ecg = segmento["ecg"] - np.mean(segmento["ecg"].values)

            # -- Prueba: Para ver el ECG
            # plt.figure()
            # plt.plot(t, ecg)
            # plt.xlabel('Tiempo (s)')
            # plt.ylabel('ECG')
            # plt.title(f"Señal ECG vs Tiempo para el sujeto {num_sujeto}")
            # plt.grid(True)
            # plt.show()

            window = signal.windows.hamming(len(segmento))
            a_mag_windowed = (a_mag * window) + np.mean(segmento["a_mag"])
            ecg_windowed = ecg * window

            # -- Prueba: Para ver el ECG del incoveniente en s_5_sit (240s - 245s)
            # if num_ventana == 97 and num_sujeto == 5 and actividad == 'sit':
            #     plt.figure()
            #     plt.plot(t, ecg_windowed)
            #     plt.xlabel('Tiempo (s)')
            #     plt.ylabel('ECG')
            #     plt.title(f'Señal ECG vs Tiempo para el sujeto {num_sujeto} (Ventana: {inicio:.2f}s - {fin:.2f}s)')
            #     plt.grid(True)
            #     plt.show()

            # -- Prueba: Para ver el ECG del incoveniente en s_16_run (212.5s - 217.5s)
            # if num_ventana == 86 and num_sujeto == 16 and actividad == 'run':
            #     plt.figure()
            #     plt.plot(t, ecg_windowed)
            #     plt.xlabel('Tiempo (s)')
            #     plt.ylabel('ECG')
            #     plt.title(f'Señal ECG vs Tiempo para el sujeto {num_sujeto} (Ventana: {inicio:.2f}s - {fin:.2f}s)')
            #     plt.grid(True)
            #     plt.show()

            # -- Extracción de características de la señal de aceleración en magnitud
            media, sd, rms, maximo, minimo, rango, energia, f_dom, energia_f_dom = aux.caracteristicas_a(a_mag_windowed, F_s)

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
            "num_sujeto": num_sujeto,
            "actividad": actividad,
            "media_a": media,
            "sd_a": sd,
            "rms_a": rms,
            "maximo_a": maximo,
            "minimo_a": minimo,
            "rango_a": rango,
            "energia_a": energia,
            "f_dom_a": f_dom,
            "energia_f_dom_a": energia_f_dom,
            "ppm_ecg": ppm
            })

            # Para desplazar la ventana 
            inicio += paso
            fin += paso

            if fin > datos['segundos_transcurridos'].max():  # Si la ventana se sale del rango de tiempo de la señal, se detiene el bucle
                break

        # Para incluir las características obtenidas de cada ventana en un solo DataFrame
        # df_caracteristicas = pd.DataFrame(caracteristicas)

        # Exporta la informacion en un .csv de acuerdo a la decisión de filtrado de las señales de acelerometría
        # df_caracteristicas.to_csv(s
        #     f"punto_3/extraccion/caracteristicas_s{num_sujeto}_{actividad}.csv",
        #     index = False)