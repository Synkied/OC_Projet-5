import configparser
# import argparse


# def config_parse_args():

#     parser = argparse.ArgumentParser()
#     parser.add_argument("-p", "--password",
#                         """The password of your local mysql root""")


def config_write(cfg_fname):
    user = input("Saisissez votre nom d'utilisateur MySQL: ")
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
    # Load the configuration file
    config = configparser.ConfigParser()
    with open(cfg_fname, 'w') as cfgfile:
        config.read(cfgfile)
