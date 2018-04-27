from app import db
from app.models import User, Article, Category, Role
import hashlib

db.drop_all()
db.create_all()
trash = Role(roletitle='trash')
admin = Role(roletitle='admin')
god = Role(roletitle='god')

passwd = hashlib.sha512('123'.encode('utf-8')).hexdigest()

javad = User(username='javad', password_hash=passwd,  email='javad@ubc.com', role=admin)
print (javad)
pewdiepie = User(username='pewdiepie', password_hash=passwd, email='pewdiepie@hotmail.com', role=trash)
print (pewdiepie)



A = Category(category='A')
B = Category(category='B')

md = "### How_to_jazz\n hello __everyone__, I am your jazz wizard\n > today I m gonna teach you how to make some old fashion"

how_to_jazz = Article(title='how_to_jazz',\
        rawcontent=md, \
        author=javad, category=A)
print(how_to_jazz)
how_to_joji= Article(title='how_to_joji',\
        rawcontent='jojijojijojijojijoji\njojiojijoji\njojijojijoji\njojijojijoji', \
        author=javad, category = A)
print(how_to_joji)

pew_news = Article(title='pew_news',\
        rawcontent='pewpewpewepwpew', \
        author=pewdiepie, category=B)
print(pew_news)

YLYL = Article(title='Skalada_du_Folora_du',\
        content='ll', \
        author=pewdiepie, category=B)
print(YLYL)




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
