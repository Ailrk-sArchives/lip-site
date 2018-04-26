from app import db
from app.models import User, Article

eric = User.query.filter_by(username="Eric").first()
print (eric.username)
print (eric.password_hash)



