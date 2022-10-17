"""
@Autor = Diego Sebastian Barrios
@email = sebastiann_db@gmail.com
@linkedin = www.linkedin.com/in/dsebastianb
@github = https://dbsebastian.github.io/
"""
import os
import pandas as pd

from config.configs import ROOT_DIR
from alkemy.logger import logger


def dict_path_csv(cat):
    """
    Crea una dict.
    Cada dict, contiene: Key : "nombre de categoria" y Value : "path" a un archivo .csv de dicha categoria
    :param cat: categoria del archivo .csv
    :return: dict, key=nombre categoria, value=path al .csv file
    """

    try:

        dict_cat_n_path = dict()
        subcat_name = os.listdir((os.path.join(ROOT_DIR, "datos", cat)))[0]
        files_names = os.listdir((os.path.join(ROOT_DIR, "datos", cat, subcat_name)))[0]
        path_final = os.path.join(ROOT_DIR, "datos", cat, subcat_name, files_names)

        dict_cat_n_path.update({cat: path_final})
        logger.debug(f".csv path correspondiente a la categoria {cat} obtenida correctamente")

    except Exception as error:
        logger.exception(f" || transform.py || dict_path_csv(): Error:{error}")

    # devuelve un dict de CAT:PATH
    return dict_cat_n_path


def columns_norm(df):
    """
    Normaliza el nombre de las columnas de una DataFrame
    :param df: DataFrame
    :return: DataFrame normalizado
    """

    try:
        correct_columns = {'Cod_Loc': 'cod_localidad', 'IdProvincia': 'id_provincia',
                           'IdDepartamento': 'id_departamento', 'Categoría': 'categoria', 'Provincia': 'provincia',
                           'Localidad': 'localidad','Nombre': 'nombre', 'Domicilio': 'domicilio',
                           'Dirección': 'domicilio', 'direccion':'domicilio', 'CP': 'codigo_postal',
                           'Teléfono': 'numero_telefono', 'telefono': 'numero_telefono', 'Mail': 'mail',
                           'Web': 'web', 'Observacion': 'observacion', 'Observaciones': 'observacion',
                           'Subcategoria': 'subcategoria', 'Piso': 'piso', 'Cod_tel': 'cod_area',
                           'información adicional': 'info_adicional', 'Info_adicional': 'info_adicional',
                           'Latitud': 'latitud', 'Longitud': 'longitud', 'TipoLatitudLongitud': 'tipo_lat_long',
                           'Fuente': 'fuente', 'Tipo_gestion': 'tipo_gestion', 'año_inicio': 'año_inauguracion',
                           'Año_actualizacion': 'año_actualizacion', 'actualizacion': 'año_actualizacion',
                           'Departamento': 'departamento', 'Pantallas': 'pantallas', 'Butacas': 'butacas'}

        df.rename(columns=correct_columns, inplace=True)
        logger.debug(f"DataFrame normalizada correctamente")

    except Exception as error:
        logger.exception(f" || transform.py || columns_norm(): Error:{error}")

    return df


def cat_correction_norm(value_path):
    """
    normaliza nombres de las columnas de un DataFrame,
    Además corrige inconsistencias con el nombre de algunas provincias.
    :param value_path: filepath a un .csv file
    :return: DataFrame normalizado y corregido
    """

    try:
        df = pd.read_csv(value_path, encoding="latin")

        df = columns_norm(df)

        df.loc[df.provincia == "Santa Fé", 'provincia'] = 'Santa Fe'
        df.loc[df.provincia.str.contains("Neuquén"), "provincia"] = "Neuquen"
        df.loc[df.provincia == "Tierra del Fuego", 'provincia'] = 'Tierra del Fuego, Antártida e Islas del Atlántico Sur'

        logger.debug(f"DataFrame normalizada y corregida correctamente")

    except Exception as error:
        logger.exception(f" || transform.py || cat_correction_norm(): Error:{error}")

    return df


