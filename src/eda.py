import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display
from scipy import stats
from scipy.stats import shapiro, kstest

def exploracion_basica(dataframe, secciones=None):
    """
    Realiza un análisis exploratorio básico de un DataFrame de pandas.

    Muestra (según secciones indicadas):
    - 'info': Información general del DataFrame (df.info()).
    - 'nulos': Porcentaje de valores nulos por columna.
    - 'duplicados': Número de filas duplicadas.
    - 'num_desc': Estadísticas descriptivas para variables numéricas.
    - 'cat_desc': Estadísticas descriptivas para variables categóricas (si existen).

    Parámetros:
    dataframe : pandas.DataFrame
        DataFrame a analizar.
    secciones : list de str, opcional
        Lista con apartados a mostrar. Puede contener 'info', 'nulos', 'duplicados', 'num_desc', 'cat_desc'.
        Si es None, muestra todos.

    Retorna:
    None (imprime los resultados por pantalla).
    """
    if secciones is None:
        secciones = ['info', 'nulos', 'duplicados', 'num_desc', 'cat_desc']

    if 'info' in secciones:
        print("### Información general del DataFrame ###")
        print(f"Forma (filas, columnas): {dataframe.shape}")
        print(f"Columnas: {list(dataframe.columns)}")
        print("\nResumen info():")
        dataframe.info()        # poner display
        print('--------------------------------------------------------------------------')

    if 'nulos' in secciones:
        print("\n### Porcentaje de valores nulos por columna ###")
        print(round(dataframe.isna().sum() / dataframe.shape[0] * 100, 2))
        print('--------------------------------------------------------------------------')

    if 'duplicados' in secciones:
        print("\n### Número de filas duplicadas ###")
        print(dataframe.duplicated().sum())
        print('--------------------------------------------------------------------------')

    if 'num_desc' in secciones:
        num_cols = dataframe.select_dtypes(include=['number']).columns
        if len(num_cols) > 0:
            print("\n### Estadísticas descriptivas para variables numéricas ###")
            print(dataframe[num_cols].describe().T)
        else:
            print("\n### No hay columnas numéricas para describir ###")
            print('--------------------------------------------------------------------------')

    if 'cat_desc' in secciones:
        cat_cols = dataframe.select_dtypes(include=['object', 'category']).columns
        if len(cat_cols) > 0:
            print("\n### Estadísticas descriptivas para variables categóricas ###")
            print(dataframe[cat_cols].describe().T)
        else:
            print("\n### No hay columnas categóricas para describir ###")


def exploracion_num(dataframe, col, graficos=True, mostrar_estadisticas=True, mostrar_outliers=True, figsize=(14, 8)):
    """
    Realiza un análisis exploratorio de una columna numérica.
    
    Parámetros
    ----------
    dataframe : pandas.DataFrame
        DataFrame que contiene los datos.
    col : str
        Nombre de la columna numérica a analizar.
    graficos : bool, opcional (default=True)
        Si True, muestra gráficos estadísticos.
    mostrar_estadisticas : bool, opcional (default=True)
        Si True, muestra estadísticas calculadas y tabla .describe().
    mostrar_outliers : bool, opcional (default=True)
        Si True, calcula y muestra outliers usando método IQR.
    figsize : tuple, opcional
        Tamaño base de los gráficos
    
    Retorna
    -------
    dict
        Diccionario con estadísticas descriptivas y outliers (si aplica).
    """

    # ---------------------------------------------------------
    # VALIDACIONES
    # ---------------------------------------------------------
    if col not in dataframe.columns:
        raise ValueError(f"La columna '{col}' no existe en el DataFrame.")
    
    if not pd.api.types.is_numeric_dtype(dataframe[col]):
        raise TypeError(f"La columna '{col}' no es numérica.")

    serie = dataframe[col].dropna()  # evita problemas con NaN

    print(f"La columna '{col}' es de tipo {dataframe[col].dtype}.") 
    num_unicos = dataframe[col].nunique()
    print(f"El número total de valores únicos es de {num_unicos}.")
    if num_unicos <= 20:
        print(f"Los valores únicos son: {dataframe[col].unique()}")
    else:
        print(f"Hay muchos valores únicos, aquí algunos ejemplos: {dataframe[col].unique()[:20]}")
    
    # ---------------------------------------------------------
    # ESTADÍSTICAS DESCRIPTIVAS
    # ---------------------------------------------------------
    stats_dict = {
        "min": round(serie.min(), 2),
        "max": round(serie.max(), 2),
        "mean": round(serie.mean(), 2),
        "median": round(serie.median(), 2),
        "std": round(serie.std(), 2),
        "percentil_25": round(serie.quantile(0.25), 2),
        "percentil_75": round(serie.quantile(0.75), 2)
    }

    if mostrar_estadisticas:
        print('--------------------------------------------------------------------------')
        print(f"\n📊 Exploración numérica de '{col}':")
        for k, v in stats_dict.items():
            print(f" - {k}: {v}")
        print('--------------------------------------------------------------------------')
        print("\nTabla completa describe():")
        print(serie.describe())
        print('--------------------------------------------------------------------------')

    # ---------------------------------------------------------
    # DETECCIÓN DE OUTLIERS (IQR)
    # ---------------------------------------------------------

    if mostrar_outliers:
        Q1 = serie.quantile(0.25)
        Q3 = serie.quantile(0.75)
        IQR = Q3 - Q1

        outliers = serie[(serie < Q1 - 1.5 * IQR) | (serie > Q3 + 1.5 * IQR)]
        conteo_outliers = outliers.value_counts()
        outliers_ids_por_valor = outliers.groupby(outliers).apply(lambda x: x.index.tolist()).to_dict()

        print(f"\n🔍 Número de outliers detectados: {outliers.shape[0]}")
        print("Conteo de outliers por valor único:")
        print(conteo_outliers)
        print('--------------------------------------------------------------------------')

        stats_dict["outliers_count"] = int(outliers.shape[0])
        stats_dict["outliers_unique_values"] = conteo_outliers.to_dict()        # dict con valores y su cuenta.
        #stats_dict["outliers_ids_by_value"] = outliers_ids_por_valor            # lista de IDs de los outliers.

    # ---------------------------------------------------------
    # GRÁFICOS
    # ---------------------------------------------------------

    if graficos:
        plt.figure(figsize=figsize)

        # --- Histograma + KDE ---
        plt.subplot(2, 2, 1)
        sns.histplot(serie, kde=True)
        plt.title(f"Histograma y KDE de {col}")

        # --- Boxplot ---
        plt.subplot(2, 2, 2)
        sns.boxplot(x=serie)
        plt.title(f"Boxplot de {col}")

        # --- Violin Plot ---
        plt.subplot(2, 2, 3)
        sns.violinplot(x=serie)
        plt.title(f"Violin plot de {col}")

        plt.tight_layout(pad=3.0)  # ajusta el espaciado automáticamente
        # o en vez de tight_layout: plt.subplots_adjust(hspace=0.4, wspace=0.3)

        plt.show()

    print('--------------------------------------------------------------------------')
    print('return - stats dict:')    # Siempre devuelve las estadísticas
    return stats_dict


