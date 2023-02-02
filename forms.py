from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, DateField, TextAreaField, EmailField
from wtforms.validators import DataRequired


class CreateItemForm(FlaskForm):
    title = StringField("Portfolio Item Title", validators=[DataRequired()])
    description = TextAreaField("Portfolio Item Description", validators=[DataRequired()])
    due_date = StringField("Due Date (mm/dd/yyyy)", validators=[DataRequired()])
    submit = SubmitField("Submit")


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class RegistrationForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Sign Up")