# coding: utf8

"""
Execute this file from a terminal if mysql_config.ini is missing.
"""

import configparser
# import argparse

from constants import *

# def config_parse_args():

#     parser = argparse.ArgumentParser()
#     parser.add_argument("-p", "--password",
#                         """The password of your local mysql root""")


def config_write(cfg_fname, user="root", pwd="root"):

    config = configparser.ConfigParser()

    config["MySQL"] = {
        'db': 'openfoodfacts_oc',
        'host': 'localhost',
        'user': user,
        'password': pwd,
    }

    with open(cfg_fname, 'w') as cfgfile:
        config.write(cfgfile)

    print()
    print("Informations enregistrées !")


if __name__ == "__main__":
    # t = configparser.ConfigParser()
    # t.read("../" + CFG_FNAME)

    # for i, v in t["MySQL"].items():
    #     print(t["MySQL"]["user"])

    config_write("../" + CFG_FNAME)
