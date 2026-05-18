# src/io.py
import pandas as pd
import os

def load_csv(ruta_archivo):
    """
    Carga el dataset de Netflix en un DataFrame de Pandas.
    """
    if not os.path.exists(ruta_archivo):
        raise FileNotFoundError(f"No se encontró ningún archivo en: {ruta_archivo}")
    
    df = pd.read_csv(ruta_archivo)
    print(f"✅ Archivo cargado con éxito. Registros: {df.shape[0]}, Columnas: {df.shape[1]}")
    return df
