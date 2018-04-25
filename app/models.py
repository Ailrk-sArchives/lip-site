from app import db

class User(db.Model):
    """
    User entries
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128));
    
    # author's forign key
    articles = db.relationship('Article', backref='author', lazy=True)

    @staticmethod
    def get_user(id):
        return User.query.get(id).first()

    @staticmethod
    def get_users():
        return User.query.all()


    def __repr__(self):
        return "<User {}>".format(self.username)

class Article(db.Model):
    """
    Article entries
    """
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True)
    content = db.Column(db.String(5000), index=True)

    # User
    author_id= db.Column(db.Integer, db.ForeignKey('users.id'))

    @staticmethod
    def get_many_articles():
        return Article.query.all()

    @staticmethod
    def get_article(id):
        return Article.query.get(id).first()

        

    def __repr__(self):
        return "<Article {}  by {}>".format(self.title, self.author)


