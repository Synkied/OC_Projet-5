from csv_downloader import TqdmDL


url = "https://world.openfoodfacts.org/data/en.openfoodfacts.org.products.csv"
directory = "../"
fname = 'en.openfoodfacts.org.products.csv'


dl_file = TqdmDL()

dl_file.download(url, directory, fname)
