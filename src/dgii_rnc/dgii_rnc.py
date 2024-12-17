"""Módulo para descargar el archivo csv de RNCs de la DGII.

Usos:
- Busqueda puntual de algún 'NOMBRE' o 'ID' (RNC)
- Cargar el dataset completo.
"""
from __future__ import annotations

import shutil
from contextlib import closing
from datetime import datetime
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile
from zoneinfo import ZoneInfo

import polars as pl
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

tz = ZoneInfo("America/Santo_Domingo")

class RNCHandler:
    """RNCHandler."""

    def __init__(self) -> None:
        """__init__."""
        self.df = pl.DataFrame()

    def download_file(self) -> None:
        """Función para descargar el archivo y extraer el csv."""
        zip_url = "https://www.dgii.gov.do/app/WebApps/Consultas/\
RNC/DGII_RNC.zip"

        with closing(requests.get(zip_url, timeout=60, stream=True)) as response:  # noqa: E501
            response.raise_for_status()
            with BytesIO() as buffer:
                for chunk in response.iter_content(chunk_size=1024 * 1024):  # 1MB chunks  # noqa: E501
                    buffer.write(chunk)
                buffer.seek(0)  # Reset buffer position

                # Process the zip file
                with ZipFile(buffer) as zfile, \
                    zfile.open("TMP/DGII_RNC.TXT") as zf, \
                    Path.open(Path.cwd() / "DGII_RNC.TXT", mode="wb") as f:
                    shutil.copyfileobj(zf, f)

    def check_file(self) -> None:
        """Función para validar si el archivo ya existe en la fecha actual.

        Si se cumple, entonces no se descarga.
        """
        file_path = "DGII_RNC.TXT"

        if Path(file_path).is_file():
            file_creation_date = datetime.fromtimestamp(
                Path(file_path).stat().st_mtime,
                tz=tz,
            ).date()
            if file_creation_date != datetime.now(tz=tz).date():
                self.download_file()
        else:
            self.download_file()

        with Path(file_path).open(encoding="Latin-1") as fh:
            self.df = (
                pl.read_csv(
                    fh.read().encode("utf-8"),
                    separator="|",
                    has_header=False,
                    encoding="utf8-lossy",
                    dtypes=[pl.Utf8],
                    quote_char=None,
                )
            )

        self.df = self.df.rename(
            {
                "column_1": "ID",
                "column_2": "NOMBRE",
                "column_3": "NOMBRE_COMERCIAL",
                "column_4": "CATEGORIA",
                "column_5": "x1",
                "column_6": "x2",
                "column_7": "x3",
                "column_8": "x4",
                "column_9": "FECHA",
                "column_10": "REGIMEN_PAGO",
                "column_11": "ESTADO",
            },
        )

        self.df = self.df.select(
            [
                "ID",
                "NOMBRE",
                "NOMBRE_COMERCIAL",
                "CATEGORIA",
                "FECHA",
                "REGIMEN_PAGO",
                "ESTADO",
            ],
        )

    def search(self, criteria: dict) -> pl.DataFrame:
        """Función para hacer una busqueda puntual con estos argumentos.

            - 'NOMBRE' -> str, nombre bajo el cual está registrado el RNC.
            - 'NOMBRE_COMERCIAL' -> str, es el nombre comercial con el cual \
está registrado el RNC.
            - 'ID' -> str, es el RNC registrado.

        Devuelve un query con la busqueda.

        Usa la descarga del archivo csv.
        """
        self.check_file()

        query = self.df

        for key, value in criteria.items():

            if key == "ID":
                query = (
                    query
                    .filter(
                        pl.col("ID") == value,
                    )
                )

            elif key == "NOMBRE":
                query = (
                    query
                    .filter(
                        pl.col("NOMBRE").str
                        .to_uppercase().str
                        .contains(value.upper()),
                    )
                )

            elif key == "NOMBRE_COMERCIAL":
                query = (
                    query
                    .filter(
                        pl.col("NOMBRE_COMERCIAL").str
                        .to_uppercase().str
                        .contains(value.upper()),
                    )
                )

        return query

    def rnc_df(self) -> pl.DataFrame:
        """Función que devuelve un dataframe con todos los RNCs."""
        self.check_file()
        return self.df

    def web_search(self, search_string: str) -> pl.DataFrame | None:
        """Busca en la web de consulta de RNCs los datos del contribuyente.

        Busca 1 Cédula/RNC a la vez.

        Args:
            search_string (str): RNC o cédula.

        Returns:
            pl.DataFrame | None: Datos del contribuyente si existen.

        """
        if not isinstance(search_string, str):
            msg = """Valor buscado no es un texto."""
            raise TypeError(
                msg,
            )

        if not search_string.isnumeric():
            msg = """Valor buscado solo debe contener texto numérico."""
            raise ValueError(
                msg,
            )

        if len(search_string) not in [9, 11]:
            msg = """La longitud del texto numérico debe ser 9 ó 11."""
            raise ValueError(
                msg,
            )

        if search_string not in self.rnc_df()["ID"]:
            msg = """Cédula/RNC No válido."""
            raise ValueError(
                msg,
            )

        options = webdriver.ChromeOptions()
        options.add_argument("headless")

        driver = webdriver.Chrome(options=options)

        wait = WebDriverWait(driver, 10)

        url = "https://www.dgii.gov.do/app/WebApps/ConsultasWeb/consultas/rnc.aspx"
        driver.get(url)

        elem_input = (
            wait
            .until(
                ec
                .element_to_be_clickable(
                    (By.ID, "ctl00_cphMain_txtRNCCedula"),
                ),
            )
        )

        elem_input.send_keys(search_string)

        elem_submit = (
            wait
            .until(
                ec
                .element_to_be_clickable(
                    (By.ID, "ctl00_cphMain_btnBuscarPorRNC"),
                ),
            )
        )

        elem_submit.click()

        if (
            wait
            .until(
                ec
                .visibility_of_element_located(
                    (By.TAG_NAME, "td"),
                ),
            )
        ):

            data = [
                i.text for i in driver.find_elements(By.TAG_NAME, "td")
            ]

        driver.close()

        cols = [value for count, value in enumerate(data) if count % 2 == 0]
        vals = [value for count, value in enumerate(data) if count % 2 != 0]

        data_dict = {}
        for key in cols:
            for value in vals:
                data_dict[key] = value
                vals.remove(value)
                break

        res_df = pl.DataFrame(
            data_dict,
        )

        if res_df.is_empty():
            print("No se encontraron datos registrados de este contribuyente.")  # noqa: T201
            return None
        return res_df


# Crear una instancia de RNCHandler
dgii_handler = RNCHandler()
