import configparser
import io
# import argparse

from constants import *

# def config_parse_args():

#     parser = argparse.ArgumentParser()
#     parser.add_argument("-p", "--password",
#                         """The password of your local mysql root""")


def config_write(cfg_fname):
    user, pwd = "", ""
    while user == "":
        user = input("Saisissez votre nom d'utilisateur MySQL: ")
    while pwd == "":
        pwd = input("Saisissez votre mot de passe MySQL: ")
    config = configparser.ConfigParser()
    config["MySQL"] = {
        'db': 'openfoodfacts_oc',
        # 'host': 'localhost',
        'user': user,
        'password': pwd,
    }

    with open(cfg_fname, 'w') as cfgfile:
        config.write(cfgfile)


def config_read(cfg_fname):

    try:
        # Load the configuration file
        config = configparser.ConfigParser()
        reader = config.read(cfg_fname)
        return reader

    except io.UnsupportedOperation as notreadable:
        print("Le fichier ne semble pas exister ou n'est pas lisible.")


if __name__ == "__main__":
    t = configparser.ConfigParser()
    t.read("../" + CFG_FNAME)

    for i, v in t["MySQL"].items():
        print(i, v)
