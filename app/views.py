from app import app, db
from flask import render_template, session, redirect, url_for
from .forms import LoginForm
from .models import *

@app.route("/index")
@app.route("/")
def index():
    articles = Article.get_many_articles()
    print(articles)
    return render_template("index.html", articles=articles)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session['username'] = form.username.data
        return redirect(url_for('index'))
    return render_template("login.html", title="Sign up", form=form, \
                            username=session.get('username'))




