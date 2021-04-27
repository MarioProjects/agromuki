# encoding: utf-8
"""
Script que recibe como argumento el nombre de un producto y devuelve su historial de volumen
y penetración en el mercado español para los años 2017 - 2018 - 2019 - 2020

Ejemplo:
$ python3 get_volumen_penetracion.py --producto limon
"""

import argparse

import pandas as pd


def set_args():
    """
        Función para recoger los argumentos que nos pasan por la linea de comandos
        :return: (dict) Argumentos recibidos por linea de comandos
    """
    parser = argparse.ArgumentParser(description='Reto Cajamar Agro Analysis')
    parser.add_argument(
        "--producto", type=str, required=True,
        help="Nombre del producto a consultar (nombre español)"
    )

    arguments = parser.parse_args()
    return arguments


# Llamamos a la función que recoge los argumentos y nos los devuelve en un diccionario
args = set_args()  # args = {"producto": "valor"}

print("\n--- Análisis del producto Nacional --- ")

# Leemos el dataset
cajamar_folder = "datasets_cajamar"
df1 = pd.read_csv(
    f"{cajamar_folder}/Dataset1.- DatosConsumoAlimentarioMAPAporCCAA.txt",
    sep="|", encoding='utf8', decimal=","
)
# Borramos las posibles columnas que se hayan cargado mal
df1 = df1.loc[:, ~df1.columns.str.contains('^Unnamed')]

# Del dataset tomamos aquellas entradas referentes al producto obtenido por la linea de comandos
productos = df1[df1['Producto'].str.contains(pat=args.producto, case=False)]
# Obtenemos los valores totales para dicho producto (tomando los valores de todas las CCAA)
productos_nacionales = productos[productos['CCAA'].str.contains(pat=r'Total', regex=True)]

# Separamos el dataset en 3 -> Uno por cada año para realizar el análisis: 2018 - 2019- 2020
productos_nacionales_2018 = productos_nacionales[productos_nacionales['Año'] == 2018]
productos_nacionales_2019 = productos_nacionales[productos_nacionales['Año'] == 2019]
productos_nacionales_2020 = productos_nacionales[productos_nacionales['Año'] == 2020]

# Mostramos el nombre de los productos que han sido seleccionados
print(f"\nProductos seleccionados: {productos['Producto'].unique().tolist()}")

# Imprimimos el volumen por años del producto
print(f"\n\n ---- Volumen {args.producto} por años ---- ")
print(f"2018: {productos_nacionales_2018['Volumen (miles de kg)'].tolist()}")
print(f"2019: {productos_nacionales_2019['Volumen (miles de kg)'].tolist()}")
print(f"2020: {productos_nacionales_2020['Volumen (miles de kg)'].tolist()}")

# Imprimimos la penetración por años del producto
print(f"\n\n ---- Penetración {args.producto} por años ---- ")
print(f"2018: {productos_nacionales_2018['Penetración (%)'].tolist()}")
print(f"2019: {productos_nacionales_2019['Penetración (%)'].tolist()}")
print(f"2020: {productos_nacionales_2020['Penetración (%)'].tolist()}")

print("")
