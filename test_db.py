from app import db
from app.models import User, Article

db.drop_all()
db.create_all()
javad = User(username="javad")
pewdiepie = User(username="javad")

how_to_jazz = Article(title="how_to_jazz",\
        content="skjlasjflsacl", \
        author=javad)
how_to_joji= Article(title="how_to_joji",\
        content="jojijojijojijojijoji", \
        author=javad)

pew_news = Article(title="pew_news",\
        content="pewpewpewepwpew", \
        author=pewdiepie)

YLYL = Article(title="Skalada_du_Folora_du",\
        content="ll", \
        author=pewdiepie)



db.session.add_all([how_to_jazz,how_to_joji,javad])
db.session.commit()
print(Article.get_many_articles())
print()
print(Article.get_article(1))
