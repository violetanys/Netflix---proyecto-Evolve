# main.py
import os
import sys


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

#rutas glovales
from src.config import RAW_PATH, CLEAN_PATH

#  funciones modulares 
from src.io import load_csv
from src.utils import assert_columns
from src.cleaning import clean

def main():
    print(" Iniciando el pipeline de datos de Netflix (Evolve)...")
    
    #-------------------------------------------------------------------------
    # 1. PASO DE CARGA (Input)
    # -------------------------------------------------------------------------
    print("\n[Paso 1/4] Cargando dataset original...")
    df_raw = load_csv(RAW_PATH)
    
    # -------------------------------------------------------------------------
    # 2. PASO DE VALIDACIÓN 
    # -------------------------------------------------------------------------
    print("\n[Paso 2/4] Validando estructura de columnas...")
    columnas_requeridas = ['type', 'title', 'director', 'cast', 'country', 'date_added', 'duration', 'rating']
    assert_columns(df_raw, required=columnas_requeridas)
    print("Estructura validada correctamente.")

    # -------------------------------------------------------------------------
    # 3. PASO DE LIMPIEZA Y FEATURE ENGINEERING (Transform)
    # -------------------------------------------------------------------------
    print("\n[Paso 3/4] Ejecutando transformaciones, imputación de nulos y feature engineering...")
    df_clean = clean(df_raw)
    
    # -------------------------------------------------------------------------
    # 4. PASO DE EXPORTACIÓN (Output)
    # -------------------------------------------------------------------------
    print("\n[Paso 4/4] Exportando dataset procesado a la carpeta clean...")
    # Asegurar que la carpeta destino exista antes de guardar
    os.makedirs(os.path.dirname(CLEAN_PATH), exist_ok=True)
    
    # Guardamos el archivo procesado en la ruta configurada
    df_clean.to_csv(CLEAN_PATH, index=False)
    print(f" Dataset limpio exportado con éxito en: {CLEAN_PATH}")
    print("\n ¡Pipeline ejecutado por completo y de forma reproducible!")

if __name__ == "__main__":
    main()