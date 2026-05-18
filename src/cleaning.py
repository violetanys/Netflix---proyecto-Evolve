# src/cleaning.py
import pandas as pd
import numpy as np

def clean(df: pd.DataFrame) -> pd.DataFrame:
    """
    Función de limpieza completa para el dataset de Netflix.
    Resuelve: Nulos, fechas, duraciones y tipos de datos.
    """
    # Trabajamos sobre una copia para no afectar al original
    df = df.copy()
    
    # 1. TRATAMIENTO DE VALORES NULOS (The "Dirty" Part)
    # Director, Reparto y País tienen muchos nulos. Los marcamos como desconocidos.
    df['director'] = df['director'].fillna('Unknown Director')
    df['cast'] = df['cast'].fillna('Unknown Cast')
    df['country'] = df['country'].fillna('Unknown Country')
    
    # Rating tiene pocos nulos, los rellenamos con la moda (el valor más común)
    if df['rating'].isnull().any():
        df['rating'] = df['rating'].fillna(df['rating'].mode()[0])
        
    # 2. TRANSFORMACIÓN DE FECHAS
    # 'date_added' viene como "September 25, 2021". Lo pasamos a formato fecha real.
    df['date_added'] = pd.to_datetime(df['date_added'].str.strip(), errors='coerce')
    
    # Creamos columnas nuevas (Feature Engineering) para el análisis temporal
    df['year_added'] = df['date_added'].dt.year.astype('Int64')
    df['month_added'] = df['date_added'].dt.month_name()
    
    # 3. LIMPIEZA DE LA COLUMNA DURATION
    # Separamos el número de la unidad (ej: "90 min" -> 90 | "2 Seasons" -> 2)
    df['duration_num'] = df['duration'].str.extract(r'(\d+)').astype(float)
    df['duration_unit'] = df['duration'].str.extract(r'([a-zA-Z]+)')
    
    # 4. LIMPIEZA DE CATEGORÍAS (listed_in)
    # Algunos géneros tienen espacios extra, los limpiamos
    df['listed_in'] = df['listed_in'].str.strip()
    
    # 5. ELIMINACIÓN DE DUPLICADOS (Si los hubiera)
    df = df.drop_duplicates()
    
    print(f"🧹 Datos limpios y procesados. Registros finales: {df.shape[0]}")
    return df# src/cleaning.py
import pandas as pd
import numpy as np

def clean(df: pd.DataFrame) -> pd.DataFrame:
    """
    Función de limpieza completa para el dataset de Netflix.
    Resuelve: Nulos, fechas, duraciones y tipos de datos.
    """
    # Trabajamos sobre una copia para no afectar al original
    df = df.copy()
    
    # 1. TRATAMIENTO DE VALORES NULOS (The "Dirty" Part)
    # Director, Reparto y País tienen muchos nulos. Los marcamos como desconocidos.
    df['director'] = df['director'].fillna('Unknown Director')
    df['cast'] = df['cast'].fillna('Unknown Cast')
    df['country'] = df['country'].fillna('Unknown Country')
    
    # Rating tiene pocos nulos, los rellenamos con la moda (el valor más común)
    if df['rating'].isnull().any():
        df['rating'] = df['rating'].fillna(df['rating'].mode()[0])
        
    # 2. TRANSFORMACIÓN DE FECHAS
    # 'date_added' viene como "September 25, 2021". Lo pasamos a formato fecha real.
    df['date_added'] = pd.to_datetime(df['date_added'].str.strip(), errors='coerce')
    
    # Creamos columnas nuevas (Feature Engineering) para el análisis temporal
    df['year_added'] = df['date_added'].dt.year.astype('Int64')
    df['month_added'] = df['date_added'].dt.month_name()
    
    # 3. LIMPIEZA DE LA COLUMNA DURATION
    # Separamos el número de la unidad (ej: "90 min" -> 90 | "2 Seasons" -> 2)
    df['duration_num'] = df['duration'].str.extract(r'(\d+)').astype(float)
    df['duration_unit'] = df['duration'].str.extract(r'([a-zA-Z]+)')
    
    # 4. LIMPIEZA DE CATEGORÍAS (listed_in)
    # Algunos géneros tienen espacios extra, los limpiamos
    df['listed_in'] = df['listed_in'].str.strip()
    
    # 5. ELIMINACIÓN DE DUPLICADOS (Si los hubiera)
    df = df.drop_duplicates()
    
    print(f"🧹 Datos limpios y procesados. Registros finales: {df.shape[0]}")
    return df