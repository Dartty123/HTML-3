from flask import Blueprint, render_template, request, redirect, url_for

from app.models.base import Session
from app.models.pizza import Pizza
from app.models.ingredient import Ingredient
from app.data.wheather import get_wheather
from app.data import wheather


pizza_route = Blueprint("pizzas", __name__)


@pizza_route.get("/")
def index():
    wheather = get_wheather("Neratovice")
    if 26 > wheather.get("temp") > 10:
        pizza_name = "Гавайська"
    elif wheather.get("temp") <= 10:
        pizza_name = "Морепіца"
    elif wheather.get("temp") > 26:
        pizza_name = "Велика піца на компанію"
    
    return render_template("index.html", title="Піцерія", wheather=wheather,pizza_name=pizza_name)


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
        return render_template("menu.html", **context )

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


@pizza_route.get("/pizza/delete/<int:id>/")
def del_pizza(id):
    with Session() as session:
        pizza = session.query(Pizza).where(Pizza.id == id).first()
        session.delete(pizza)
        session.commit()

    return redirect(url_for("pizzas.index"))


@pizza_route.get("/pizza/edit/<int:id>/")
@pizza_route.post("/pizza/edit/<int:id>/")
def edit_pizza(id):
    with Session() as session:
        pizza = session.query(Pizza).where(Pizza.id == id).first()

        if request.method == "POST":
            pizza.name = request.form.get("name")
            pizza.price = request.form.get("price")
            session.commit()
            return redirect(url_for("pizzas.menu", ))
        return render_template("edit_pizza.html", pizza=pizza, wheather=wheather)
    
@pizza_route.get("/")
def index():
        context = {
            "question": "Яка піца тобі найбільше подобаєтся",
            "answers": ["Гавайська, Морепіца, Велика піца на компію"]
    }
        return render_template("index.html", **context)

@pizza_route.get("/add_vote/")
def add_vote():
    vote = request.args.get("answer")
    with open("data/answers.txt", "a", encoding="utf-8") as file:
        file.write(vote + "\n")

    return redirect(url_for("results"))


@pizza_route.get("/results/")
def results():
    with open("data/answers.txt", "r", encoding="utf-8") as file:
        answers = file.readlines()

    return render_template("results.html", answers=answers)
