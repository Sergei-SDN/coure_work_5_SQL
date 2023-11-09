import json
from configparser import ConfigParser
import os

default_path = os.path.abspath("data/database.ini")


def config(filename: str = default_path, section: str = "postgresql"):
    """
    Эта функция для получения параметров базы данных
    """

    # создать парсер
    path_absolute = os.path.abspath(filename)
    parser = ConfigParser()

    # прочитать файл конфигурации
    parser.read(path_absolute)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            'Section {0} is not found in the {1} file.'.format(section, filename))
    return db


def load_companies(filename: str):
    """
    Эта функция для получения компаний из файла
    """
    result = load_jsonfile(filename)
    return result


def load_jsonfile(filename: str):
    """
    Эта функция для загрузки данных из файла JSON
    """
    with open(filename, 'r', encoding='UTF-8') as file:
        result = json.load(file)
    return result
