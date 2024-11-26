from flask import Blueprint, render_template, request, redirect, url_for

from app.models.base import Session
from app.models.pizza import Pizza,Review,Grade
from app.models.ingredient import Ingredient
from app.data.wheather import get_wheather
from app.forms import forms

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

    with Session() as session:
        pizzas = session.query(Pizza).all()
        pizza_form = forms.PizzaForm()
        pizza_form.pizzas.choices = []

        for pizza in pizzas:
            pizza_form.pizzas.choices.append((pizza.name, pizza.name))

        if request.method == "POST":
            name = pizza_form.name.data
            pizzas = pizza_form.pizzas.data
            pizzas_db = []

            for pizza in pizzas:
                pizza_db = session.query(pizza.pizza).where(pizza.pizza.name == pizza).first()
                pizzas_db.append(pizza_db)

            shop_list = pizza.ShopList(name=name, pizzas=pizzas_db)
            session.add(shop_list)
            session.commit()

        return render_template("index.html", form=pizza_form)
    
    return render_template("poll.html", title="Піцерія", wheather=get_wheather,pizza_name=pizza_name)


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
        return render_template("edit_pizza.html", pizza=pizza, wheather=get_wheather)
    
@pizza_route.get("/poll/")
def poll():
        context = {
            "question": "Яка піца тобі найбільше подобаєтся",
            "answers": ["Гавайська, Морепіца, Велика піца на компію"]
    }
        return render_template("poll.html", **context)

@pizza_route.get("/add_vote/")
def add_vote():
    vote = request.args.get("answer")
    with open("app/data/answers.txt", "a", encoding="utf-8") as file:
        file.write(vote + "\n")

    return redirect(url_for("results"))


@pizza_route.get("/results/")
def results():
    with open("app/data/answers.txt", "r", encoding="utf-8") as file:
        answers = file.readlines()

    return render_template("results.html", answers=answers)


@pizza_route.route("/review/", methods=["GET", "POST"])
def review():
    with Session() as session:
        review_form = forms.ReviewForm()
        review_form.grades.choices = [(1, 1), (2, 2), (3, 3)]
        grades = session.query(Grade).all()

        for grade in grades:
            review_form.grades.choices.append((grade.grade, grade.grade))

        if request.method == "POST":
            name = review_form.name.data
            grade = review_form.grades.data
            grade_db = session.query(Grade).where(Grade.grade == grade).first()
            text = review_form.review.data

            review_db = Review(name=name, grade=grade_db, text=text)
            session.add(review_db)
            session.commit()

        return render_template("review.html", form=review_form)