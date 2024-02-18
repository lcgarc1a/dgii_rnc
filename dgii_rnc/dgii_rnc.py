"""Módulo para descargar el archivo csv de RNCs de la DGII.

Usos:
- Busqueda puntual de algún 'NOMBRE' o 'ID' (RNC)
- Cargar el dataset completo.
"""

import os
from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile
import shutil
from datetime import datetime, date
import polars as pl

class RNCHandler:
    """RNCHandler.
    """

    def __init__(self):
        self.df = None

    def download_file(self):
        """
        Función para descargar el archivo y extraer el csv.
        """

        zip_url = "https://www.dgii.gov.do/app/WebApps/Consultas/RNC/DGII_RNC.zip"

        with urlopen(zip_url) as zip_resp:
            with ZipFile(BytesIO(zip_resp.read())) as zfile:
                with zfile.open("TMP/DGII_RNC.TXT") as zf, open(os.path.join(os.getcwd(), 'DGII_RNC.TXT'), 'wb') as f:
                    shutil.copyfileobj(zf, f)

    def check_file(self):
        """Función para validar si el archivo ya existe en la fecha actual. 
        Si se cumple, entonces no se descarga.
        """

        file_path = 'DGII_RNC.TXT'
        if os.path.isfile(file_path):
            file_creation_date = datetime.fromtimestamp(os.path.getctime(file_path)).date()
            if file_creation_date != date.today():
                self.download_file()
        else:
            self.download_file()

        with open('DGII_RNC.TXT', 'r', encoding='Latin-1') as fh:
            self.df = (
                pl.read_csv(
                    fh.read().encode('utf-8'),
                    separator='|',
                    has_header=False,
                    encoding='utf8-lossy',
                    dtypes={
                        'column_1': str,
                        'column_2': str,
                        'column_3': str,
                        'column_4': str,
                        'column_5': str,
                        'column_6': str,
                        'column_7': str,
                        'column_8': str, 
                        'column_9': str,
                        'column_10': str,
                        'column_11': str
                    }
                )
            )

        self.df = (
            self.df.rename(
                {
                    'column_1': 'ID',
                    'column_2': 'NOMBRE',
                    'column_3': 'NOMBRE_COMERCIAL',
                    'column_4': 'CATEGORIA',
                    'column_5': 'x1',
                    'column_6': 'x2',
                    'column_7': 'x3',
                    'column_8': 'x4', 
                    'column_9': 'FECHA',
                    'column_10': 'REGIMEN_PAGO',
                    'column_11': 'ESTADO'
                }
            )
        )

        self.df = (
            self.df.filter(pl.col('x1').is_not_null())
            .select(
                [
                    'ID',
                    'NOMBRE',
                    'NOMBRE_COMERCIAL',
                    'CATEGORIA',
                    'FECHA',
                    'REGIMEN_PAGO',
                    'ESTADO'
                ]
            )
        )

    def dgii_search(self, criteria):
        """Función para hacer una busqueda puntual con estos argumentos:

            - 'NOMBRE' --> str, nombre bajo el cual está registrado el RNC.
            - 'NOMBRE_COMERCIAL' --> str, es el nombre comercial con el cual está registrado el RNC.
            - 'ID' --> str, es el RNC registrado.
        
        Devuelve un query con la busqueda.
        """

        self.check_file()

        query = self.df

        for key, value in criteria.items():

            if key == 'ID':
                query = (
                    query
                    .filter(
                        pl.col('ID') == value
                    )
                )

            elif key == 'NOMBRE':
                query = (
                    query
                    .filter(
                        pl.col('NOMBRE').str.to_uppercase().str.contains(value.upper())
                    )
                )

            elif key == 'NOMBRE_COMERCIAL':
                query = (
                    query
                    .filter(
                        pl.col('NOMBRE_COMERCIAL').str.to_uppercase().str.contains(value.upper())
                    )
                )

        return query

    def rnc_df(self):
        """Función que devuelve un dataframe.

        En su momento se hizo con la función `read_csv` de polars por su rapidez.

        Se puede agregar `.to_pandas()` luego de llamar la función para usar el df en pandas.
        """

        self.check_file()
        return self.df

# Crear una instancia de RNCHandler
dgii_handler = RNCHandler()