def exploracion_cat(dataframe, col, graficos=True, mostrar_tablas=True, top=10, detectar_raras=True, umbral_raras=0.01, figsize=(14, 6)):
    """
    Realiza un análisis exploratorio detallado de una columna categórica.

    Parámetros
    ----------
    dataframe : pandas.DataFrame
        DataFrame que contiene los datos.
    col : str
        Nombre de la columna categórica a analizar.
    graficos : bool, opcional (default=True)
        Si True, muestra gráficos (countplot y barras horizontales).
    mostrar_tablas : bool, opcional (default=True)
        Si True, muestra tablas de frecuencias absolutas y relativas.
    top : int, opcional (default=10)
        Número de categorías más frecuentes a mostrar en tablas y gráficos.
    detectar_raras : bool, opcional (default=True)
        Si True, detecta categorías con muy poca frecuencia.
    umbral_raras : float, opcional (default=0.01)       # valor práctico y comúnmente usado en análisis exploratorios.
        Proporción mínima para considerar una categoría como "rara".
    figsize : tuple, opcional
        Tamaño de los gráficos.

    Retorna
    -------
    dict
        Diccionario con moda, cardinalidad, tablas de frecuencia y categorías raras.
    """

    # ---------------------------------------------------------
    # VALIDACIONES
    # ---------------------------------------------------------
    if col not in dataframe.columns:
        raise ValueError(f"La columna '{col}' no existe en el DataFrame.")

    if pd.api.types.is_numeric_dtype(dataframe[col]):
        raise TypeError(f"La columna '{col}' es numérica. Esta función es para categóricas.")

    serie = dataframe[col]

    # ---------------------------------------------------------
    # ESTADÍSTICAS BÁSICAS
    # ---------------------------------------------------------
    modo = serie.mode(dropna=False)[0]
    cardinalidad = serie.nunique(dropna=False)

    print('--------------------------------------------------------------------------')
    print(f"\n📊 Exploración categórica de '{col}':")
    print(f" - Moda: {modo}")
    print(f" - Cardinalidad (nº de categorías distintas): {cardinalidad}")

    # ---------------------------------------------------------
    # TABLAS
    # ---------------------------------------------------------
    frecuencias_abs = serie.value_counts(dropna=False)
    frecuencias_rel = serie.value_counts(normalize=True, dropna=False).round(4) * 100

    if mostrar_tablas:
        print('--------------------------------------------------------------------------')
        print("\nFrecuencias absolutas (completas):")
        display(frecuencias_abs)

        print("\nFrecuencias relativas (%):")
        display(frecuencias_rel)

        print(f"\nTop {top} categorías más frecuentes:")
        display(frecuencias_abs.head(top))

    # ---------------------------------------------------------
    # DETECCIÓN DE CATEGORÍAS RARAS
    # ---------------------------------------------------------
    categorias_raras = None
    if detectar_raras:
        categorias_raras = frecuencias_rel[frecuencias_rel < (umbral_raras * 100)]
        print('--------------------------------------------------------------------------')
        print(f"\n🔍 Categorías raras (< {umbral_raras*100}%): {len(categorias_raras)}")
        if len(categorias_raras) > 0:
            display(categorias_raras)

    # ---------------------------------------------------------
    # GRÁFICOS
    # ---------------------------------------------------------
    if graficos:
        print('--------------------------------------------------------------------------')
        plt.figure(figsize=figsize)

        # --- Countplot ---
        plt.subplot(1, 2, 1)
        sns.countplot(data=dataframe, x=col, order=frecuencias_abs.index[:top])
        plt.title(f"Top {top} categorías más frecuentes - {col}")
        plt.xticks(rotation=45)

        # --- Barras horizontales ---
        plt.subplot(1, 2, 2)
        frecuencias_abs.head(top).sort_values().plot(kind='barh')
        plt.title(f"Frecuencia (Top {top}) - {col}")

        plt.tight_layout()
        plt.show()

    # ---------------------------------------------------------
    # RETURN STRUCTURE
    # ---------------------------------------------------------
    return {
        "moda": modo,
        "cardinalidad": cardinalidad,
        "frecuencias_abs": frecuencias_abs,
        "frecuencias_rel": frecuencias_rel,
        "categorias_raras": categorias_raras
    }