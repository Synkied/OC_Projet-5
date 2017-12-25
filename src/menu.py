import math
from colorama import init
from termcolor import colored
from terminaltables import AsciiTable

from db_models import *

init()  # inits colorama


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
        self.main_menu()

    def main_menu(self):
        """
        Main menu of the app.
        Asks what the user wants to do.
        """
        print()
        print("=" * 50)
        print("Menu principal".upper().center(50))
        print("=" * 50)
        print("1 - Lister les catégories d'aliments à substituer.")
        print("2 - Retrouver mes aliments substitués.")
        print("0 - Quitter l'application.")
        print()
        print("Saisissez votre choix : ")
        try:
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

        except KeyboardInterrupt as keyinter:
            print("Au revoir, alors ! :)")
            exit()

    def quit(self):
        print("Bye bye !")
        exit()

    def display_categories(self):
        """
        Display categories in the terminal.
        if the input is not a "n" or "p" or a number,
        the user is asked to try again.
        """

        # creating the header of the categories table
        categories_data = [["id", "Catégorie"]]

        # creating an AsciiTable object from terminatables,
        # using categories_data
        categories_table = AsciiTable(categories_data)

        print()
        print("Voici toutes les catégories, veuillez en choisir une : ")
        try:
            select_categories = Categories.select().order_by(Categories.id)
            categories_ids = []
            for category in select_categories:
                # put all categories ids in a list to iterate over...
                categories_ids.append(category.id)
                categories_data.append([category.id, category.name])
            print()
            print(categories_table.table)
            cat_choice = input(" >> ")

            try:
                cat_choice = int(cat_choice)

                if cat_choice in categories_ids:
                    self.display_products(cat_choice, 1, 10, None)
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

        except KeyboardInterrupt as keyinter:
            print("Au revoir, alors ! :)")
            exit()

    def display_products(self, cat_choice, page, products_p_page, n_of_pages):
        """
        display products in the terminal.
        cat_choice is the category selected by the user.
        """
        # creating the header of the categories table
        products_data = [["id", "Produit", "Nutri grade"]]

        # creating an AsciiTable object from terminatables,
        # using products_data
        products_table = AsciiTable(products_data)

        print()
        print("Voici les produits, veuillez en choisir un : ")
        print("Page suivante (n), page précédente (p)")
        try:
            query = Products.select().where(
                Products.cat_id == cat_choice
            ).order_by(
                Products.id
            )

            # query pagination
            query_paginated = query.paginate(page, products_p_page)

            # an empty list to store all filtered products id
            cur_page_prod_ids = []
            num_products = [product.id for product in query]

            for product in query_paginated:
                # get all products ids in a list to iterate over...
                cur_page_prod_ids.append(product.id)
                products_data.append([
                    product.id,
                    product.name,
                    product.nutri_grade,
                ])

            print(products_table.table)

            n_of_pages = math.ceil(len(num_products) / products_p_page)

            print("*" * 11)
            print("Page", page, "/", n_of_pages)

            print()
            prod_choice = input(" >> ")

            if prod_choice.lower() == "n" or prod_choice.lower() == "p":
                # get next or previous page if asked by user
                self.menu_actions[prod_choice](
                    self,
                    cat_choice,
                    page,
                    products_p_page,
                    n_of_pages,
                )

            else:
                try:
                    prod_choice = int(prod_choice)
                    if prod_choice in cur_page_prod_ids:
                        self.display_better_product(prod_choice)
                    else:
                        print("!" * 36)
                        print("Veuillez entrer un produit valide.")
                        print("!" * 36)
                        self.display_products(
                            cat_choice,
                            page,
                            products_p_page,
                            n_of_pages,
                        )

                except KeyboardInterrupt as keyinter:
                    print("Au revoir, alors ! :)")
                    exit()

                except ValueError as VE:
                    print()
                    print("!" * 36)
                    print("Veuillez entrer un nombre ou (n/p).")
                    print("!" * 36)
                    self.display_products(
                        cat_choice,
                        page,
                        products_p_page,
                        n_of_pages,
                    )

        except KeyboardInterrupt as keyinter:
            print("Au revoir, alors ! :)")
            exit()

        # returns query to be able to display next and previous pages
        return query

    def display_better_product(self, prod_choice):
        """
        Displays a better product than the one chosen by the user.

        """

        # header for the substitute table
        substitute_data = [
            [
                "Nom",
                "Nutri grade",
                "Marques",
                "Magasin",
                "URL",
            ]
        ]

        # transforms the substitute_data to a table
        substitute_table = AsciiTable(substitute_data)

        cur_product = Products.get(
            Products.id == prod_choice
        )

        substitute_query = Products.select().where(
            Products.nutri_grade <= cur_product.nutri_grade,
            Products.cat_id == cur_product.cat_id).order_by(
            fn.Rand()
        ).limit(1)

        # ... else give a product with a better nutrigrade
        # else:
        #     substitute_query = Products.select().where(
        #         Products.nutri_grade < cur_product.nutri_grade,
        #         Products.cat_id == cur_product.cat_id).order_by(
        #         fn.Rand()
        #     ).limit(1)

        for substitute in substitute_query:
            sub_brands = self.select_brands(substitute, "id")
            sub_stores = self.select_stores(substitute, "id")
            print()
            print("Voici le substitut proposé :")
            print("-" * 28)
            substitute_data.append([
                substitute.name,
                substitute.nutri_grade,
                ", ".join(tuple(brand.name for brand in sub_brands)),
                ", ".join(tuple(store.name for store in sub_stores)),
                substitute.url,
            ])

            print(substitute_table.table)

            self.add_favs(cur_product, substitute)

    def add_favs(self, cur_product, substitute):
        """
        Tries to add a favorite to the Favorites table.
        The user can disagree and then it goes back to the main menu.
        """
        print("Voulez-vous l'enregistrer ? (o/n)")

        save_fav = input(" >> ")

        while save_fav not in ["o".lower(), "n".lower()]:
            print('Veuillez entrer "o" ou "n"')
            save_fav = input(" >> ")

        if save_fav.lower() == "o":
            Favorites.create(
                product_id=cur_product.id,
                substitute_id=substitute.id,
            )

            print()
            print(
                "Substitut enregistré dans vos favoris ! Retour au menu."
            )
            self.menu_actions['main_menu'](self)

        elif save_fav.lower() == "n":
            print("Substitut non enregistré, retour au menu.")
            self.menu_actions['main_menu'](self)

    def select_stores(self, product, product_id):
        """
        Query to select stores from many to many table
        """
        stores = (Stores.select().join(Productsstores).join(
            Products
        ).where(Products.id == getattr(product, product_id)))

        return stores

    def select_brands(self, product, product_id):
        """
        Query to select brands from many to many table
        """
        brands = (Brands.select().join(Productsbrands).join(
            Products
        ).where(Products.id == getattr(product, product_id)))

        return brands

    def display_favs(self):
        """
        Displays the favorites saved by user.
        This function uses colorclass to color the terminal
        It also uses terminaltables to display the data as tables.
        """
        favorites = Favorites.select()
        count_favs = Favorites.select().count()

        product_data = [
            [
                'id',
                colored('Produit substitué', 'red'),
                colored('Marque(s)', 'yellow'),
                colored('Magasin(s)', 'yellow'),
                colored('Substituant', 'green'),
                colored('Marque(s)', 'yellow'),
                colored('Magasin(s)', 'yellow'),
            ]
        ]

        product_table = AsciiTable(product_data)

        try:
            if count_favs == 0:
                print("Vous n'avez pas encore enregistré de favoris.")
            else:
                print()
                print("Vous avez", count_favs, "favoris.")
                print("Les voici :")
                print("-" * 30)

                favorites_ids = []

                for favorite in favorites:
                    favorites_ids.append(favorite.id)

                    substitutes = Products.select().where(
                        Products.id == favorite.substitute_id
                    )
                    products = Products.select().where(
                        Products.id == favorite.product_id
                    )

                    # get the brands and stores of the substitutes
                    sub_brands = self.select_brands(favorite, "substitute_id")
                    sub_stores = self.select_stores(favorite, "substitute_id")
                    # get the brands and stores of the products
                    prod_brands = self.select_brands(favorite, "product_id")
                    prod_stores = self.select_stores(favorite, "product_id")

                    # display products and substitutes
                    # Colorama is used to color some texts
                    for product in products:
                        pass

                    for sub in substitutes:
                        pass

                    # Appends data to the product_data list.
                    # These are supposed to be represented as tables.
                    # Datas are :
                    # favorite id, product name, substitute name
                    # and the brands and stores associated with each them
                    product_data.append([
                        favorite.id,
                        colored(
                            "".join(product.name for product in products),
                            "red"
                        ),
                        colored(
                            ", ".join(tuple(brand.name
                                            for brand in prod_brands)),
                            "yellow"
                        ),
                        colored(
                            ", ".join(tuple(store.name
                                            for store in prod_stores)),
                            "yellow"
                        ),
                        colored(
                            "".join(sub.name for sub in substitutes),
                            "green"
                        ),
                        colored(
                            ", ".join(tuple(brand.name
                                            for brand in sub_brands)),
                            "yellow"
                        ),
                        colored(
                            ", ".join(tuple(store.name
                                            for store in sub_stores)),
                            "yellow"
                        ),
                    ])

                print(product_table.table)

                self.edit_favs(favorites_ids)

        except KeyboardInterrupt as keyinter:
            print("Au revoir, alors ! :)")
            exit()

    def edit_favs(self, favorites_ids):
        print()
        print(
            "Choisissez un favori à supprimer ou (n) \
pour retourner au menu principal."
        )
        edit_fav_choice = input(" >> ")

        try:
            if edit_fav_choice.lower() == "n":
                print("Retour au menu principal.")
                self.menu_actions['main_menu'](self)

            else:
                try:
                    edit_fav_choice = int(edit_fav_choice)
                    if edit_fav_choice in favorites_ids:
                        self.remove_favs(edit_fav_choice, favorites_ids)
                    else:
                        print("!" * 36)
                        print("Veuillez entrer un favori valide.")
                        print("!" * 36)
                        self.edit_favs(favorites_ids)

                except KeyboardInterrupt as keyinter:
                        print("Au revoir, alors ! :)")
                        exit()

                except ValueError as VE:
                    print()
                    print("!" * 36)
                    print("Veuillez entrer un nombre ou (n).")
                    print("!" * 36)
                    self.edit_favs(favorites_ids)

        except KeyboardInterrupt as keyinter:
            print("Au revoir, alors ! :)")
            exit()

    def remove_favs(self, edit_fav_choice, favorites_ids):
        """
        Removing favorites from the Favorites table.
        """
        print("Êtes-vous sûr ? (o/n)")
        remove_fav = input(" >> ")

        while remove_fav not in ["o".lower(), "n".lower()]:
            print('Veuillez entrer "o" ou "n"')
            remove_fav = input(" >> ")
        try:
            edit_fav_choice = int(edit_fav_choice)
            if remove_fav.lower() == "o":
                favorite = Favorites.get(Favorites.id == edit_fav_choice)
                favorite.delete_instance()
                print()
                print("/" * 17)
                print("Favori supprimé !")
                print("/" * 17)
            else:
                print()
                print("!" * 18)
                print("Opération annulée.")
                print("!" * 18)
                self.display_favs()

        except KeyboardInterrupt as keyinter:
                print("Au revoir, alors ! :)")
                exit()

        except ValueError as VE:
            print()
            print("!" * 36)
            print("Veuillez entrer un nombre ou (n).")
            print("!" * 36)
            self.edit_favs(favorites_ids)

        self.display_favs()

    def ask_oui_non(self):
        pass

    def next_page(self, cat_choice, page, products_p_page, n_of_pages):
        """
        Gets the next page if it exists
        """
        if page < n_of_pages:
            page += 1
            query = self.display_products(
                cat_choice,
                page,
                products_p_page,
                n_of_pages,
            )
            query.paginate(
                page,
                products_p_page,
            )

        else:
            print()
            print("Vous êtes à la dernière page ;).")
            query = self.display_products(
                cat_choice,
                page,
                products_p_page,
                n_of_pages,
            )
            query.paginate(
                page,
                products_p_page,
            )

    def previous_page(self, cat_choice, page, products_p_page, n_of_pages):
        """
        If the current page isn't 1, gets previous page.
        """
        if page > 1:
            page -= 1
            query = self.display_products(
                cat_choice,
                page,
                products_p_page,
                n_of_pages,
            )

            query.paginate(
                page,
                products_p_page,
            )
        else:
            print()
            print("Vous êtes à la première page ;).")
            query = self.display_products(
                cat_choice,
                page,
                products_p_page,
                n_of_pages,
            )

            query.paginate(
                page,
                products_p_page,
            )

    """
    Menu actions, used to quickly access some funcs
    """
    menu_actions = {
        'main_menu': main_menu,
        '1': display_categories,
        '2': display_favs,
        'n': next_page,
        'p': previous_page,
        '0': quit
    }


if __name__ == "__main__":
    menu = Menu()
