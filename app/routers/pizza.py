from flask import Blueprint, render_template, request, redirect

from app.models.base import Session
from app.models.pizza import Pizza
from app.models.ingredient import Ingredient
from app.data.wheather import get_wheather


pizza_route = Blueprint("pizzas", __name__)


@pizza_route.get("/")
def index():
    wheather = get_wheather("Neratovice")

    if 26 > wheather.get("temp") > 10:
        pizza_name = "Тепла"
    elif wheather.get("temp") <= 10:
        pizza_name = "Холодна"
    elif wheather.get("temp") > 26:
        pizza_name = "Пепероні"

    return render_template("index.html", title="Піцерія", wheather=wheather, pizza_name=pizza_name)


@pizza_route.get("/menu/")
def menu():
    wheather = get_wheather("Kyiv")
    with Session() as session:
        pizzas = session.query(Pizza).all()
        ingredients = session.query(Ingredient).all()

        context = {
            "pizzas": pizzas,
            "ingredients": ingredients,
            "title": "меню",
            "wheather": wheather
        }
        return render_template("menu.html", **context)


@pizza_route.post("/add_pizza/")
def add_pizza():
    with Session() as session:
        name = request.form.get("name")
        price = request.form.get("price")

        ingredients = request.form.getlist("ingredients")
        ingredients = session.query(Ingredient).where(Ingredient.id.in_(ingredients)).all()

        pizza = Pizza(name=name, price=price, ingredients=ingredients)
        session.add(pizza)
        session.commit()
        return redirect("/menu/")