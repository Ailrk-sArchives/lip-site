from app import db

class User(db.Model):
    """
    User entries
    """
    id = db.Column(db.Integer,  primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128));
    
    # author's forign key
    articles = db.relationship('Articles', backref='user')

    def __repr__(self):
        return "<User {}>".format(self.username)

class Articles(db.Model):
    """
    Article entries
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True)
    content = db.Column(db.String(5000), index=True)

    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))


