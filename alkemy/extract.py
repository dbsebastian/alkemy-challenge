"""
@Autor = Diego Sebastian Barrios
@email = sebastiann_db@gmail.com
@linkedin = www.linkedin.com/in/dsebastianb
@github = https://dbsebastian.github.io/
"""
import requests
import datetime
import os
import shutil
import csv

from alkemy.logger import logger
from configs import ROOT_DIR


def url_additament(url):
    """
    link = desde un iterable
    toma links, quita la parte final del string, para formar un link de descarga csv soportado por google spreadsheets
    :param url: url_raw provisto por el challenge
    :return: url con formato de descarga para google sheet
    """
    add_to_url = "export?format=csv"

    try:
        url_link = url.split("/")[:-1]
        url_link.append(add_to_url)
        url = "/".join(url_link)
        logger.debug(f"{url[-33:-18]} correctamente creado")
    except Exception as error:
        logger.exception(f"|| extract.py || url_additament() || Error:{error}")

    return url


def txt_link_extraction(path_txt):
    """
    extrae links de un .txt, los separa y con ellos crea una lista de links.
    :param path_txt: path donde se encuentra el .txt que contiene los links
    :return: lista de urls
    """
    raw_url_list = []

    try:
        with open(path_txt) as file:
            for line in file:
                try:
                    if line != "\n":
                        line = line.replace("\n", "")
                        line = url_additament(line)

                        raw_url_list.append(line)
                        logger.debug(f"Link: {line[-33:-18]} agregado")
                    else:
                        pass

                except Exception as error:
                    logger.exception(f"extract.py > link_extraction(): Error:{error}")

    except Exception as error:
        logger.exception(f"|| extract.py || txt_link_extraction() || Error:{error}")

    return raw_url_list


def dic_creator(path_txt):
    """
    Crea una lista de las categorias de cada archivo obtenido
    :param path_txt: path del .txt que contiene los links a descargar
    :return:
    """
    url_list = txt_link_extraction(path_txt)

    categorias = []
    try:
        for link in url_list:
            req = requests.get(link)
            if "Museos" in req.headers["Content-Disposition"].split(";")[1]:
                categorias.append("museos")
            elif "Cine" in req.headers["Content-Disposition"].split(";")[1]:
                categorias.append("cines")
            else:
                categorias.append("bibliotecas")
        logger.info("Nombre de categorias creadas")
    except Exception as error:
        logger.exception(f"|| extract.py || captura_nombres() || Error:{error}")

    dict_final = dict(zip(categorias, url_list))
    return dict_final


def elimina_archivos_previos(cat_name):
    """
    elimina si existen archivos previos
    :param cat_name: para conformar el path, requiere el nombre de categoria
    """

    try:
        shutil.rmtree(f"{ROOT_DIR}/datos/{cat_name}", ignore_errors=True)
        logger.debug(f"elimina_archivos_previos => en: {cat_name} fueron borrados.")
    except Exception as error:
        logger.exception(f"|| extract.py || elimina_archivos_previos() || Error:{error}")



def read_csv_creator(url_csv):
    """
        crea un objeto csv_read, necesario para luego escribir el csv en el archivo final.
    :param url_csv: url a descargar el csv
    :return: objeto csv.read
    """
    # csv_obj_read = None
    try:
        req = requests.get(url_csv).content.decode("utf-8")
        csv_obj_read = csv.reader(req.splitlines())
        logger.debug(f"csv_obj_read => Creado correctamente")
    except Exception as error:
        logger.exception(f"|| extract.py || read_csv_creator() || Error:{error}")


    return csv_obj_read


def write_csv_creator(csv_reader_obj, csv_file_path):
    """
        crea un objeto read con el nombre del file final, y escribe en el el csv_read_obj
    :param csv_reader_obj: objeto del tipo csv.reader
    :param csv_file_path: path del csv file
    :return:
    """
    try:
        with open(csv_file_path, "w", newline="") as final_file:
            writer_csv = csv.writer(final_file, delimiter=",")
            for row in csv_reader_obj:
                writer_csv.writerow(row)
        logger.debug(f"write_csv_creator => {csv_file_path} creado")
    except Exception as error:
        logger.exception(f"|| extract.py || write_csv_creator() || Error:{error}")


def path_y_file_creator(categoria, url_csv):
    """
    Crea los paths para descargar los csv, crea los nombres y descarga los archivos csv.
    :param categoria: nombre de la categoria del csv
    :param url_csv: url del csv
    :return:
    """

    date = datetime.date.today()
    path = f"{ROOT_DIR}/datos/{categoria}/{date.strftime('%Y-%B')}"
    filename = f"{categoria}{date.strftime('-%d-%m-%Y')}.csv"

    try:
        # delete previous folder (the path is datos/cat
        elimina_archivos_previos(categoria)

        # creo el .csv
        os.makedirs(os.path.dirname(f"{path}/{filename}"), exist_ok=True)

        # creo read
        csv_read = read_csv_creator(url_csv)

        # creo write, y escribo el .csv
        write_csv_creator(csv_read, f"{path}/{filename}")
        logger.debug("path_y_file_creator funcionamiento correcto")
    except Exception as error:
        logger.exception(f"|| extract.py || path_y_file_creator() || Error:{error}")

    logger.info(f"Path_y_file_creator aplicado correctamente al archivo proveniente de la categoria {categoria}")
