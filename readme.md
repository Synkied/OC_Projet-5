# OpenFoodFacts DB seeker 0.1

The aim of this project is to query the OpenFoodFacts (OFF) API in order to populate a local SQL database (MySQL in my case). A CLI interface is provided to search for products and substitutes in the created database. Substitutes can be saved by the user for later use.

This project's development has to be documentation-driven, so the different classes will be detailed in this README.

## Installation (MacOS):

### Python 3

Install from : https://www.python.org/downloads/
Preferably choose Python 3.6.3

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

```sh 
source ~/.profile
```

## Database creation:

### MySQL and install.py

1. Install MySQL for your OS : https://dev.mysql.com/downloads/mysql/#downloads
2. Set your root password or create a new MySQL user.
3. Clone this repo.
4. Do ```$ workon {your_virtual_env}``` where {your_virtual_env} is the name of your virtual environment.
5. Do ```$ cd {path/to/this_repo}``` where {this_repo} is the name of this repo, and {path/to/} is where you chose to put it on your computer.
5. Do ```$ pip install -r requirements.txt``` 
6. Use "../src/install.py" and do every step, from step 1 to step 5.
Step 1 may take some time depending on your connection. You can also direct download from OpenFoodFacts : https://world.openfoodfacts.org/data/fr.openfoodfacts.org.products.csv.
!! If you direct download the csv file, place it in the root folder of this project (OC_Projet-5) !!
To stop the download from the terminal, use <kbd>CTRL</kbd>+<kbd>C</kbd>.
7. You can now use the app.

## Using the app

### menu.py

To use the app, simply do from a terminal : ```$ python menu.py```
Then follow along the steps.
