from typing import Callable
import os
import configparser

user_home = os.path.expanduser('~')
init_file = os.path.join(user_home, 'wedata.ini')


def save_env(section: str, option: str, value: str):
    conf = configparser.ConfigParser()
    conf.read(init_file, encoding="utf-8")
    if section not in conf.sections():
        conf.add_section(section)
    conf.set(section, option, value)
    conf.write(open(init_file, 'w'))


def get_env(section: str, option: str) -> str:
    conf = configparser.ConfigParser()
    conf.read(init_file, encoding="utf-8")
    return conf.get(section, option)


