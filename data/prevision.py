#!/usr/bin/env python
# coding: utf-8
"""
Script que recibe como argumento el nombre de un producto y devuelve su historial de importaciones
y exportaciones para los años 2017 - 2018 - 2019 - 2020, así como los valores máximos y mínimos
observados en dicho periodo

Ejemplo de uso:
$ python3 prevision.py --tipo Importación
"""

import argparse

import torch
import torch.nn as nn

import numpy as np
import pandas as pd
import torch.nn.functional as F


def split_data(data, inw, outw):
    """
    Dado un conjunto de datos 'data', se generan dos salidas con todas las posibles combinaciones
    de 'data' correlativo con tamaño 'inw' y sus consiguientes 'data' de tamaño 'outw'
    """
    x, y = [], []
    for i in range(len(data)):
        if len(data[i:]) >= (inw + outw):
            x.append(data[i:(i + inw)])
            y.append(data[(i + inw):(i + inw + outw)])
        else:
            break
    return np.stack(x), np.stack(y)


def set_args():
    """
    Función para recoger los argumentos que nos pasan por la linea de comandos
    :return: (dict) Argumentos recibidos por linea de comandos
    """
    parser = argparse.ArgumentParser(description='Reto Cajamar Agro Analysis')
    # Declaramos un argumento '--producto' que nos sirve para realizar la consulta
    parser.add_argument(
        "--tipo", type=str, required=True, choices=["Exportación", "Importación"],
        help="Tipo de movimiento a predecir. Ejemplo: Exportación."
    )

    parser.add_argument('--progreso', action='store_true', help='Muestr el progreso de la red neuronal')

    arguments = parser.parse_args()
    return arguments


# Llamamos a la función que recoge los argumentos y nos los devuelve en un diccionario
args = set_args()  # args = {"tipo": "valor"}

# Listado de los meses que deseamos analizar
MESES = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
]

# Importamos los datasets con la información por años de importaciones y exportaciones de producto por meses
fepex_folder = "fepex_importaciones_exportaciones"
exportaciones_meses_productos = pd.ExcelFile(f'{fepex_folder}/FH_EPRODMESEUR_processed.ods')
importaciones_meses_productos = pd.ExcelFile(f'{fepex_folder}/FH_IPRODMESEUR_processed.ods')

if args.tipo == "Exportación":
    dfem_2016 = pd.read_excel(exportaciones_meses_productos, '2016')
    dfem_2017 = pd.read_excel(exportaciones_meses_productos, '2017')
    dfem_2018 = pd.read_excel(exportaciones_meses_productos, '2018')
    dfem_2019 = pd.read_excel(exportaciones_meses_productos, '2019')
    dfem_2020 = pd.read_excel(exportaciones_meses_productos, '2020')

    all_data = pd.concat([
        dfem_2016.drop(["Producto", "Total", "TIPO"], axis=1).sum(),
        dfem_2017.drop(["Producto", "Total", "TIPO"], axis=1).sum(),
        dfem_2018.drop(["Producto", "Total", "TIPO"], axis=1).sum(),
        dfem_2019.drop(["Producto", "Total", "TIPO"], axis=1).sum(),
        dfem_2020.drop(["Producto", "Total", "TIPO"], axis=1).sum(),
    ])

    all_data = all_data.values.astype(float).reshape(-1)

elif args.tipo == "Importación":
    dfim_2016 = pd.read_excel(importaciones_meses_productos, '2016')
    dfim_2017 = pd.read_excel(importaciones_meses_productos, '2017')
    dfim_2018 = pd.read_excel(importaciones_meses_productos, '2018')
    dfim_2019 = pd.read_excel(importaciones_meses_productos, '2019')
    dfim_2020 = pd.read_excel(importaciones_meses_productos, '2020')

    all_data = pd.concat([
        dfim_2016.drop(["Producto", "Total", "TIPO"], axis=1).sum(),
        dfim_2017.drop(["Producto", "Total", "TIPO"], axis=1).sum(),
        dfim_2018.drop(["Producto", "Total", "TIPO"], axis=1).sum(),
        dfim_2019.drop(["Producto", "Total", "TIPO"], axis=1).sum(),
        dfim_2020.drop(["Producto", "Total", "TIPO"], axis=1).sum(),
    ])

    all_data = all_data.values.astype(float).reshape(-1)

else:
    assert False, f"Tipo '{args.tipo}' desconocido."

test_data_size = 10  # meses
train_data = all_data[:-test_data_size]
test_data = all_data[-test_data_size:]

in_data_window = 5
out_pred_window = 3

x, y = split_data(train_data, in_data_window, out_pred_window)
x, y = torch.tensor(x, dtype=torch.float), torch.tensor(y, dtype=torch.float)


class NeuralNet(nn.Module):

    def __init__(self, in_window, out_window):
        super(NeuralNet, self).__init__()

        self.fc1 = nn.Linear(in_window, 128)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, out_window)

    def forward(self, entrada):
        out = self.fc1(entrada)
        out = F.relu(out)
        out = self.fc2(out)
        out = F.relu(out)
        out = self.fc3(out)
        return out


model = NeuralNet(in_window=in_data_window, out_window=out_pred_window)

num_epochs = 100000
learning_rate = 0.01

criterion = torch.nn.MSELoss()  # Error cuadrático medio para regresión
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

# Train the model
model.train()
for epoch in range(num_epochs):
    optimizer.zero_grad()
    outputs = model(x)

    # obtain the loss function
    loss = criterion(outputs, y)
    loss.backward()

    optimizer.step()

    if epoch % 100 == 0 and args.progreso:
        print("Epoch: %d, loss: %1.5f" % (epoch, loss.item()))


# ---- Predicción COVID-19
model.eval()

# pre-covid
train_preds = []
for i in range(0, len(train_data), out_pred_window):
    if len(train_data[i:]) >= (in_data_window + out_pred_window):
        pred = model(torch.tensor(train_data[i:(i + in_data_window)], dtype=torch.float)).data.numpy().tolist()
        train_preds.extend(pred)
    else:
        break

months_to_predict = 10 + in_data_window
predicted_months = []
pred_historial = train_preds[-in_data_window:]

while len(pred_historial) < months_to_predict:
    pred_historial.extend(model(torch.tensor(pred_historial[-in_data_window:], dtype=torch.float)).data.numpy().tolist())

meses_prevision = 8
covid_pred = pred_historial[in_data_window:(meses_prevision + in_data_window)]

print("\n --- Predicción Enero 2019 a Octubre 2020 ---\n")

print(f"Real: {np.concatenate((train_data, test_data))[:-2][-22:].tolist()}")
print(f"\nPrevisto: {np.concatenate((train_preds, covid_pred))[-22:].tolist()}")

print(f"\nMin: {np.concatenate((np.concatenate((train_data, test_data)), np.concatenate((train_preds, covid_pred)))).min()}")
print(f"Max: {np.concatenate((np.concatenate((train_data, test_data)), np.concatenate((train_preds, covid_pred)))).max()}")
