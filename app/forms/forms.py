from flask_wtf import FlaskForm
import wtforms


class ProductForm(FlaskForm):
    name = wtforms.StringField("Введіть своє ім'я")
    pizzas = wtforms.SelectMultipleField("Виберіть піцу")
    submit = wtforms.SubmitField("Купити")


class ReviewForm(FlaskForm):
    name = wtforms.StringField("Введіть своє ім'я")
    grades = wtforms.SelectField("Виберіть оцінку")
    review = wtforms.TextAreaField("Напишіть свій відгук")
    submit = wtforms.SubmitField("Відправити відгук")