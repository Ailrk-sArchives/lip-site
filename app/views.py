from app import app, db
from flask import render_template, session, redirect, url_for
from .forms import LoginForm
from .models import *
import hashlib

@app.route('/index', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def index(): 
    articles = Article.get_many_articles()

    """ login and signup """
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            user = User(username=form.username.data)
            db.session.add(user)
            session['logined'] = False
        else:
            # check the validaty of password
            if ( hashlib.sha1(form.password.data).hexdigest() == \
                    user.password_hash):
                session['logined'] = True
                session['username'] = form.username.data
                form.username.data = ''
                form.password.data = ''
            else:
                return redirect(url_for('index'))

    return render_template("index.html", articles=articles, form=form, \
                            session=session)

@app.route('/article/<title>')

