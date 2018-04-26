from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,\
    TextAreaField
from wtforms.validators import DataRequired, Email

class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me')
    submit = SubmitField('Login')

class SignupForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    email = StringField('e-mail', validators=[DataRequired(), Email()])
    submit = SubmitField('Signup')

class EditorForm(FlaskForm):
    articlename = StringField('article name', validators=[DataRequired()])
    textarea = TextAreaField('textarea', validators=[DataRequired()])     
    submit = SubmitField('Publish')
     


