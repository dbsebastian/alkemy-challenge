"""
@Autor = Diego Sebastian Barrios
@email = sebastiann_db@gmail.com
@linkedin = www.linkedin.com/in/dsebastianb
@github = https://dbsebastian.github.io/
"""
import os

import extract as ext
import transform as trm
import load as lod

from config.configs import ROOT_DIR
from decouple import config
from alkemy.logger import logger

# Para configurar de manera correcta los loggings del script
# "DEBUG" para ver logs detallados, diferentes etapas de las diferentes funciones.
# "INFO" para ver logs sobre la ejecución correcta de funciones nada mas.
logger.setLevel("DEBUG")


def main():
    try:

        # path del .txt que contiene los links de descarga
        path_txt = os.path.join(ROOT_DIR, "alkemy", "list of url.txt")

        # crea un dict, con
        # key= nombre CATEGORIA
        # value = LINK de descarga
        dowload_links = ext.dic_creator(path_txt)

        # itero el dicc, que contiene
        # Key = nombre de la categoria
        # Value = links de descarga
        # => uso "extr.path_y.." para descargar los .csv
        for name, link in dowload_links.items():
            ext.path_y_file_creator(name, link)

        # hasta aquí ya se descargaron los .csv, con directorio y filename propios.

        nombre_categorias = list(dowload_links.keys())

        # ---------------------------------------
        csv_paths = list()
        for categoria in nombre_categorias:
            csv_paths.append(trm.dict_path_csv(categoria))

        # a partir del diccionario que contiene dicts, con nombre de categorias y sus filepath a los .csv
        # creo los diferentes dataFrames usando las correspondientes funciones
        # creadas en "transform.py"

        df_full = trm.df_full_creator(csv_paths)
        df_cines = trm.df_cines_creator(csv_paths)
        df_reg_categorias = trm.df_registros_por_categoria(df_full)
        df_reg_fuente = trm.df_registros_por_fuente(df_full)
        df_provincias_cat = trm.df_registros_provincia_categoria(df_full)

        # ---------------------------------------

        # ya obtenidas las df, normalizadas y conformadas correctamente, queda por cargarlas (load).
        # 1ro, crear conexión con la database de postgres

        url_conexion = f"postgresql://{config('POSTGRES_USER')}:{config('PASSWORD')}" \
                       f"@{config('POSTGRES_HOST')}:{config('POSTGRES_PORT')}"

        db_conect = lod.db_engine_connect_creator(url_conexion)

        # conectado correctamente la database, queda por cargar las dataFrames a sus correspondientes
        # tablas en la database.

        lod.table_creator_n_df_loader(db_conect, "full", df_full)
        lod.table_creator_n_df_loader(db_conect, "cines", df_cines)
        lod.table_creator_n_df_loader(db_conect, "por_categorias", df_reg_categorias)
        lod.table_creator_n_df_loader(db_conect, "por_fuentes", df_reg_fuente)
        lod.table_creator_n_df_loader(db_conect, "provincias", df_provincias_cat)

        logger.info("Main() se ejecuto de manera correcta")

    except Exception as error:
        logger.exception(f" || main.py || Main(): Error:{error}")


if __name__ == '__main__':
    main()
