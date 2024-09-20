import sqlite3


def create_table():
    try:
        sql_con = sqlite3.connect("first_db.db")
        cursor = sql_con.cursor()

        with open("create_table.sql") as fh:
            query = fh.read()

        cursor.execute(query)
        sql_con.commit()
        cursor.close()
        print("Таблиця успішно створена")

    except sqlite3.Error as error:
        print("Помилка: ", error)

    finally:
        if sql_con:
            sql_con.close()
            print("З'єднання з базою даних успішно завершене")


def insert_data():
    try:
        sql_con = sqlite3.connect("first_db.db")
        cursor = sql_con.cursor()

        with open("insert_data.sql") as fh:
            query = fh.read()

        cursor.execute(query)
        sql_con.commit()
        cursor.close()
        print("Дані успішно записані")

    except sqlite3.Error as error:
        print("Помилка: ", error)

    finally:
        if sql_con:
            sql_con.close()
            print("З'єднання з базою даних успішно завершене")


def insert_data_by_values(first_name: str, last_name: str, age: int|None = None, grade: float|None = None):
    try:
        sql_con = sqlite3.connect("first_db.db")
        cursor = sql_con.cursor()

        query = "INSERT INTO Students (first_name, last_name, age, grade) VALUES (?, ?, ?, ?)"
        data = (first_name, last_name, age, grade)

        cursor.execute(query, data)
        sql_con.commit()
        cursor.close()

    except sqlite3.Error as error:
        print(f"SQL_Error: {error}")

    finally:
        if sql_con:
            sql_con.close()
            print("З'єднання з базою даних успішно завершене")


def insert_data_by_employees(data: list):
    try:
        sql_con = sqlite3.connect("first_db.db")
        cursor = sql_con.cursor()

        query = "INSERT INTO Employees (first_name, last_name, age, position) VALUES (?, ?, ?, ?)"

        cursor.executemany(query, data)
        sql_con.commit()
        cursor.close()

    except sqlite3.Error as error:
        print(f"SQL_Error: {error}")

    finally:
        if sql_con:
            sql_con.close()
            print("З'єднання з базою даних успішно завершене")


def get_students() -> dict:
    data = {
        "error": "",
        "students": []
    }

    try:
        sql_con = sqlite3.connect("first_db.db")
        cursor = sql_con.cursor()

        cursor.execute("SELECT * FROM Students;")
        data["students"] = cursor.fetchall()

        for item in data:
            print(f"{item = }")

        cursor.close()
        print("Дані успішно записані")

    except sqlite3.Error as error:
        print("Помилка: ", error)
        data["error"] = error

    finally:
        if sql_con:
            sql_con.close()
            print("З'єднання з базою даних успішно завершене")

        return data