import pandas as pd
from lector_excel import cargar_excel, detectar_hoja_valida
from procesador_datos import limpiar_dataframe, normalizar_datos
from generador_actas import generar_acta

def main():
    ruta = input("Ingrese la ruta del archivo Excel: ")
    hojas = cargar_excel(ruta)

    if hojas:
        hoja_valida = detectar_hoja_valida(hojas)
        if hoja_valida is not None:
            print("Hoja detectada, ajustando encabezados...")
            hoja_valida.columns = hoja_valida.iloc[2]   # fila 2 como nombres de columnas

            # Rellenar nombres NaN con el colegio anterior + "_total"
            cols = []
            ultimo_nombre = None
            for col in hoja_valida.columns:
                if pd.notnull(col):
                    ultimo_nombre = str(col).strip()
                    cols.append(ultimo_nombre + "_cant")
                else:
                    if ultimo_nombre:
                        cols.append(ultimo_nombre + "_total")
                    else:
                        cols.append("DESCONOCIDO")
            hoja_valida.columns = cols

            # 🔎 Eliminar columnas duplicadas
            hoja_valida = hoja_valida.loc[:, ~hoja_valida.columns.duplicated()]

            print("Columnas ajustadas:", hoja_valida.columns)

            hoja_valida = hoja_valida.drop([0,1,2])     # eliminar filas de encabezado
            hoja_valida = hoja_valida.reset_index(drop=True)

            print("Columnas detectadas:", list(hoja_valida.columns))

            print("Hoja detectada, limpiando datos...")
            df_limpio = limpiar_dataframe(hoja_valida)
            tabla = normalizar_datos(df_limpio)

            # 🔎 Depuración: mostrar columnas y primeras filas
            print("Columnas de la tabla normalizada:", tabla.columns)
            print("Primeras filas de la tabla normalizada:")
            print(tabla.head(20))

            print("Establecimientos detectados:", tabla["establecimiento"].unique())
            print(tabla.head(10))

            if not tabla.empty:
                establecimientos = tabla["establecimiento"].unique()
                folio = 1
                for est in establecimientos:
                    est_nombre = str(est).strip()
                    datos_est = tabla[tabla["establecimiento"] == est]

                    # 🔎 Depuración: ver qué se está generando
                    print(f"Generando acta para: {est_nombre}, productos: {len(datos_est)}")

                    generar_acta(est_nombre, datos_est, folio=folio)
                    folio += 1
        else:
            print("No se pudo detectar una hoja válida.")
    else:
        print("Error al leer el archivo.")

if __name__ == "__main__":
    main()
