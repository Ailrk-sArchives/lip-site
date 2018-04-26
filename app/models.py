from app import db
import hashlib

class User(db.Model):
    """
    User entries
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(128))
    
    # author's forign key
    articles = db.relationship('Article', backref='author', lazy=True)

    @staticmethod
    def get_user(user_id):
        return User.query.get(user_id)

    @staticmethod
    def get_users():
        return User.query.all()

    def add_user(username, password, email):
        user = User(username=username, \
                    password_hash= \
                    hashlib.sha512( str(password).encode('utf-8')).hexdigest(),\
                    email=email)

        db.session.add(user)
        db.session.commit()


    def __repr__(self):
        return '<User {}>'.format(self.username)

class Article(db.Model):
    """
    Article entries
    """
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True)
    content = db.Column(db.String())

    # User
    author_id= db.Column(db.Integer, db.ForeignKey('users.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

    @staticmethod
    def get_many_articles():
        return Article.query.all()

    @staticmethod
    def get_article(article_id):
        return Article.query.get(article_id)

    def new_article(title, content, category,  author):
        article = Article(title=title, content=content, \
                            category=category, author=author)
        db.session.add(article)
        db.session.commit()
        return article.id

    def edit_article(article_id, title, content, category):
        article = Article.query.get(article_id)
        article.title = title
        article.content = content
        article.category = category
        db.session.commit()


    def __repr__(self):
        return '<Article {}  by {}>'.format(self.title, self.author)

class Category(db.Model):
    """
    Category entries
    """
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(64))

    # one category to many articles
    articles = db.relationship('Article', backref='category')

    @staticmethod
    def get_category(category):
        return Category.query.filter_by(category=category).first()
        
    def __repr__(self):
        return '<Category {}>'.format(self.category) 


