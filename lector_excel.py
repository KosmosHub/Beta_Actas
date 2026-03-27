import pandas as pd

def cargar_excel(ruta_archivo):
    """
    Carga un archivo Excel y devuelve un diccionario con todas las hojas.
    """
    try:
        hojas = pd.read_excel(ruta_archivo, sheet_name=None)
        return hojas
    except Exception as e:
        print(f"Error al cargar el Excel: {e}")
        return None

def detectar_hoja_valida(hojas):
    """
    Detecta la hoja válida. Por ahora, toma la primera hoja con más de 5 filas y columnas.
    """
    for nombre, df in hojas.items():
        if df.shape[0] > 5 and df.shape[1] > 5:
            print(f"Hoja detectada: {nombre}")
            return df
    print("No se encontró una hoja válida.")
    return None
