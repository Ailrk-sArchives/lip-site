from app import app, db
from flask import render_template, session, redirect, url_for
from .forms import LoginForm, SignupForm
from .models import *
import hashlib

@app.route('/index', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def index(): 
    articles = Article.get_many_articles()

    return render_template('index.html', articles=articles, session=session)

@app.route('/login')
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            user = User(username=form.username.data)
            db.session.add(user)
            session['logined'] = False
        else:
            # check the validaty of password
            if ( hashlib.sha512(form.password.data).hexdigest() == \
                    user.password_hash):
                session['logined'] = True
                session['username'] = form.username.data
                form.username.data = ''
                form.password.data = ''
            else:
                return redirect(url_for('index'))
    return render_template('login.html', form=form)


@app.route('/signup')
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            user = User(username=form.username.data)
            db.session.add(user)
            session['logined'] = False
        else:
            # check the validaty of password
            if ( hashlib.sha512(form.password.data).hexdigest() == \
                    user.password_hash):
                session['logined'] = True
                session['username'] = form.username.data
                form.username.data = ''
                form.password.data = ''
            else:
                return redirect(url_for('index'))
    return render_template('signup.html', form=form)

@app.route('/article/<id>')
def show_article(id):
    article = Article.get_article(id)
    return render_template('article.html', article=article)


