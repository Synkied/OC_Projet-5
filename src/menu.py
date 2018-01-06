# coding: utf8
import math

from colorama import init
from termcolor import colored
from terminaltables import AsciiTable
from peewee import *
import pymysql

from db_models import *

init()  # inits colorama


class Menu():

    def __init__(self):
        print()
        print("-" * 56)
        print("*" * 56)
        print(
            """Welcome ! This app was tailored to search through the
OpenFoodFacts website and suggest you healthier products ;) !""".upper()
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
        print("Main menu".upper().center(50))
        print("=" * 50)
        print("1 - List available categories.")
        print("2 - See my favorites substitutes.")
        print("0 - Quit.")
        print()
        print("Input your choice: ")
        try:
            answer = input(" >> ")

            if answer in self.menu_actions.keys():
                self.menu_actions[answer](self)

            else:
                print()
                print("!" * 31)
                print("Please, make a valid choice.")
                print("!" * 31)
                self.menu_actions['main_menu'](self)

        except KeyboardInterrupt as keyinter:
            print("See you, then ! :)")
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
        categories_data = [["id", "category"]]

        # creating an AsciiTable object from terminatables,
        # using categories_data
        categories_table = AsciiTable(categories_data)

        print()
        print("Here are the available categories, choose one: ")
        try:
            select_categories = Category.select().order_by(Category.id)
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
                    print("Please, input a valid category.")
                    print("!" * 36)
                    self.display_categories()

            except ValueError as VE:
                print()
                print("!" * 26)
                print("Please input an integer.")
                print("!" * 26)
                self.display_categories()

        except KeyboardInterrupt as keyinter:
            print("See you, then ! :)")
            exit()

        except InternalError as peweeie:
            print()
            print("!" * 83)
            print("A problem occured.\
\nHere's the original message :\n\n", colored("{}".format(peweeie), "red"))
            print("!" * 83)
            print()
            self.menu_actions['main_menu'](self)

    def display_products(self, cat_choice, page, products_p_page, n_of_pages):
        """
        display products in the terminal.
        cat_choice is the category selected by the user.
        """
        # creating the header of the categories table
        products_data = [["id", "Product", "Nutri grade"]]

        # creating an AsciiTable object from terminatables,
        # using products_data
        products_table = AsciiTable(products_data)

        print()
        print("Here are the products, choose one : ")
        print("Next page (n), Previous page (p)")
        try:
            query = Product.select().where(
                Product.cat_id == cat_choice
            ).order_by(
                Product.id
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
                        print("Please, input a valid product.")
                        print("!" * 36)
                        self.display_products(
                            cat_choice,
                            page,
                            products_p_page,
                            n_of_pages,
                        )

                except KeyboardInterrupt as keyinter:
                    print("See you, then ! :)")
                    exit()

                except ValueError as VE:
                    print()
                    print("!" * 36)
                    print("Please, input a number or (n/p).")
                    print("!" * 36)
                    self.display_products(
                        cat_choice,
                        page,
                        products_p_page,
                        n_of_pages,
                    )

        except KeyboardInterrupt as keyinter:
            print("See you, then ! :)")
            exit()

        except InternalError as pie:
            print()
            print("!" * 83)
            print("A problem occured.\
\nHere's the original message :\n\n", colored("{}".format(pie), "red"))
            print("!" * 83)
            print()
            self.menu_actions['main_menu'](self)

        # returns query to be able to display next and previous pages
        return query

    def display_better_product(self, prod_choice):
        """
        Displays a better product than the one chosen by the user.

        """

        # header for the substitute table
        substitute_data = [
            [
                "Name",
                "Nutri grade",
                "Brand(s)",
                "Store(s)",
                "URL",
            ]
        ]

        # transforms the substitute_data list to a table
        substitute_table = AsciiTable(substitute_data)

        cur_product = Product.get(
            Product.id == prod_choice
        )

        # if nutri_grade is a, give a similarly graded product
        if cur_product.nutri_grade == "a":
            substitute_query = Product.select().where(
                Product.nutri_grade == cur_product.nutri_grade,
                Product.cat_id == cur_product.cat_id).order_by(
                fn.Rand()
            ).limit(1)

        # else give a product with a better nutrigrade
        else:
            substitute_query = Product.select().where(
                Product.nutri_grade < cur_product.nutri_grade,
                Product.cat_id == cur_product.cat_id).order_by(
                fn.Rand()
            ).limit(1)

        for substitute in substitute_query:
            sub_brands = self.select_brands(substitute, "id")
            sub_stores = self.select_stores(substitute, "id")
            print()
            print("Here's the suggested replacement:")
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
        print("Would you like to save it to your favorites? (y/n)")

        save_fav = input(" >> ")

        while save_fav not in ["y".lower(), "n".lower()]:
            print('Please input "y" or "n"')
            save_fav = input(" >> ")

        if save_fav.lower() == "y":
            Favorite.create(
                product_id=cur_product.id,
                substitute_id=substitute.id,
            )

            print()
            print(
                "Replacement saved in your favorites ! Back to main menu."
            )
            self.menu_actions['main_menu'](self)

        elif save_fav.lower() == "n":
            print("Replacement ignored. Back to main menu.")
            self.menu_actions['main_menu'](self)

    def select_stores(self, product, product_id):
        """
        Query to select stores from many to many table
        """
        stores = (Store.select().join(Productstore).join(
            Product
        ).where(Product.id == getattr(product, product_id)))

        return stores

    def select_brands(self, product, product_id):
        """
        Query to select brands from many to many table
        """
        brands = (Brand.select().join(Productbrand).join(
            Product
        ).where(Product.id == getattr(product, product_id)))

        return brands

    def display_favs(self):
        """
        Displays the favorites saved by user.
        This function uses colorclass to color the terminal
        It also uses terminaltables to display the data as tables.
        """

        try:
            favorites = Favorite.select()
            count_favs = Favorite.select().count()

            product_data = [
                [
                    'id',
                    colored('Original product', 'red'),
                    colored('Brand(s)', 'yellow'),
                    colored('Store(s)', 'yellow'),
                    colored('Replacement', 'green'),
                    colored('Brand(s)', 'yellow'),
                    colored('Store(s)', 'yellow'),
                ]
            ]

            product_table = AsciiTable(product_data)

            if count_favs == 0:
                print("You did not save any favorite yet. Back to main menu.")
                print()
                self.menu_actions['main_menu'](self)
            else:
                print()
                print("You have", count_favs, "favorite(s).")
                print("Here they are :")
                print("-" * 30)

                # list of ids being displayed
                favorites_ids = []

                for favorite in favorites:
                    favorites_ids.append(favorite.id)

                    substitutes = Product.select().where(
                        Product.id == favorite.substitute_id
                    )
                    products = Product.select().where(
                        Product.id == favorite.product_id
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

        except pymysql.err.InternalError as pymysqlie:
            print()
            print("!" * 83)
            print("A problem occured.\
\nHere's the original message :\n\n", colored("{}".format(pymysqlie), "red"))
            print("!" * 83)
            print()
            self.menu_actions['main_menu'](self)

        except InternalError as peweeie:
            print()
            print("!" * 83)
            print("A problem occured.\
\nHere's the original message :\n\n", colored("{}".format(peweeie), "red"))
            print("!" * 83)
            print()
            self.menu_actions['main_menu'](self)

        except KeyboardInterrupt as keyinter:
            print("See you, then ! :)")
            exit()

    def edit_favs(self, favorites_ids):
        """
        Editing favorites.
        favorites_ids is a list of int of the favorites being displayed
        in the terminal
        """
        print()
        print(
            "Please choose a favorite to delete or (m) \
to go back to main menu."
        )
        edit_fav_choice = input(" >> ")

        try:
            if edit_fav_choice.lower() == "m":
                print("Back to main menu.")
                self.menu_actions['main_menu'](self)

            else:
                try:
                    edit_fav_choice = int(edit_fav_choice)
                    if edit_fav_choice in favorites_ids:
                        self.remove_favs(edit_fav_choice, favorites_ids)
                    else:
                        print("!" * 36)
                        print("Please input a valid favorite.")
                        print("!" * 36)
                        self.edit_favs(favorites_ids)

                except KeyboardInterrupt as keyinter:
                        print("See you, then ! :)")
                        exit()

                except ValueError as VE:
                    print()
                    print("!" * 36)
                    print("Please input a number or (m).")
                    print("!" * 36)
                    self.edit_favs(favorites_ids)

        except KeyboardInterrupt as keyinter:
            print("See you, then ! :)")
            exit()

    def remove_favs(self, edit_fav_choice, favorites_ids):
        """
        Removing favorites from the Favorite table.
        """
        print("Do you really want to delete this favorite? (y/n)")
        remove_fav = input(" >> ")

        while remove_fav not in ["y".lower(), "n".lower()]:
            print('Veuillez entrer "y" ou "n"')
            remove_fav = input(" >> ")
        try:
            edit_fav_choice = int(edit_fav_choice)
            if remove_fav.lower() == "y":
                favorite = Favorite.get(Favorite.id == edit_fav_choice)
                favorite.delete_instance()
                print()
                print("/" * 17)
                print("Favorite deleted !")
                print("/" * 17)
            else:
                print()
                print("!" * 18)
                print("Canceled operation.")
                print("!" * 18)
                self.display_favs()

        except KeyboardInterrupt as keyinter:
                print("See you, then ! :)")
                exit()

        except ValueError as VE:
            print()
            print("!" * 36)
            print("Please input a number or (n).")
            print("!" * 36)
            self.edit_favs(favorites_ids)

        self.display_favs()

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
            print("This is the last page ;).")
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
            print("This is the first page ;).")
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
