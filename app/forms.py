from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,\
    TextAreaField
from wtforms.validators import DataRequired 

class LoginForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("remember_me")
    submit = SubmitField("Login")

class SignupForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Signup")

class EditorForm(FlaskForm):
    articlename = StringField("username", validators=[DataRequired()])
    textarea = TextAreaField(validators=[DataRequired()])     
    submit = SubmitField("Publish")
     


