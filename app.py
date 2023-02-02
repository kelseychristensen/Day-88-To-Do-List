from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_bootstrap import Bootstrap
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import smtplib
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from forms import CreateItemForm, RegistrationForm, LoginForm
from flask_ckeditor import CKEditor
from datetime import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = "goi4924rvfadjfo94hbiodaajfda39u"
ckeditor = CKEditor(app)
Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def logged_in(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        if current_user.is_authenticated:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('register'))
    return decorated_func


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100),unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)

    items = relationship("Item", back_populates="author")

class Item(db.Model):
    __tablename__ = "list-items"
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    author = relationship("User", back_populates="items")

    title = db.Column(db.String(250), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    due_date = db.Column(db.String(250), nullable=False)
    status = db.Column(db.Integer, nullable=False)


@app.route('/')
def home():
    if current_user.is_authenticated:
        items = current_user.items
        return render_template("index.html", all_items=items)
    else:
        return render_template("index.html")

@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():

        if User.query.filter_by(email=form.email.data).first():
            #User already exists
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))

        hash_and_salted_password = generate_password_hash(
            password=form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            email=form.email.data,
            password=hash_and_salted_password,
            name=form.name.data,
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("home"))
    return render_template("register.html", form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for("home"))
    return render_template("login.html", form=form, logged_in=current_user.is_authenticated)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/new_item", methods=["GET", "POST"])
@logged_in
def new_item():
    form = CreateItemForm()
    if form.validate_on_submit():
        item_to_add = Item(
            title=form.title.data,
            description=form.description.data,
            author=current_user,
            due_date=form.due_date.data,
            status=0
        )
        db.session.add(item_to_add)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("new_item.html", form=form)


@app.route("/edit-item/<int:item_id>", methods=["GET", "POST"])
def edit_item(item_id):
    item = Item.query.get(item_id)
    edit_form = CreateItemForm(
        title=item.title,
        description=item.description,
        due_date=item.due_date
    )
    if edit_form.validate_on_submit():
        item.title = edit_form.title.data
        item.description = edit_form.description.data
        item.due_date = edit_form.due_date.data
        db.session.commit()
        return redirect(url_for("home", item_id=item_id))

    return render_template("new_item.html", form=edit_form)


@app.route("/complete/<int:item_id>")
def complete(item_id):
    item_to_complete = Item.query.get(item_id)
    item_to_complete.status = 1
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/undo_complete/<int:item_id>")
def undo_complete(item_id):
    item_to_complete = Item.query.get(item_id)
    item_to_complete.status = 0
    db.session.commit()
    return redirect(url_for("home"))

if __name__ == '__main__':
    app.run(debug=True)
