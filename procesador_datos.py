import pandas as pd

def limpiar_dataframe(df):
    if "Productos solicitados" in df.columns:
        df_limpio = df[df["Productos solicitados"].notnull()]
    else:
        df_limpio = df
    return df_limpio.reset_index(drop=True)

def interpretar_celda(valor):
    if pd.isnull(valor):
        return None
    try:
        val = str(valor).replace(".", "").replace(",", "").strip()
        if val.isdigit():
            return int(val)
        return float(val)
    except:
        return None

def normalizar_datos(df):
    registros = []
    col_producto = "Productos solicitados_cant"  # ya renombrada en main

    # Detectar columnas que terminan en "_cant" pero excluir las fijas
    columnas_cant = [
        c for c in df.columns
        if c.endswith("_cant") and not c.startswith(("ITEM", "Productos solicitados", "UNIDAD", "CANTIDADES", "IMAGEN", "PRECIO", "DESCONOCIDO"))
    ]

    for col_cant in columnas_cant:
        colegio = col_cant.replace("_cant", "")
        col_total = colegio + "_total"

        for _, fila in df.iterrows():
            producto_nombre = str(fila[col_producto])
            cantidad = interpretar_celda(fila[col_cant]) if col_cant in df.columns else None
            total = interpretar_celda(fila[col_total]) if col_total in df.columns else None

            # Solo registrar si hay producto y cantidad/total
            if producto_nombre and (cantidad is not None or total is not None):
                registros.append({
                    "establecimiento": colegio,
                    "producto": producto_nombre,
                    "cantidad": cantidad if cantidad is not None else 0,
                    "total": total
                })

    return pd.DataFrame(registros, columns=["establecimiento", "producto", "cantidad", "total"])
