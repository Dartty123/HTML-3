from flask import Flask, render_template


app = Flask(__name__,)


@app.get("/")
def index():
    return render_template("index.html", title = "Вас вітає піцерія")


@app.get("/menu/")
def menu():
    pizzas = [
        {"name": "Гавайська", "price": 35},
        {"name": "Цезаро", "price": 40},
        {"name": "Маргарита", "price": 20},
        {"name": "Mілано", "price": 25},
]
    context = {
        "pizzas": pizzas,
        "title": "меню"
    }
    return render_template("menu.html", **context)


if __name__ == "__main__":
    app.run(debug=True)    