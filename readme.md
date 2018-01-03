# OpenFoodFacts DB seeker 0.1

The aim of this project is to query the OpenFoodFacts (OFF) API in order to populate a local SQL database (MySQL in my case). A CLI interface is provided to search for products and substitutes in the created database. Substitutes can be saved by the user for later use.

This project's development has to be documentation-driven, so the different classes will be detailed in this README.

## Installation (MacOS):

### Virtualenv and VirtualenvWrapper

```sh
pip install --user virtualenv
pip install --user virtualenvwrapper
```

After the installation it's time to add theses lines in ```~/.profile``` (maybe ```~/.bashrc``` or ```~/.bash_profile```)

```sh
export WORKON_HOME=~/.virtualenvs
mkdir -p $WORKON_HOME
export PROJECT_HOME=~/pyprojects
mkdir -p $PROJECT_HOME
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3.x
export VIRTUALENVWRAPPER_VIRTUALENV=~/.local/bin/virtualenv
source .local/bin/virtualenvwrapper.sh
```

And finally reload this file :

```source ~/.profile```

### Install Python 3.6.0

```sh
wget https://www.python.org/ftp/python/3.6.0/Python-3.6.0.tgz
tar -xvzf Python-3.6.0
cd Python-3.6.0
sudo ./configure
sudo make install
cd ..
rm Python-3.6.0.tgz
rm -rf Python-3.6.0
```

## Initialize the database:

1. Install MySQL for your OS : https://dev.mysql.com/downloads/mysql/#downloads
2. Set your root password or create a new MySQL user.
3. Clone this repo.
4. Do ```sh $ pip install -r requirements.txt``` 
5. Use "Install.py" and do every step, from step 1 to step 5.
Step 1 may take some time depending on your connection. You can also direct download from OpenFoodFacts : https://world.openfoodfacts.org/data/fr.openfoodfacts.org.products.csv.
!! If you direct download the csv file, place it in the root folder of this project (OC_Projet-5) !!
6. You can now use "menu.py" and search for products. Substitutes will be displayed to you, you can save them.

## 

