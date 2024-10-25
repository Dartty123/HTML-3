from flask import Flask ,render_template ,request ,redirect ,url_for

from app.routers.pizza import pizza_route 
from app.models.pizza import Pizza
from app.models.ingredient import Ingredient
from app.models.base import create_db


app = Flask(__name__,static_folder="app/static",template_folder="app/templates")
app.register_blueprint(pizza_route)


if __name__ == "__main__":
    create_db()
    app.run(debug=True)
    @app.get("/")
    def index():
        context = {
            "question": "Яка піца тобі найбільше подобаєтся",
            "answers": ["Гавайська, Морепіца, Велика піца на компію"]
    }
        return render_template("index.html", **context)

@app.get("/add_vote/")
def add_vote():
    vote = request.args.get("answer")
    with open("data/answers.txt", "a", encoding="utf-8") as file:
        file.write(vote + "\n")

    return redirect(url_for("results"))


@app.get("/results/")
def results():
    with open("data/answers.txt", "r", encoding="utf-8") as file:
        answers = file.readlines()

    return render_template("results.html", answers=answers)


if __name__ == "__main__":
    app.run(debug=True)