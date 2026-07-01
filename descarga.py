import os
import requests

url_base = "https://physionet.org/files/pulse-transit-time-ppg/1.1.0/csv/"
os.makedirs("./datos_csv", exist_ok=True)

archivos = [f"s{i}_{a}.csv" for i in range(1, 23) for a in ["sit", "walk", "run"]] + ["subjects_info.csv"]

for i, nom in enumerate(archivos, 1):
    print(f"[{i}/67] Descargando {nom}...", flush=True)
    res = requests.get(url_base + nom, stream=True)
    
    if res.status_code == 200:
        with open(f"./datos_csv/{nom}", "wb") as f:
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