from app import db
from app.models import User, Article, Category, Role
import hashlib


passwd = hashlib.sha512('123'.encode('utf-8')).hexdigest()


db.session.add_all([how_to_jazz,how_to_joji,javad, pewdiepie])
db.session.commit()

for a in Article.get_many_articles():
    print(a.title)
    print(a.author)
    print(a.category)
    print(a.rawcontent)
    print(a.content)
    print()

print ()

for a in Role.query.all():
    print(a.roletitle)
print(Article.get_article(1).id)

javad.authorize(admin)
User.authorize_by_id(2, god)
for a in User.query.all():
    print(a.username)
    print(a.role.roletitle)
