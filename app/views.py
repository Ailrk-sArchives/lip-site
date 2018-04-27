from app import app, db
from flask import render_template, session, redirect, url_for, flash 
from .forms import LoginForm, SignupForm, EditorForm
from .models import *
from .utils import SessionManager, logger




@app.route('/index', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def index(): 
    articles = Article.get_many_articles()

    return render_template('index.html', articles=articles, session=session)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            # X the user is not existed. login failed
            SessionManager.login_off(session)
            msg = 'user is not existed'
            flash(msg)
            logger.debug(msg)
            return redirect(url_for('login'))
        else:
            # check the validaty of password
            if  hashlib.sha512(str(form.password.data).encode('utf-8')).hexdigest()\
                             == user.password_hash:
                SessionManager.login_on(session, form.username.data)
                logger.info('User ' + session['username'] +  ' logined')
                return redirect(url_for('index'))
            else:
                # X passwd is not correct, login failed
                msg = 'Invalid password'
                flash(msg)
                logger.warn(msg)
                SessionManager.login_off(session)
                return redirect(url_for('login'))

    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        # check if the user is exist
        if user is None:
            User.add_user(username=form.username.data, \
                        password=form.password.data, \
                        email=form.email.data) 

            SessionManager.login_off(session)
            logger.info('User ' + form.username.data + ' signuped')
            return redirect(url_for('login'))

        else:
            # X given user is existed
            msg = 'username is already existed'
            flash(msg)
            logger.debug(msg)

            SessionManager.login_off(session)
            return redirect(url_for('signup'))
    return render_template('signup.html', form=form)

@app.route('/article/<int:article_id>')
def show_article(article_id):
    article = Article.get_article(article_id)
    return render_template('article.html', article=article)

@app.route('/new', methods=['GET', 'POST'])
def new():
    """
    Create empty EditorForm.
    """
    form = EditorForm()
    categories = Category.get_many_categories()

    if session['logined'] and session['username']:

        # admin check. only admin can create article
        if session['roletitle'] == Role.query.filter_by(roletitle='admin').first().roletitle:
            if form.validate_on_submit():
                article= Article.new_article(title=form.articlename.data, \
                                    rawcontent=form.textarea.data, \
                                    category=Category.get_category(form.category.data),\
                                    author=User.get_user_by_name(username=session['username']) )        
                if article:
                    logger.info('new article ' + '<' + article.title + '> created')
                    return redirect(url_for('show_article', article_id=article.id))
                else:
                    flash('invalid input')
                    return redirect(url_for('new'))

        else:
            logger.error('Unauthorized, unable to create article')
            flash('Only admin can create articles')
            return redirect(url_for('index'))
    
        if form.errors: print(form.errors)


    else:
        logger.error( 'Unlogined, unable to create article')
        flash('please login before create article')
        SessionManager.login_off(session)
        return redirect(url_for('index'))

    return render_template('editor.html', form=form, categories=categories)

@app.route('/edit/article/<int:article_id>', methods=['GET', 'POST'])
def edit(article_id):
    """
    Create EditorForm with article and title
    """
    form = EditorForm()
    article = Article.get_article(article_id)

    if session['logined'] and session['username']:
        categories = Category.get_many_categories()

        if form.validate_on_submit():
            edited_article = Article.edit_article(article_id=article_id,\
                                title=form.articlename.data, \
                                rawcontent=form.textarea.data, \
                                category=Category.get_category(form.category.data) )
            if edited_article:
                logger.info('new article ' + '<' + article.title + '> created')
                return redirect(url_for('show_article', article_id=article.id))
            else:
                flash('invalid input')
                return redirect(url_for('new'))

        print(form.errors)

    else:
        logger.error('Not logined, unable to create article')
        flash('please login before create article')
        SessionManager.login_off(session)
        return redirect(url_for('index'))

   
    form.articlename.data = article.title
    form.textarea.data = article.rawcontent
    form.category.data = article.category.category

    return render_template('editor.html', form=form, categories=categories)

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/logout')
def logout():
    SessionManager.login_off(session)
    return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(403)
def forbidden(e):
    return render_template('402.html'),403

@app.errorhandler(500)
def internal_server_error(e):
    return render_templatel('500.html'), 500

@app.errorhandler(502)
def bad_gateway(e):
    return render_template('502.html'), 502

@app.route('/about')
def about():
    return render_template('about.html')
