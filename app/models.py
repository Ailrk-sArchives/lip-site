from app import db
import hashlib
import markdown2

""" many to many relationship for user-likedarticles relationship"""
liked_articles = db.Table(
    'liked_articles',
    db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('article_id', db.Integer, db.ForeignKey('articles.id'), primary_key=True)
)


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
    # liked articles <many-to-many relationship>
    likedarticles = db.relationship(
        'Article',
        secondary=liked_articles,
        lazy='subquery',
        backref=db.backref('likedusers', lazy=True)
    )

    # role_id
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    """ static filed"""
    @staticmethod
    def get_user(user_id):
        return User.query.get(user_id)

    @staticmethod
    def get_user_by_name(username):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def get_users():
        return User.query.all()

    @staticmethod
    def add_user(username, password, email, role):
        user = User(username=username,
                    password_hash=hashlib.sha512(
                        str(password).encode('utf-8')).hexdigest(),
                    email=email,
                    role=role)
        db.session.add(user)
        db.session.commit()

    @staticmethod
    def authorize_by_id(user_id, role):
        try:
            user = User.get_user(user_id)
            user.role = role
        except BaseException:
            print("id unauthorized")

    @staticmethod
    def delete_user(user_id):
        user = User.get_user(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()

    @staticmethod
    def get_many_user_articles(user_id):
        user = User.get_user(user_id)
        if user:
            return user.articles

    @staticmethod
    def get_many_liked_articles(user_id):
        user = User.get_user(user_id)
        if user:
            return user.likedarticles

    @staticmethod
    def get_many_liked_articles_by_category(user_id, category):
        user = User.get_user(user_id)
        if user:
            return Article.query.filter_by(
                likeduser=user,
                category=category.category
            )

    """ non static field """
    def self_id(self):
        return self.id

    def authorize(self, role):
        try:
            self.role = role
        except BaseException:
            print("autorization error")

        db.session.commit()

    def like_article(self, article):
        if article:
            self.likedarticles.append(article)
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
    rawcontent = db.Column(db.String())
    content = db.Column(db.String())

    # User
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

    @staticmethod
    def get_many_articles():
        return Article.query.order_by(Article.id.desc())

    @staticmethod
    def get_article(article_id):
        return Article.query.get(article_id)

    @staticmethod
    def get_many_articles_by_category(article_cate):
        return Article.query.filter_by(category=article_cate).order_by(Article.id.desc())

    @staticmethod
    def new_article(title, rawcontent, category, author):
        article = Article(
            title=title, rawcontent=rawcontent,
            content=markdown2.markdown(rawcontent),
            category=category, author=author
        )
        db.session.add(article)
        db.session.commit()
        return article

    @staticmethod
    def edit_article(article_id, title, rawcontent, category=None):
        article = Article.query.get(article_id)
        article.title = title
        article.rawcontent = rawcontent
        article.content = markdown2.markdown(rawcontent)
        article.category = category
        db.session.commit()
        return article

    def __repr__(self):
        return '<Article {}  by {}>'.format(self.title, self.author)


class Category(db.Model):
    """
    Category entries
    """
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(64), unique=True)
    color = db.Column(db.String(64), unique=True)

    # one category to many articles
    articles = db.relationship('Article', backref='category')

    @staticmethod
    def get_many_categories():
        return Category.query.all()

    @staticmethod
    def get_category(category):
        return Category.query.filter_by(category=category).first()

    def __repr__(self):
        return '<Category {}>'.format(self.category)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    roletitle = db.Column(db.String(64))
    user = db.relationship('User', backref='role')
