# encoding: utf-8
"""
Script que recibe como argumento el nombre de un producto y devuelve su historial de importaciones
y exportaciones para los años 2017 - 2018 - 2019 - 2020, así como los valores máximos y mínimos
observados en dicho periodo

Ejemplo de uso:
$ python3 importaciones_exportaciones_producto.py --producto ajo
"""

import argparse
import json

import pandas as pd


def set_args():
    """
    Función para recoger los argumentos que nos pasan por la linea de comandos
    :return: (dict) Argumentos recibidos por linea de comandos
    """
    parser = argparse.ArgumentParser(description='Reto Cajamar Agro Analysis')
    # Declaramos un argumento '--producto' que nos sirve para realizar la consulta
    parser.add_argument(
        "--producto", type=str, required=True,
        help="Nombre del producto a consultar"
    )

    arguments = parser.parse_args()
    return arguments


# Llamamos a la función que recoge los argumentos y nos los devuelve en un diccionario
args = set_args()  # args = {"producto": "valor"}

# Listado de los meses que deseamos analizar
MESES = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
]

#######################################################################################
# ------------------ EXPORTACIONES E IMPORTACIONES POR PRODUCTOS ----------------------
#######################################################################################

# Importamos los datasets con la información por años de importaciones y exportaciones de producto por meses
fepex_folder = "fepex_importaciones_exportaciones"
exportaciones_meses_productos = pd.ExcelFile(f'{fepex_folder}/FH_EPRODMESEUR_processed.ods')
importaciones_meses_productos = pd.ExcelFile(f'{fepex_folder}/FH_IPRODMESEUR_processed.ods')

print("\n--- Análisis del Exportaciones --- ")

# Creamos variables (listas) para almacenar los valores de exportaciones, importaciones y en que mes suceden
marco_tiempo, exp_historial, imp_historial = [], [], []
for year in ["2017", "2018", "2019", "2020"]:  # Iteramos a través de los años 2017 - 2018 - 2019 - 2020

    # -- Caso de exportaciones
    dfem = pd.read_excel(exportaciones_meses_productos, year)  # Tomamos la hoja que hace referencia al año iterado
    # De la hoja con toda la información para ese año, solo queremos la que contenga el producto seleccionado
    # Tomando aquellos meses que hemos especificado mediante la variable 'MESES'
    exp_anuales = dfem.loc[dfem["Producto"].str.contains(pat=args.producto, case=False)][MESES].iloc[0].tolist()
    # Añadimos a nuestra variable los valores de exportación para el año iterado
    exp_historial.extend(exp_anuales)

    # -- Caso de importaciones
    dfim = pd.read_excel(importaciones_meses_productos, year)  # Tomamos la hoja que hace referencia al año iterado
    # De la hoja con toda la información para ese año, solo queremos la que contenga el producto seleccionado
    # Tomando aquellos meses que hemos especificado mediante la variable 'MESES'
    imp_anuales = dfim.loc[dfim["Producto"].str.contains(pat=args.producto, case=False)][MESES].iloc[0].tolist()
    # Añadimos a nuestra variable los valores de importación para el año iterado
    imp_historial.extend(imp_anuales)

    # Guardamos el marco de tiempo del cual hemos extraído valores de exportación e importación
    marco_tiempo.extend([f"{mes} - {year}" for mes in MESES])

# Imprimimos por pantalla los datos recogidos
print(f"\nHistorial (tiempo): {json.dumps(marco_tiempo)}")
print(f"\n\nExportaciones (valor monetario): {exp_historial}")
print(f"\n\nImportaciones (valor monetario): {imp_historial}")

print(f"\n\nMin: {min(min(exp_historial), min(imp_historial))}")
print(f"Max: {max(max(exp_historial), max(imp_historial))}")

print("")
