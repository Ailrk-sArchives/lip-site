from app import db
from app.models import User, Article

db.drop_all()
db.create_all()

javad = User(username="javad")
print (javad)
pewdiepie = User(username="pewdiepie")
print (pewdiepie)

how_to_jazz = Article(title="how_to_jazz",\
        content="skjlasjflsacl", \
        author=javad)
print(how_to_jazz)
how_to_joji= Article(title="how_to_joji",\
        content="jojijojijojijojijoji\njojiojijoji\njojijojijoji\njojijojijoji", \
        author=javad)
print(how_to_joji)

pew_news = Article(title="pew_news",\
        content="pewpewpewepwpew", \
        author=pewdiepie)
print(pew_news)

YLYL = Article(title="Skalada_du_Folora_du",\
        content="ll", \
        author=pewdiepie)
print(YLYL)


db.session.add_all([how_to_jazz,how_to_joji,javad, pewdiepie])
db.session.commit()
print(Article.get_many_articles()[0].id)
print(Article.get_article(1).id)
