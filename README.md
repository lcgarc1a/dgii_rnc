# Dataset de los RNCs de la DGII de República Dominicana

Herramienta sencilla para carga el dataset de los RNCs de la DGII.

Puede ser útil para actualizar rápidamente la información en los flujos de trabajo.

## Dependencias

    - Polars

## Modo de Uso

### Cargar dataset de RNCs

```python
>>> from dgii_rnc.dgii_rnc import dgii_handler
>>> import polars as pl

>>> df = dgii_handler.rnc_df()

>>> df.shape
(728522, 7)

>>> df.filter(pl.col("NOMBRE").str.contains("BANCO CENTRAL"))
shape: (4, 7)
+-----------+-------------------------------------------------------------------+----------------------------------+--------------------------------+------------+--------------+--------+
| ID        | NOMBRE                                                            | NOMBRE_COMERCIAL                 | CATEGORIA                      | FECHA      | REGIMEN_PAGO | ESTADO |
| ---       | ---                                                               | ---                              | ---                            | ---        | ---          | ---    |
| str       | str                                                               | str                              | str                            | str        | str          | str    |
+========================================================================================================================================================================================+
| 401007551 | BANCO CENTRAL DE LA REPUBLICA DOMINICANA                          | null                             | SERV GRALES DE LA ADM PÚBLICA  | 23/10/1947 | ACTIVO       | NORMAL |
| 430027715 | ARS PLAN SALUD BANCO CENTRAL                                      | ARS BANCO CENTRAL                | ADMINISTRACION DE RIESGOS DE S | 23/06/2003 | ACTIVO       | NORMAL |
| 401508583 | FONDO DE JUBILACIONES Y PENSIONES DEL PERSONAL DEL BANCO CENTRAL  | null                             | ADMINISTRACIÓN DE FONDOS DE PE | 24/02/1999 | ACTIVO       | NORMAL |
| 430118591 | CLUB EMPLEADOS DEL BANCO CENTRAL                                  | CLUB EMPLEADOS DEL BANCO CENTRAL | SERV. DE ORGANIZACIÓN, DIRECCI | 08/09/2011 | ACTIVO       | NORMAL |
+-----------+-------------------------------------------------------------------+----------------------------------+--------------------------------+------------+--------------+--------+
```

### Convertir en dataframe de pandas

```python
>>> df = df.to_pandas()
```

