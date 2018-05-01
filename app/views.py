from app import app, db
from flask import render_template, session, redirect, url_for, flash, abort
from .forms import LoginForm, SignupForm, EditorForm
from .models import *
from .utils import SessionManager, logger

# context processors
@app.context_processor
def inject_categories():
    def create_categories_list():
        return Category.get_many_categories()
    return dict(create_categories_list=create_categories_list)

@app.context_processor
def inject_current_user():
    def get_current_user():
        return User.get_user_by_name(username=session['username'])
    return dict(get_current_user=get_current_user)

@app.context_processor
def inject_user():
    def get_user(username):
        return User.get_user_by_name(username=username)
    return dict(get_user=get_user)


# routing
@app.route('/index', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
@app.route('/<category>', methods=['GET', 'POST'])
def index(category=None): 
    articles=[]
    if not category:
        articles = Article.get_many_articles()
    else:
        category = Category.query.filter_by(category=category).first()
        if not category: abort(404)
        articles = Article.get_many_articles_by_category(article_cate=category)
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
                        email=form.email.data, \
                        role=Role(roletitle='admin')) 

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
    
    if not article: abort(404)

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

    if not article: abort(404)

    if article.author.username != session['username']:
        flash('Only author can modify their own articles')
        return redirect(url_for('index'))

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
@app.route('/profile/<display>')
@app.route('/profile/user/<other_username>')
@app.route('/profile/user/<other_username>/<display>')
def profile(other_username=None, display=None):

    if session['username'] and session['logined']:
        # check if it is routing to other people's page or user's own profile
        if other_username == None:
            if display == 'liked_articles':
                return render_template('profile.html',other_username=None,\
                        display='liked_articles')

            elif display == 'created_articles':
                return render_template('profile.html',other_username=None, \
                        display='created_articles')

        else:
            if display == 'liked_articles':
                return render_template('profile.html',other_username=other_username,\
                        display='liked_articles')

            elif display == 'created_articles':
                return render_template('profile.html',other_username=other_username, \
                        display='created_articles')

            else:
                return render_template('profile.html',other_username=other_username, \
                        display='created_articles')


    # if Unlogined user try to access his own personal profile
    elif not other_username:
        flash('please login before access profile')
        return redirect(url_for('index'))
    else:
        return render_template('profile.html',other_username=other_username,\
                display='created_articles')

    return render_template('profile.html', other_username=None, display='created_articles')

@app.route('/logout')
def logout():
    SessionManager.login_off(session)
    return redirect(url_for('index'))

@app.route('/like/<int:article_id>')
def like(article_id):
    if session['username'] and session['logined']:
        user = User.get_user_by_name(username=session['username'])
        user.like_article(Article.get_article(article_id))
        return redirect(url_for('show_article', article_id=article_id))
    else:
        flash('please login')
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
