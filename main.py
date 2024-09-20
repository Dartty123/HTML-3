from flask import Flask, render_template, request, redirect

from app.data import db


app = Flask(__name__, static_folder="app/static", template_folder="app/templates")


app = Flask(__name__,)


@app.get("/")
def index():
    return render_template("index.html", title = "Вас вітає піцерія")


@app.get("/menu/")
def menu():
    pizzas = [
        {"name": "Гавайська", "price": 35, "ingredients":"Курка, ананас, томат, сир"},
        {"name": "Цезаро", "price": 40, "ingredients":"Соус'Цезар', листя салату, помідори, пармезан"},
        {"name": "Маргарита", "price": 20, "ingredients":"Томат, помідори, сир"},
        {"name": "Mілано", "price": 25, "ingredients":"Cоус, ковбаса 'Мілано', гриби, сир"},
]
    context = {
        "pizzas": pizzas,
        "title": "меню"
    }
    return render_template("menu.html", **context)


if __name__ == "__main__":
    app.run(debug=True)    