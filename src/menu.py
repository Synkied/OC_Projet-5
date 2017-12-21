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
        self.main_menu()

    def main_menu(self):
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
        print()
        print("Voici toutes les catégories, veuillez en choisir une : ")
        print("-" * 54)
        try:
            select_categories = Categories.select().order_by(Categories.id)
            categories_ids = []
            for category in select_categories:
                # put all categories ids in a list to iterate over...
                categories_ids.append(category.id)
                print(category.id, "-", category.name)
            print()
            cat_choice = input(" >> ")

            try:
                cat_choice = int(cat_choice)

                if cat_choice in categories_ids:
                    self.display_products(cat_choice, 1, 10)
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

    def display_products(self, cat_choice, page, products_per_page):
        """
        display products in the terminal.
        cat_choice is the category selected by the user.
        """
        print()
        print("Voici les produits, veuillez en choisir un : ")
        print("Page suivante (n), page précédente (p)")
        print("-" * 54)
        try:
            query = Products.select().where(
                Products.cat_id == cat_choice
            ).order_by(
                Products.id
            )

            # query pagination
            query_paginated = query.paginate(page, products_per_page)

            # an empty list to store all filtered products id
            products_ids = []
            num_products = [product.id for product in query]

            for product in query_paginated:
                # get all products ids in a list to iterate over...
                products_ids.append(product.id)
                print(product.id, "-", product.name)

            num_of_pages = len(num_products) // products_per_page

            print("*" * 25)
            print("Page", page, "/", num_of_pages)

            print()
            prod_choice = input(" >> ")

            if prod_choice.lower() == "n" or prod_choice.lower() == "p":
                # get next or previous page if asked by user
                self.menu_actions[prod_choice](
                    self,
                    cat_choice,
                    page,
                    products_per_page,
                )

            else:
                try:
                    prod_choice = int(prod_choice)
                    if prod_choice in products_ids:
                        self.display_better_product(prod_choice)
                    else:
                        print("!" * 36)
                        print("Veuillez entrer un produit valide.")
                        print("!" * 36)
                        self.display_products(
                            cat_choice,
                            page,
                            products_per_page,
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
                        products_per_page,
                    )

        except KeyboardInterrupt as keyinter:
            print("Au revoir, alors ! :)")
            exit()

        # returns query to be able to display next and previous pages
        return query, num_of_pages

    def display_better_product(self, prod_choice):
        # get nutri grade of chosen product
        cur_product = Products.get(
            Products.id == prod_choice
        )

        # if nutri_grade = a, give a similar grade product
        # else give a product with a better nutrigrade
        if cur_product.nutri_grade == "a":
            substitute_query = Products.select().where(
                Products.nutri_grade == cur_product.nutri_grade,
                Products.cat_id == cur_product.cat_id).order_by(
                fn.Rand()
            ).limit(1)

        else:
            substitute_query = Products.select().where(
                Products.nutri_grade < cur_product.nutri_grade,
                Products.cat_id == cur_product.cat_id).order_by(
                fn.Rand()
            ).limit(1)

        for product in substitute_query:
            print()
            print("Voici le substitut proposé :")
            print("-" * 28)
            print(
                "Nom :", product.name, "/ nutri grade :", product.nutri_grade
            )

            # print brands and stores if defined
            brands = (Brands.select().join(Productsbrands).join(
                Products
            ).where(Products.id == product.id))
            for brand in brands:
                print("Marques :", brand.name)
            stores = (Stores.select().join(Productsstores).join(
                Products
            ).where(Products.id == product.id))
            for store in stores:
                print("Magasin :", store.name)
            # OFF url
            print("URL OpenFoodFacts :", product.url)
            print()
            print("-" * 33)
            print("Voulez-vous l'enregistrer ? (o/n)")

            save_fav = input(" >> ")

            if save_fav.lower() == "o":
                pass

            elif save_fav.lower() == "n":
                pass

            else:
                print('Veuillez entrer "o" ou "n"')

    def next_page(self, cat_choice, page, products_per_page):
        """
        Gets the next page if it exists
        """
        page += 1
        query, num_of_pages = self.display_products(cat_choice, page, products_per_page)

        query.paginate(
            page,
            products_per_page,
        )

    def previous_page(self, cat_choice, page, products_per_page):
        """
        If the current page isn't 1, gets previous page.
        """
        if page > 1:
            page -= 1
            query, num_of_pages = self.display_products(cat_choice, page, products_per_page)

            query.paginate(
                page,
                products_per_page,
            )
        else:
            print("Vous êtes à la première page ;). ")
            query, num_of_pages = self.display_products(cat_choice, page, products_per_page)

            query.paginate(
                page,
                products_per_page,
            )

    def add_favs(self):
        pass

    def remove_favs(self):
        pass

    def display_favs(self):
        get_favs = Favorites.select()
        count_favs = Favorites.select().count()
        if count_favs == 0:
            print("Vous n'avez pas encore enregistré de favoris.")
        else:
            print(get_favs.product, get_favs.substitute)

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
