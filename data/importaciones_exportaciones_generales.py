# coding: utf-8
"""
Script para analizar el volumen de importaciones y exportaciones de frutas y verduras españolas a lo largo
de los años (2017 - 2018 - 2019 - 2020)

Ejemplo:
$ python3 importaciones_exportaciones_generales.py
"""

import json

import numpy as np
import pandas as pd

# Listado de los meses que deseamos analizar
MESES = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
]

# Carga de los datasets que vamos a utilizar
fepex_folder = "fepex_importaciones_exportaciones"
exportaciones_meses_productos = pd.ExcelFile(f'{fepex_folder}/FH_EPRODMESEUR_processed.ods')
importaciones_meses_productos = pd.ExcelFile(f'{fepex_folder}/FH_IPRODMESEUR_processed.ods')

# Creamos variables (listas) para almacenar los valores de exportaciones y en que mes suceden
exp_tiempo, exp_historial_hortalizas, exp_historial_frutas = [], [], []
# ["2016", "2017", "2018", "2019", "2020"]
for year in ["2017", "2018", "2019", "2020"]:  # Iteramos a través de los años 2017 - 2018 - 2019 - 2020
    # Tomamos el dataset de exportaciones, seleccionando aquella hoja referente al año de la iteración actual
    dfem = pd.read_excel(exportaciones_meses_productos, year)
    # Dividimos los datos por tipo -> Hortalizas y Frutas
    exp_meses_hortalizas = dfem.loc[dfem["TIPO"] == "Hortaliza"][MESES].sum().tolist()
    exp_meses_frutas = dfem.loc[dfem["TIPO"] == "Fruta"][MESES].sum().tolist()

    # Añadimos a la lista con el historial, los datos de la iteración actual
    exp_historial_hortalizas.extend(exp_meses_hortalizas)
    exp_historial_frutas.extend(exp_meses_frutas)
    exp_tiempo.extend([f"{mes} - {year}" for mes in MESES])

print(f"\nHistorial (tiempo): {json.dumps(exp_tiempo)}")
print(f"\n\nHistorial Exportaciones Hortalizas: {exp_historial_hortalizas}")
print(f"\n\nHistorial Exportaciones Frutas: {exp_historial_frutas}")

# Creamos variables (listas) para almacenar los valores de importaciones y en que mes suceden
imp_tiempo, imp_historial_hortalizas, imp_historial_frutas = [], [], []
# ["2016", "2017", "2018", "2019", "2020"]
for year in ["2017", "2018", "2019", "2020"]:  # Iteramos a través de los años 2017 - 2018 - 2019 - 2020
    # Tomamos el dataset de importaciones, seleccionando aquella hoja referente al año de la iteración actual
    dfim = pd.read_excel(importaciones_meses_productos, year)
    # Dividimos los datos por tipo -> Hortalizas y Frutas
    imp_meses_hortalizas = dfim.loc[dfim["TIPO"] == "Hortaliza"][MESES].sum().tolist()
    imp_meses_frutas = dfim.loc[dfim["TIPO"] == "Fruta"][MESES].sum().tolist()

    # Añadimos a la lista con el historial, los datos de la iteración actual
    imp_historial_hortalizas.extend(imp_meses_hortalizas)
    imp_historial_frutas.extend(imp_meses_frutas)
    imp_tiempo.extend([f"{mes} - {year}" for mes in MESES])


# Imprimimos datos interesantes recogidos
print(f"\nHistorial (tiempo): {json.dumps(imp_tiempo)}")
print(f"\n\nHistorial Importaciones Hortalizas: {imp_historial_hortalizas}")
print(f"\n\nHistorial Importaciones Frutas: {imp_historial_frutas}")

max_val = max(*exp_historial_hortalizas, *imp_historial_hortalizas, *exp_historial_frutas, *imp_historial_frutas)
min_val = min(*exp_historial_hortalizas, *imp_historial_hortalizas, *exp_historial_frutas, *imp_historial_frutas)
print(f"Valor maximo (entre todas importaciones y exportaciones): {max_val}")
print(f"Valor mínimo (entre todas importaciones y exportaciones): {min_val}")
print("")

exp_frutas_sobre_hortalizas = np.array(exp_historial_frutas).sum() / np.array(exp_historial_hortalizas).sum()
imp_frutas_sobre_hortalizas = np.array(imp_historial_frutas).sum() / np.array(imp_historial_hortalizas).sum()
print(f"La exportación de frutas es {exp_frutas_sobre_hortalizas} mayor a la de hortalizas")
print(f"La importación de frutas es {imp_frutas_sobre_hortalizas} mayor a la de hortalizas")
print("")

exp_hortalizas_sobre_imp = np.array(exp_historial_hortalizas).sum() / np.array(imp_historial_hortalizas).sum()
print(f"La exportación de hortalizas es {exp_hortalizas_sobre_imp} mayor a la importación de las mismas")
exp_frutas_sobre_imp = np.array(exp_historial_frutas).sum() / np.array(imp_historial_frutas).sum()
print(f"La exportación de frutas es {exp_frutas_sobre_imp} mayor a la importación de las mismas")
print("")

exp_horto_sobre_imp = (np.array(exp_historial_hortalizas).sum() + np.array(exp_historial_frutas).sum()) / \
                      (np.array(imp_historial_hortalizas).sum() + np.array(imp_historial_frutas).sum())
print(f"La exportación de productos hortofrutícolas es {exp_horto_sobre_imp} mayor a la importación de los mismas")
print("")
