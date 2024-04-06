# Dominican Republic Taxpayer Dataset and Search Tool

[![PyPI - Version](https://img.shields.io/pypi/v/dgii-rnc)](https://pypi.org/project/dgii-rnc/) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dgii-rnc)](https://www.python.org/downloads/)
 ![PyPI - Status](https://img.shields.io/pypi/status/dgii-rnc) [![changelog](https://img.shields.io/badge/changelog-5A5A5A)](./CHANGELOG.md)

Simple tool to load the dataset of taxpayers of the Dominican Republic. It can be used to correct data on names or IDs registered in some data source, as well as being integrated into a much larger application.

Source: [https://www.dgii.gov.do/app/WebApps/Consultas/RNC/DGII_RNC.zip]

## Installation

```python
>>> pip install dgii-rnc
```

## Dependencies

- Polars
- Selenium

## How to use

### Getting the dataset

```python
>>> from dgii_rnc.dgii_rnc import dgii_handler
>>> import polars as pl

>>> df = dgii_handler.rnc_df()

>>> df.shape
(735018, 7)

>>> df.filter(pl.col("NOMBRE").str.contains("BANCO CENTRAL"))
shape: (4, 7)
+-----------+----------------+----------------+---------------+------------+--------------+--------+
| ID        | NOMBRE         | NOMBRE_COMERCI | CATEGORIA     | FECHA      | REGIMEN_PAGO | ESTADO |
| ---       | ---            | AL             | ---           | ---        | ---          | ---    |
| str       | str            | ---            | str           | str        | str          | str    |
|           |                | str            |               |            |              |        |
+==================================================================================================+
| 401007551 | BANCO CENTRAL  | null           | SERV GRALES   | 23/10/1947 | ACTIVO       | NORMAL |
|           | DE LA          |                | DE LA ADM     |            |              |        |
|           | REPUBLICA      |                | PÚBLICA       |            |              |        |
|           | DOMINICANA     |                |               |            |              |        |
| 430027715 | ARS PLAN SALUD | ARS BANCO      | ADMINISTRACIO | 23/06/2003 | ACTIVO       | NORMAL |
|           | BANCO CENTRAL  | CENTRAL        | N DE RIESGOS  |            |              |        |
|           |                |                | DE S          |            |              |        |
| 401508583 | FONDO DE       | null           | ADMINISTRACIÓ | 24/02/1999 | ACTIVO       | NORMAL |
|           | JUBILACIONES Y |                | N DE FONDOS   |            |              |        |
|           | PENSIONES DEL  |                | DE PE         |            |              |        |
|           | PERSONAL DEL   |                |               |            |              |        |
|           | BANCO CENTRAL  |                |               |            |              |        |
| 430118591 | CLUB EMPLEADOS | CLUB EMPLEADOS | SERV. DE      | 08/09/2011 | ACTIVO       | NORMAL |
|           | DEL BANCO      | DEL BANCO      | ORGANIZACIÓN, |            |              |        |
|           | CENTRAL        | CENTRAL        | DIRECCI       |            |              |        |
+-----------+----------------+----------------+---------------+------------+--------------+--------+
```

### Searches

#### Local

```python
>>> # 'Csv' search
>>> search_query = dgii_handler.search({'NOMBRE':'BANCO CENTRAL DE LA REPUBLICA'})
>>> print(search_query)
shape: (1, 7)
+-----------+----------------+----------------+---------------+------------+--------------+--------+
| ID        | NOMBRE         | NOMBRE_COMERCI | CATEGORIA     | FECHA      | REGIMEN_PAGO | ESTADO |
| ---       | ---            | AL             | ---           | ---        | ---          | ---    |
| str       | str            | ---            | str           | str        | str          | str    |
|           |                | str            |               |            |              |        |
+==================================================================================================+
| 401007551 | BANCO CENTRAL  | null           | SERV GRALES   | 23/10/1947 | ACTIVO       | NORMAL |
|           | DE LA          |                | DE LA ADM     |            |              |        |
|           | REPUBLICA      |                | PÚBLICA       |            |              |        |
|           | DOMINICANA     |                |               |            |              |        |
+-----------+----------------+----------------+---------------+------------+--------------+--------+
```

#### Web

```python
>>> # 'Web' search
>>> web_search_query = dgii_handler.web_search('401007551')
>>> web_search_query.to_dicts()
>>> [{'Cédula/RNC': '401-00755-1',
...  'Nombre/Razón Social': 'BANCO CENTRAL DE LA REPUBLICA DOMINICANA',
...  'Nombre Comercial': ' ',
...  'Categoría': '',
...  'Régimen de pagos': 'NORMAL',
...  'Estado': 'ACTIVO',
...  'Actividad Economica': 'SERV GRALES DE LA ADM PÚBLICA (INCL. EL DESEMPEÑO DE FUNCIONES EJECUTIVAS Y LEGISLATIVAS DE ADM POR PARTE DE LAS ENTIDADES DE LA A',
...  'Administracion Local': 'ADM LOCAL GGC'}]
```

### Convert to pandas dataframe

```python
>>> df = df.to_pandas()
```
