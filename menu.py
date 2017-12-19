from db_models import *


class Menu():

    def __init__(self):
        print()
        print("-" * 56)
        print("*" * 56)
        print(
            """Bienvenue ! Cette application vous propose
de remplacer un produit par un autre plus "healthy" ;) !""".upper()
        )
        print("*" * 56)
        print("-" * 56)
        self.get_categorie_or_favs()

    # def main_menu(self):
    #     print("Voulez-vous utiliser l'application ? (O/N): ")
    #     answer = input(" >> ")
    #     if answer.upper() == "O":
    #         self.get_categorie_or_favs()
    #     elif answer.upper() == "N":
    #         print("Au revoir, alors !")
    #         exit()
    #     else:
    #         print("Ce n'est pas une réponse valide, veuillez réessayer :).")
    #         self.main_menu()

    def get_categorie_or_favs(self):
        """
        Main menu of the app.
        Asks what the user wants to do.
        """
        print()
        print("=" * 50)
        print("1 - Lister les catégories d'aliments à substituer.")
        print("2 - Retrouver mes aliments substitués.")
        print("0 - Quitter l'application.")
        print()
        print("Saisissez votre choix : ")
        answer = input(" >> ")

        if answer == "1":
            self.menu_actions[answer](self)

        elif answer == "2":
            self.menu_actions[answer](self)

        elif answer == "0":
            self.menu_actions[answer](self)

        else:
            print()
            print("!" * 31)
            print("Veuillez faire un choix valide.")
            print("!" * 31)
            self.menu_actions['main_menu'](self)

    def quit(self):
        print("Bye bye !")
        exit()

    def display_categories(self):
        """
        display categories in the terminal
        """
        print()
        print("Voici toutes les catégories, veuillez en choisir une : ")
        print("-" * 54)
        select_categories = Categories.select().order_by(Categories.id)
        categories_ids = []
        for category in select_categories:
            # get all categories ids in a list to iterate over...
            categories_ids.append(category.id)
            print(category.id, "-", category.name)
        print()
        cat_choice = input(" >> ")

        try:
            cat_choice = int(cat_choice)

            if cat_choice in categories_ids:
                self.display_products(cat_choice)
            else:
                print("!" * 36)
                print("Veuillez entrer une catégorie valide.")
                print("!" * 36)
                self.display_categories()
        except ValueError as VE:
            print()
            print("!" * 26)
            print("Veuillez entrer un nombre.")
            print("!" * 26)
            self.display_categories()

        # if Categories.select().Min(Categories.id) <= cat_choice <= Categories.select().Max(Categories.id):
        #     print("Ok")

    def display_products(self, cat_choice):
        """
        display products in the terminal.
        cat_choice is the category selected by the user.
        """
        print()
        print("Voici les produits, veuillez en choisir un : ")
        print("-" * 54)
        query = Products.select().where(
            Products.cat_id == cat_choice
        ).order_by(
            Products.id
        ).paginate(1, 10)

        products_ids = []
        for product in query:
            # get all products ids in a list to iterate over...
            products_ids.append(product.id)
            print(product.id, "-", product.name)
        print()
        prod_choice = input(" >> ")

        try:
            prod_choice = int(prod_choice)
            if prod_choice in products_ids:
                self.get_better_product(prod_choice)
            else:
                print("!" * 36)
                print("Veuillez entrer un produit valide.")
                print("!" * 36)
                self.display_products(cat_choice)

        except ValueError as VE:
            print()
            print("!" * 26)
            print("Veuillez entrer un nombre.")
            print("!" * 26)
            self.display_products(cat_choice)

    def get_better_product(self, prod_choice):
        # get nutri grade of chosen product
        cur_product = Products.get(
            Products.id == prod_choice
        )

        substitute_query = Products.select().where(Products.nutri_grade <= cur_product.nutri_grade, Products.cat_id == cur_product.cat_id).order_by(fn.Rand()).paginate(1, 1)
        for product in substitute_query:
            print("Nom :", product.name, "/ Nutri grade :", product.nutri_grade)
            # print(Brands.get(Brands.id == Productsbrands.get(product.id)).id)
            brands = (Brands.select().join(Productsbrands).join(Products).where(Products.id == product.id))
            for brand in brands:
                print("Marques : ", brand.name)
            stores = (Stores.select().join(Productsstores).join(Products).where(Products.id == product.id))
            for store in stores:
                print("Magasin : ", store.name)


        # display brands and stores

    def next_page(self):
        pass

    def previous_page(self):
        pass

    def add_favs(self):
        pass

    def remove_favs(self):
        pass

    def display_favs(self):
        pass

    menu_actions = {
        'main_menu': get_categorie_or_favs,
        '1': display_categories,
        '2': display_favs,
        '9': next_page,
        '8': previous_page,
        '0': quit
    }


if __name__ == "__main__":
    menu = Menu()
