# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
# *                          HAM_Database by Jacopx                         *
# *                  https://github.com/Jacopx/HAM_Database                 *
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

import mysql.connector as mariadb
import os
import time
import configparser
from prettytable import PrettyTable

clear = lambda: os.system('clear')


def main():
    config = configparser.ConfigParser()
    config.read('configuration/mycnf.ini')

    usr = config['DEFAULT']['USER']
    pwd = config['DEFAULT']['PWD']
    host = config['DEFAULT']['HOST']
    port = config['DEFAULT']['PORT']
    db = config['DEFAULT']['DB']

    # Starting connection to MySQL database
    mariadb_connection = mariadb.connect(user=usr, password=pwd, host=host, port=port, database=db)
    cursor = mariadb_connection.cursor()

    # Text menu in Python
    loop = True

    while loop:
        print_menu()
        choice = int(input("Enter your choice [1-5]: "))

        if choice == 1:
            new_ham(cursor, mariadb_connection)
        elif choice == 2:
            search_ham(cursor)
        elif choice == 3:
            delete_operator(cursor, mariadb_connection)
        elif choice == 4:
            show_all_ham(cursor)
        elif choice == 5:
            print("Exiting from software, bye!")
            loop = False  # This will make the while loop to end as not value of loop is set to False
        else:
            # Any integer inputs other than values 1-5 we print an error message
            print("Wrong option selection. Enter any key to try again..")

    return 0


def print_menu():
    clear()  # This function not work inside the IDE console
    print(30 * "-", "MENU", 30 * "-")
    print("1. Add new HAM operator")
    print("2. Search for operator")
    print("3. Delete operator")
    print("4. Show all operators")
    print("5. Exit")
    print(67 * "-")


def new_ham(cursor, connection):
    id = input("ID: ").upper()
    name = input("Name: ")
    location = input("Location: ")
    comments = input("Comments: ")

    # Print datas for confimation
    print("New HAM operator:\n")

    x = PrettyTable(["ID", "Name", "Location", "Comments"])
    x.add_row([id, name, location, comments])
    print(x)

    choice = input("\nConfirm the data (y/n)? ")
    if choice == "y":
        cursor.execute("INSERT INTO Operators (ID, name, loc, comments, added) VALUES (%s,%s,%s,%s,%s)",
            (id, name, location, comments, time.strftime('%Y-%m-%d %H:%M:%S')))
        connection.commit()


def search_ham(cursor):
    id = input("ID of operator to be SEARCH: ").upper()
    cursor.execute("SELECT * FROM Operators WHERE ID='" + id + "'")
    results = cursor.fetchall()

    x = PrettyTable(["ID", "Name", "Location", "Comments", "Added"])

    for line in results:
        x.add_row(line)

    print(x)

    input("\nClose? ")


def show_all_ham(cursor):
    cursor.execute("SELECT * FROM Operators ORDER BY Added")
    results = cursor.fetchall()

    x = PrettyTable(["ID", "Name", "Location", "Comments", "Added"])

    for line in results:
        x.add_row(line)

    print(x)

    input("\nClose? ")


def delete_operator(cursor, connection):
    id = input("ID of operator to be DELETE: ").upper()

    print("Are you sure to delete:\n")
    print("ID:\t" + id)

    choice = input("\nConfirm (y/n)? ")
    if choice == "y":
        cursor.execute("DELETE FROM Operators WHERE ID='" + id + "'")
        connection.commit()


if __name__ == "__main__":
    main()
