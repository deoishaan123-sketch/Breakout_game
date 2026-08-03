from breakout import start_game
from datetime import date
from wsgiref.validate import validator

from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from flask import Flask, abort, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
# from flask_gravatar import Gravatar
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms.validators import DataRequired, Email

# Import your forms from the forms.py
# from forms import CreatePostForm

app=Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor=CKEditor(app)
bootstrap=Bootstrap5(app)

login_manager=LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

class LoginFlask(FlaskForm):
    email=StringField("Email",validators=[DataRequired(),Email()])
    password=PasswordField("Password",validators=[DataRequired()])
    submit=SubmitField("Let me in")

class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


class Registerform(FlaskForm):
    email=StringField("Email",validators=[DataRequired(),Email()])
    password=PasswordField("Password",validators=[DataRequired()])
    name=StringField("name",validators=[DataRequired()])
    submit=SubmitField("Sign up")

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(100))

with app.app_context():
    db.create_all()

@app.route('/register',methods=["GET","POST"])
def register():
    form = Registerform()
    if form.validate_on_submit():

        email = request.form.get('email')
        result= db.session.execute(db.select(User).where(User.email==email))
        user=result.scalar()

        if user:
            flash("This email already in Use!")
            return redirect(url_for("login"))

        hash_and_salted_password=generate_password_hash(
            password=request.form.get('password'),
            method="pbkdf2:sha256",
            salt_length=8

        )

        new_user=User(
        email=request.form.get('email'),
        password=hash_and_salted_password,
        name=request.form.get('name')
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("play_game"))

    return render_template("register.html",form=form)

@app.route('/login',methods=["GET","POST"])
def login():
    form=LoginFlask()
    if form.validate_on_submit():
        email=form.email.data
        password=form.password.data
        result=db.session.execute(db.select(User).where(User.email==email))
        user=result.scalar()


        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for("login"))

        elif not check_password_hash(user.password, password):
            flash("Password incorrect, please try again.")
            return redirect(url_for("login"))

        login_user(user)
        return redirect(url_for("play_game"))

    return render_template("login.html",form=form)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/play")
def play_game():
    if current_user.is_authenticated:
        return render_template("game.html")
    return render_template("start.html")

@app.route("/game")
def game():
    if not current_user.is_authenticated:
        return redirect(url_for("play_game"))
    start_game()
    return redirect(url_for('get_all_posts'))

@app.route("/")
def get_all_posts():
    return render_template("index.html")


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
