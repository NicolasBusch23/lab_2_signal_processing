import scipy.signal as signal

def aplicar_filtro_pasabanda(datos, F_s, freq_min, freq_max, orden):
    """
    Aplica un filtro Butterworth pasabanda a una señal de acelerometría.
    
    Parámetros:
    - datos: señal de acelerometría (a_x, a_y o a_z).
    - F_s: frecuencia de muestreo de tu sensor (en Hz).
    - freq_min: límite inferior.
    - freq_max: límite superior.
    - orden: orden del filtro.
    """
    
    # 1. Crear los coeficientes (b, a) del filtro Butterworth
    b, a = signal.butter(orden, [freq_min, freq_max], btype = 'bandpass', fs = F_s)
    
    # 2. Aplicar el filtro a los datos
    datos_filtrados = signal.filtfilt(b, a, datos)
    
    return datos_filtrados