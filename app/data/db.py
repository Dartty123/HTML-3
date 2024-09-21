import sqlite3


def create_table():
    try:
        sql_con = sqlite3.connect("pizzas.db")
        cursor = sql_con.cursor()

        with open("data/create_table.sql") as file:
            query = file.read()

        cursor.execute(query)
        sql_con.commit()
        cursor.close()

    except sqlite3.Error as error:
        print(f"Error: {error}")

    finally:
        if sql_con:
            sql_con.close()


def insert_data(name: str, ingredients: str, price: float):
    try:
        sql_con = sqlite3.connect("pizzas.db")
        cursor = sql_con.cursor()

        query = "INSERT INTO Pizzas (name, ingredients, price) VALUES (?, ?, ?)"
        data = (name, ingredients, price)

        cursor.execute(query, data)
        sql_con.commit()
        cursor.close()

    except sqlite3.Error as error:
        print(f"Error: {error}")

    finally:
        if sql_con:
            sql_con.close()


def get_pizzas():
    try:
        sql_con = sqlite3.connect("pizzas.db")
        cursor = sql_con.cursor()

        query = "SELECT * FROM Pizzas"

        cursor.execute(query)
        pizzas = cursor.fetchall()
        cursor.close()
        return pizzas

    except sqlite3.Error as error:
        print(f"Error: {error}")

    finally:
        if sql_con:
            sql_con.close()