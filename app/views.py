from app import app
from flask import render_template, session, redirect, url_for
from .forms import LoginForm

@app.route("/index")
@app.route("/")
def index():
    return render_template("index.html", username="mohamede")

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session['username'] = form.username.data
        return redirect(url_for('index'))
    return render_template("login.html", title="Sign up", form=form, \
                            username=session.get('username'))




