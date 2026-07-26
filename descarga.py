import os
import requests

url_base = "https://physionet.org/files/pulse-transit-time-ppg/1.1.0/csv/"
carpeta_destino = "./datos_csv"
os.makedirs(carpeta_destino, exist_ok=True)

archivos = [f"s{i}_{a}.csv" for i in range(1, 23) for a in ["sit", "walk", "run"]] + ["subjects_info.csv"]

for i, nom in enumerate(archivos, 1):
    ruta_archivo = f"{carpeta_destino}/{nom}"
    
    # Comprueba si el archivo ya existe en la carpeta
    if os.path.exists(ruta_archivo):
        print(f"[{i}/{len(archivos)}] {nom} ya existe. Omitiendo...", flush=True)
        continue  # Salta a la siguiente iteración del ciclo

    print(f"[{i}/{len(archivos)}] Descargando {nom}...", flush=True)
    res = requests.get(url_base + nom, stream=True)
    
    if res.status_code == 200:
        with open(ruta_archivo, "wb") as f:
            descargado = 0
            # Lee y escribe en bloques de 1 MB
            for bloque in res.iter_content(chunk_size=1024 * 1024):
                if bloque:
                    f.write(bloque)
                    descargado += len(bloque)
                    # Muestra los MB descargados en la misma línea
                    print(f"\r    Progreso: {descargado / (1024*1024):.1f} MB", end="", flush=True)
        print("\n    ¡Completado!")
    else:
        print(f"    Error {res.status_code}")