def df_full_creator(list_of_dicts):
    """
    Concatena DataFrames para conformar una DataFrame única.
    Además selecciona y acota las columnas del DataFrame
    :param list_of_dicts: Lista de Diccionarios, formato: KEY= categoria, VALUE= .csv path
    :return: DataFrame
    """

    try:
        cols_acotadas = ["cod_localidad", "id_provincia", "id_departamento", "categoria", "provincia", "localidad",
                         "nombre",
                         "domicilio", "codigo_postal", "numero_telefono", "mail", "web"]

        df_list = list()

        for dict in list_of_dicts:
            for key_cat, value_path in dict.items():
                df_list.append(cat_correction_norm(value_path))

        df_final = pd.concat(df_list)
        df_final = df_final[cols_acotadas]

        logger.info(f"DataFrame final creada correctamente")

    except Exception as error:
        logger.exception(f" || transform.py || df_full_creator(): Error:{error}")

    return df_final


def df_cines_creator(list_of_dicts):
    """
    Confecciona la DataFrame Cines y sos respectivas columnas
    :param list_of_dicts: Lista de Diccionarios, formato: KEY= categoria, VALUE= DataFrame
    :return: DataFrame
    """
    df_cines = None

    try:
        for dict in list_of_dicts:
            for key_cat, value_path in dict.items():
                if "cines" in key_cat:
                    df_cines = cat_correction_norm(value_path)
                else:
                    pass

        df_cines = df_cines[["provincia", "pantallas", "butacas", "espacio_INCAA"]].rename(
            columns={"pantallas":"cantidad_pantallas", "butacas":"cantidad_butacas",
                     "espacio_INCAA":"cantidad_espacios_incaa"}
        )
        df_cines = df_cines[["provincia", "cantidad_pantallas", "cantidad_butacas", "cantidad_espacios_incaa"]]\
            .groupby(["provincia"], as_index=False)\
            .agg({"cantidad_pantallas":"sum", "cantidad_butacas":"sum", "cantidad_espacios_incaa":"count"})

        logger.info(f"DataFrame Cines creada correctamente")

    except Exception as error:
        logger.exception(f" || transform.py || df_cines_creator(): Error:{error}")

    return df_cines


def df_registros_por_categoria(df):
    """
    Confecciona la DataFrame "cantidad de registros por categoría"
    :param df: DataFrame completa (con columnas normalizadas) (la construida como df_full)
    :return: DataFrame
    """

    try:
        df_por_categoria = pd.DataFrame(df.groupby(["categoria"], as_index=False).size())\
            .rename(columns={"size":"registros"})

        logger.info(f"DataFrame 'Cantidad de registros por categoría' creada correctamente")

    except Exception as error:
        logger.exception(f" || transform.py || df_registros_por_categoria(): Error:{error}")

    return df_por_categoria


def df_registros_por_fuente(df):
    """
    Confecciona la DataFrame "cantidad de registros por fuente"
    :param df: DataFrame completa (con columnas normalizadas) (la construida como df_full)
    :return:  DataFrame
    """

    try:
        lista = []
        for title, df in zip(["Bibliotecas", "Espacios de Exhibición Patrimonial", "Cines"],
                             [df[df.categoria == "Bibliotecas Populares"].shape[0],
                                 df[df.categoria == "Espacios de Exhibición Patrimonial"].shape[0],
                                 df[df.categoria == "Salas de cine"].shape[0]]
                             ):
            lista.append({"fuentes_de_los_csv":title, "registros":df})
        df_fuentes = pd.DataFrame(lista).sort_values("registros", ascending=False).reset_index(drop=True)

        logger.info(f"DataFrame 'cantidad de registros por fuente' creada correctamente")

    except Exception as error:
        logger.exception(f" || transform.py || df_registros_por_fuente(): Error:{error}")

    return df_fuentes


def df_registros_provincia_categoria(df):
    """
    Confecciona la DataFrame "cantidad de registros por provincias y categorías"
    :param df: DataFrame completa (con columnas normalizadas) (la construida como df_full)
    :return: DataFrame
    """

    try:
        df_por_provincia_categ = pd.DataFrame(df.groupby(["provincia", "categoria"], as_index=False).size())\
            .rename(columns={"size":"registros_por_categoria"})

        logger.info(f"DataFrame 'cantidad de registros por provincias y categorias' creada correctamente")

    except Exception as error:
        logger.exception(f" || transform.py || df_registros_provincia_categoria(): Error:{error}")

    return df_por_provincia_categ
