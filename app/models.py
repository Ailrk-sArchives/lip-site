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

    def get_many_articles():
        return Article.query.all()

    def get_article(id):
        return Article.query.get(id).first()

        

    def __repr__(self):
        return "<Article {}  by {}>".format(self.title, self.author)


