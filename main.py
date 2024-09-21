from flask import Flask,  render_template
from app.data import db


app = Flask(__name__, static_folder="app/static", template_folder="app/templates")


@app.get("/")
def index():
    return render_template("index.html", title = "Вас вітає піцерія")

@app.get("/menu/")
def menu():
    pizza_db = db.get_PIZZA()
    pizzas = []
    for pizza in pizza_db:
        pizzas.append(
            {"name": pizza[1], "ingredients": pizza[2], "price": pizza[3]}
        )

    context = {
        "pizzas": pizzas,
        "title": "меню"
    }
    return render_template("menu.html", **context)


if __name__ == "__main__":
    app.run(debug=True)