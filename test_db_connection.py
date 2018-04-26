from app import db
from app.models import User, Article, Category
import hashlib

db.drop_all()
db.create_all()

passwd = hashlib.sha512('123'.encode('utf-8')).hexdigest()

javad = User(username='javad', password_hash=passwd,  email='javad@ubc.com')
print (javad)
pewdiepie = User(username='pewdiepie', password_hash=passwd, email='pewdiepie@hotmail.com')
print (pewdiepie)


A = Category(category='A')
B = Category(category='B')

how_to_jazz = Article(title='how_to_jazz',\
        content='skjlasjflsacl', \
        author=javad, category=A)
print(how_to_jazz)
how_to_joji= Article(title='how_to_joji',\
        content='jojijojijojijojijoji\njojiojijoji\njojijojijoji\njojijojijoji', \
        author=javad, category = A)
print(how_to_joji)

pew_news = Article(title='pew_news',\
        content='pewpewpewepwpew', \
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
    print()
print(Article.get_article(1).id)
