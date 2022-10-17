"""
@Autor = Diego Sebastian Barrios
@email = sebastiann_db@gmail.com
@linkedin = www.linkedin.com/in/dsebastianb
@github = https://dbsebastian.github.io/
"""
import os
import logging

from config.configs import ROOT_DIR
from logging.handlers import TimedRotatingFileHandler

logger = logging.getLogger(__name__)

# creacion del handler
handler = TimedRotatingFileHandler(os.path.join(ROOT_DIR, "logs", ".log"),
                                   when="m", interval=1, backupCount=1)


# formato de los mensajes de logs creados
fmt_file = '%(levelname)s %(asctime)s %(module)s' \
           ' [%(filename)s:%(funcName)s:%(lineno)d] %(message)s'
file_formatter = logging.Formatter(fmt_file)


handler.setFormatter(file_formatter)
logger.addHandler(handler)
