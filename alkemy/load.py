"""
@Autor = Diego Sebastian Barrios
@email = sebastiann_db@gmail.com
@linkedin = www.linkedin.com/in/dsebastianb
@github = https://dbsebastian.github.io/
"""
import os

from sqlalchemy import sql
from sqlalchemy import create_engine

from alkemy.logger import logger

from configs import ROOT_DIR


def buscador_sql(string_sql):
    """
    Busca entre archivos .sql, segun "string" en el filename
    :param string_sql: string que sera buscado en el filename de los .sql files
    :return: string: nombre del .sql file buscado
    """
    raw_list = os.listdir(os.path.join(ROOT_DIR, "sql_files"))

    try:
        sql_list = []
        for element in raw_list:
            if string_sql in element:
                sql_list.append(element.split(".")[0])
                logger.debug(f"El archivo {element} fue encontrado")

    except Exception as error:
        logger.exception(f" || load.py || buscador_sql(): Error:{error}")

    return sql_list[0]


def db_engine_connect_creator(url_conexion):
    """
    Conecta a la db, crea engine y .connect() para ejecutar sql. statement desde un .py
    :param url_conexion: url con los datos para conectar a la db de postgresql
    :return: objeto "sqlalchemy.engine.base.Connection"
    """

    try:
        engine = create_engine(url_conexion)
        logger.info("create_engine() creado correctamente")
    except Exception as error:
        logger.exception(f" || load.py || db_engine_connect_creator(): Error:{error}")

    try:
        connect = engine.connect()
        logger.debug("Engine.connect() creado correctamente")
    except Exception as error:
        logger.exception(f" || load.py || db_engine_connect_creator(): Error:{error}")

    logger.info(f"db_engine_connect_creator() funcionamiento correcto")

    return connect


def elimina_tabla_previa(conect_ob, sql_table_name):
    """
    Elimina sql existente que comparta el nombre a la .sql filename indicada
    :param conect_ob: objeto "sqlalchemy.engine.base.Connection"
    :param sql_table_name: filename del .sql a ser eliminado si existiera
    :return:
    """

    try:
        clean = sql.text(f"DROP TABLE IF EXISTS {sql_table_name.split('.')[0]}")
        conect_ob.execute(clean)
        logger.debug(f"tabla {sql_table_name.split('.')[0]} eliminada correctamente")

    except Exception as error:
        logger.exception(f" || load.py || elimina_tabla_previa(): Error:{error}")


def crea_tabla_sql(conect_ob, file_from_open):
    """
    crea una nueva tabla en la base de datos
    :param conect_ob: objeto "sqlalchemy.engine.base.Connection"
    :param file_from_open: archivo .sql abierto con Open()
    :return:
    """

    try:
        to_execute = sql.text(file_from_open.read())
        conect_ob.execute(to_execute)
        logger.debug(f"tabla creada correctamente")

    except Exception as error:
        logger.exception(f" || load.py || crea_tabla_sql(): Error:{error}")


def fecha_carga_creator(conect_ob, sql_name):
    """
    Crea y adiciona a la tabla indicada la columna "fecha_de_carga" con la fecha actual.
    :param conect_ob: objeto "sqlalchemy.engine.base.Connection"
    :param sql_name: nombre del archivo .sql en el que se adicionará la columna
    :return:
    """

    try:
        to_execute = sql.text(f"ALTER TABLE {sql_name} "
                              f"ADD fecha_de_carga date not null default CURRENT_DATE")
        conect_ob.execute(to_execute)
        logger.debug(f" 'fecha_de_carga' correctamente agregada a la tabla {sql_name}")

    except Exception as error:
        logger.exception(f" || load.py || fecha_carga_creator(): Error:{error}")


def table_creator_n_df_loader(conexion, sql_name, dataframe):
    """
    crea una tabla en la database
    :param conexion: objeto "sqlalchemy.engine.base.Connection"
    :param sql_name: string, parte del filename que tiene el .sql en el directorio "sql_files"
    :return:
    """

    try:
        sql_name = buscador_sql(sql_name)

        with open(f"{os.path.join(ROOT_DIR, 'sql_files', f'{sql_name}.sql')}", encoding="utf8") as file:
            elimina_tabla_previa(conexion, sql_name)

            crea_tabla_sql(conexion, file)

        dataframe.to_sql(sql_name, conexion, if_exists='replace', index=False)

        fecha_carga_creator(conexion, sql_name)

    except Exception as error:
        logger.exception(f" || load.py || table_creator_n_df_loader(): Error:{error}")

    logger.info(f"tabla correspondiente a {sql_name} creada y cargada correctamente")
