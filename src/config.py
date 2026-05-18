# src/config.py
import os

# Ruta raíz del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Rutas a las carpetas de datos
RAW_PATH = os.path.join(BASE_DIR, 'data', 'raw', 'netflix_titles.csv')
CLEAN_PATH = os.path.join(BASE_DIR, 'data', 'clean', 'netflix_titles_clean.csv')