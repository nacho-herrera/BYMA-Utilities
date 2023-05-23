
from datetime import date, timedelta
from typing import List

import pandas as pd

from enums import Monedas
from slyc import SLYC

def download_estado_monedas(
    sliq: SLYC,
    fechas: List[str],
    moneda: Monedas = Monedas.PESOS,
) -> None:
    sliq._download_data(
        sliq.get_estado_moneda,
        "estado_monedas",
        "EtTotales",
        "Fecha",
        fechas,
        moneda,
    )

def download_estado_fondos(
    sliq: SLYC, fechas: List[str], moneda: Monedas = Monedas.PESOS
) -> None:
    sliq._download_data(
        sliq.get_liquidacion_fondos,
        "estado_fondos",
        "EtMovimientos",
        "Fecha",
        fechas,
        moneda,
    )

def download_estado_movimientos(
    sliq: SLYC, fechas: List[str], moneda: Monedas = Monedas.PESOS
) -> None:
    sliq._download_data(
        sliq.get_movimientos_obligaciones,
        "estado_movimientos",
        "EMovOblig",
        "Fecha",
        fechas,
        moneda,
    )

    
def _create_date_range(self, start_date: date, end_date: date) -> List[str]:
    delta = timedelta(days=1)
    dates = []
    current_date = start_date
    while current_date <= end_date:
        if (
            current_date.weekday() < 5
        ):  # Exclude weekends (Monday is 0 and Sunday is 6)
            dates.append(current_date.strftime("%Y-%m-%d"))
        current_date += delta
    return dates


def _download_data(
    self, data_func, filename_prefix, wanted_key, wanted_attr, fechas, moneda
):
    respuesta = []
    for fecha in fechas:
        print(f"Downloading {fecha}")
        resp = data_func(moneda=moneda, fecha=fecha)
        if "error" in resp.keys():
            if resp["error"] == True:
                pass
        else:
            if wanted_key in resp.keys() and resp[wanted_key] != None:
                for item in resp[wanted_key]["item"]:
                    item[wanted_attr] = fecha
                    respuesta.append(item)

    df = pd.DataFrame(respuesta)
    last_date = fechas[-1]
    csv_filename = f"{last_date} - {filename_prefix}_{moneda}.csv"
    df.to_csv(csv_filename)
    print(f"Download completed. Data saved to '{csv_filename}'")
