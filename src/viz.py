import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Configuración estética global para cumplir con la alta relación dato/tinta
sns.set_theme(style="white")
NETFLIX_RED = "#E50914"
NEUTRAL_GRAY = "#4E4E4E"

def plot_content_type(df):
    """Pregunta 1: Proporción de Películas vs Series"""
    plt.figure(figsize=(7, 5))
    ax = sns.countplot(
        data=df, 
        x='type', 
        palette=[NETFLIX_RED, NEUTRAL_GRAY],
        hue='type',
        legend=False
    )
    
    # Añadir etiquetas de conteo sobre las barras
    for p in ax.patches:
        ax.annotate(f'{int(p.get_height())}', 
                    (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha='center', va='baseline', fontsize=11, color='black', xytext=(0, 5),
                    textcoords='offset points')
                    
    plt.title("Distribución del Catálogo Histórico de Netflix", fontsize=14, pad=15, weight='bold')
    plt.xlabel("Tipo de Contenido", fontsize=12)
    plt.ylabel("Cantidad de Títulos", fontsize=12)
    sns.despine()
    plt.tight_layout()
    
    # Guardado único para el Gráfico 1
    plt.savefig('../reports/visualizaciones/1_tipo_contenido.png', dpi=300)
    plt.show()

def plot_movie_duration(df):
    """Pregunta 2: Distribución de la duración de películas"""
    # Filtrar solo películas y asegurar que la duración sea numérica
    movies = df[df['type'] == 'Movie'].dropna(subset=['duration_num'])
    
    plt.figure(figsize=(9, 5))
    sns.histplot(
        data=movies, 
        x='duration_num', 
        kde=True, 
        color=NETFLIX_RED, 
        bins=30
    )
    
    plt.title("Distribución de la Duración de las Películas (Minutos)", fontsize=14, pad=15, weight='bold')
    plt.xlabel("Duración (minutos)", fontsize=12)
    plt.ylabel("Frecuencia", fontsize=12)
    sns.despine()
    plt.tight_layout()
    
    # Guardado único para el Gráfico 2
    plt.savefig('../reports/visualizaciones/2_distribucion_duracion.png', dpi=300)
    plt.show()

def plot_top_countries(df):
    """Pregunta 3: Top 5 países productores (excluyendo Unknown)"""
    # Filtrar Unknown y obtener los 5 principales países
    filtered_df = df[df['country'] != 'Unknown']
    top_countries = filtered_df['country'].value_counts().head(5)
    
    plt.figure(figsize=(9, 5))
    ax = sns.barplot(
        x=top_countries.values, 
        y=top_countries.index, 
        hue=top_countries.index,
        palette="Greys_r",
        legend=False
    )
    
    # Resaltar el líder (primer elemento) pintándolo de rojo Netflix
    ax.patches[0].set_facecolor(NETFLIX_RED)
    
    # Añadir valores al final de las barras horizontales
    for i, v in enumerate(top_countries.values):
        ax.text(v + 20, i, f" {v}", va='center', fontsize=10, weight='bold')
        
    plt.title("Top 5 Países Líderes en Producción de Contenido", fontsize=14, pad=15, weight='bold')
    plt.xlabel("Cantidad Total de Títulos", fontsize=12)
    plt.ylabel("País", fontsize=12)
    sns.despine()
    plt.tight_layout()
    
    # Guardado único para el Gráfico 3
    plt.savefig('../reports/visualizaciones/3_top_paises.png', dpi=300)
    plt.show()

def plot_seasonality(df):
    """Pregunta 4: Estacionalidad por meses (Lanzamientos)"""
    # Asegurar orden cronológico de los meses
    months_order = [
        'January', 'February', 'March', 'April', 'May', 'June', 
        'July', 'August', 'September', 'October', 'November', 'December'
    ]
    
    # Filtrar nulos en los meses y contar
    df_months = df.dropna(subset=['month_added'])
    monthly_counts = df_months['month_added'].value_counts().reindex(months_order)
    
    plt.figure(figsize=(10, 5))
    ax = sns.barplot(
        x=monthly_counts.index, 
        y=monthly_counts.values, 
        hue=monthly_counts.index,
        color=NEUTRAL_GRAY,
        legend=False
    )
    
    # Resaltar visualmente la barra con el valor máximo pintándola de rojo
    max_idx = monthly_counts.values.argmax()
    ax.patches[max_idx].set_facecolor(NETFLIX_RED)
    
    plt.title("Estacionalidad: Volumen de Contenido Añadido por Mes", fontsize=14, pad=15, weight='bold')
    plt.xlabel("Mes del Año", fontsize=12)
    plt.ylabel("Cantidad de Títulos", fontsize=12)
    plt.xticks(rotation=45)
    sns.despine()
    plt.tight_layout()
    
    # Guardado único para el Gráfico 4
    plt.savefig('../reports/visualizaciones/4_estacionalidad_meses.png', dpi=300)
    plt.show()

def plot_evolution(df):
    """Pregunta 5: Evolución temporal de Películas vs Series"""
    # Agrupar por año de adición y tipo de contenido, filtrando años lógicos (ej. desde 2008)
    evolution = df[df['year_added'] >= 2008].groupby(['year_added', 'type']).size().reset_index(name='count')
    
    plt.figure(figsize=(10, 5))
    sns.lineplot(
        data=evolution, 
        x='year_added', 
        y='count', 
        hue='type', 
        palette=[NETFLIX_RED, NEUTRAL_GRAY], 
        style='type', 
        markers=True, 
        dashes=False,
        linewidth=2.5
    )
    
    plt.title("Evolución Temporal del Catálogo (Adiciones Anuales)", fontsize=14, pad=15, weight='bold')
    plt.xlabel("Año de Adición a la Plataforma", fontsize=12)
    plt.ylabel("Cantidad de Títulos Añadidos", fontsize=12)
    plt.legend(title="Tipo de Contenido")
    sns.despine()
    plt.tight_layout()
    
    # Guardado único para el Gráfico 5
    plt.savefig('../reports/visualizaciones/5_evolucion_temporal.png', dpi=300)
    plt.show()