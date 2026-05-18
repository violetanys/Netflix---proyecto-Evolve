# src/viz.py
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Configuramos un estilo base limpio para todas las gráficas
sns.set_theme(style="white")

def plot_content_type(df: pd.DataFrame):
    """
    Pregunta 1: ¿El catálogo está dominado por películas o series?
    Tipo de gráfico: Conteo / Barras verticales.
    """
    fig, ax = plt.subplots(figsize=(6, 4.5))
    colores = ['#E50914', '#4E4E4E'] # Rojo Netflix y Gris oscuro
    
    sns.countplot(
        data=df, 
        x='type', 
        ax=ax, 
        palette=colores, 
        order=df['type'].value_counts().index,
        hue='type',
        legend=False
    )
    
    ax.set_title('Catálogo de Netflix: ¿Predominan Películas o Series?', fontsize=12, pad=15, fontweight='bold')
    ax.set_xlabel('Tipo de Contenido', fontsize=10, labelpad=8)
    ax.set_ylabel('Cantidad Registrada', fontsize=10, labelpad=8)
    
    sns.despine() # Quita bordes superior y derecho
    
    # Añadir etiquetas sobre las barras
    for p in ax.patches:
        ax.annotate(f'{int(p.get_height()):,}', 
                    (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha='center', va='center', xytext=(0, 8), 
                    textcoords='offset points', fontsize=9, fontweight='bold')
    
    plt.tight_layout()
    plt.show()


def plot_movie_duration(df: pd.DataFrame):
    """
    Pregunta 2: ¿Cuál es la duración promedio de las películas y cómo se distribuye?
    Tipo de gráfico: Histograma con curva de densidad (KDE).
    """
    # Filtramos solo las películas y nos aseguramos de que no haya nulos en duration_num
    movies_df = df[(df['type'] == 'Movie') & (df['duration_num'].notnull())]
    
    fig, ax = plt.subplots(figsize=(7, 4.5))
    
    sns.histplot(
        data=movies_df, 
        x='duration_num', 
        kde=True, 
        ax=ax, 
        color='#E50914', 
        bins=30,
        edgecolor='white'
    )
    
    ax.set_title('Distribución de la Duración de las Películas en Netflix', fontsize=12, pad=15, fontweight='bold')
    ax.set_xlabel('Duración (minutos)', fontsize=10, labelpad=8)
    ax.set_ylabel('Frecuencia (Cantidad)', fontsize=10, labelpad=8)
    
    sns.despine()
    plt.tight_layout()
    plt.show()


def plot_top_countries(df: pd.DataFrame):
    """
    Pregunta 3: ¿Cuáles son los 5 países que más contenido producen?
    Tipo de gráfico: Barras horizontales (ideal para leer nombres largos).
    """
    # Quitamos 'Unknown Country' para ver los países reales productores
    df_filtered = df[df['country'] != 'Unknown Country']
    
    # Obtenemos el top 5 de países
    top_5 = df_filtered['country'].value_counts().head(5)
    
    fig, ax = plt.subplots(figsize=(7, 4.5))
    
    sns.barplot(
        x=top_5.values, 
        y=top_5.index, 
        ax=ax, 
        palette='Reds_r', # Degradado de rojos
        hue=top_5.index,
        legend=False
    )
    
    ax.set_title('Top 5 Países Productores de Contenido en Netflix', fontsize=12, pad=15, fontweight='bold')
    ax.set_xlabel('Cantidad Total de Títulos', fontsize=10, labelpad=8)
    ax.set_ylabel('País', fontsize=10, labelpad=8)
    
    sns.despine()
    
    # Añadir valores al final de cada barra horizontal
    for i, v in enumerate(top_5.values):
        ax.text(v + 15, i, f'{int(v):,}', va='center', fontsize=9, fontweight='bold')
        
    plt.tight_layout()
    plt.show()


def plot_seasonality(df: pd.DataFrame):
    """
    Pregunta 4: ¿En qué meses del año se suele incorporar más contenido?
    Tipo de gráfico: Barras verticales ordenadas por calendario.
    """
    # Nos aseguramos de quitar filas sin mes
    df_filtered = df[df['month_added'].notnull()]
    
    # Orden cronológico estándar de los meses
    orden_meses = ['January', 'February', 'March', 'April', 'May', 'June', 
                   'July', 'August', 'September', 'October', 'November', 'December']
    
    conteo_meses = df_filtered['month_added'].value_counts().reindex(orden_meses)
    
    fig, ax = plt.subplots(figsize=(9, 4.5))
    
    sns.barplot(
        x=conteo_meses.index, 
        y=conteo_meses.values, 
        ax=ax, 
        color='#4E4E4E', # Gris neutro para resaltar tendencias sin saturar
    )
    
    # Destacamos el mes con más lanzamientos pintándolo de rojo
    max_idx = conteo_meses.values.argmax()
    ax.patches[max_idx].set_facecolor('#E50914')
    
    ax.set_title('Estacionalidad: Lanzamientos por Mes en Netflix', fontsize=12, pad=15, fontweight='bold')
    ax.set_xlabel('Mes de Adición', fontsize=10, labelpad=8)
    ax.set_ylabel('Títulos Lanzados', fontsize=10, labelpad=8)
    
    # Rotamos ligeramente los nombres para que queden bien espaciados
    plt.xticks(rotation=30)
    
    sns.despine()
    plt.tight_layout()
    plt.show()


def plot_evolution(df: pd.DataFrame):
    """
    Pregunta 5: ¿Cómo ha evolucionado la adición de Películas vs Series a lo largo de los años?
    Tipo de gráfico: Gráfico de líneas temporal (Series temporales).
    """
    # Filtramos a partir de 2008 (cuando Netflix empezó a meter contenido digital constante)
    df_filtered = df[(df['year_added'].notnull()) & (df['year_added'] >= 2008)]
    
    # Agrupamos por año y tipo para contar los registros
    evolucion = df_filtered.groupby(['year_added', 'type']).size().reset_index(name='count')
    
    fig, ax = plt.subplots(figsize=(8, 4.5))
    colores = {'Movie': '#E50914', 'TV Show': '#4E4E4E'}
    
    sns.lineplot(
        data=evolucion, 
        x='year_added', 
        y='count', 
        hue='type', 
        ax=ax, 
        palette=colores, 
        linewidth=2.5,
        marker='o' # Añade un punto en cada año para marcar el dato exacto
    )
    
    ax.set_title('Evolución Temporal: Películas vs Series Añadidas', fontsize=12, pad=15, fontweight='bold')
    ax.set_xlabel('Año de Adición a la Plataforma', fontsize=10, labelpad=8)
    ax.set_ylabel('Cantidad Lanzada', fontsize=10, labelpad=8)
    
    # Ubicar la leyenda de manera limpia
    ax.legend(title='Tipo de Contenido', frameon=False)
    
    sns.despine()
    plt.tight_layout()
    plt.show()