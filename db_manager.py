from app import db
from app.models import User, Article, Category
import hashlib
import markdown2


class Manager():
    def __init__(self):
        self.env = {
            'add': lambda callback: self.add(callback),
            'get': lambda callback: self.get(callback),
            'remove': lambda callback: self.remove(callback),
            'edit': lambda callback: self.edit(callback),
            'hashpass': lambda rawpass: self.hashpass(rawpass)
        }

        self.add_callbacks = {
            'category': lambda: self.new_category(),
            'user': lambda: self.new_user(),
            'article': lambda: self.new_article()
        }

        self.get_callbacks = {
            'category': lambda args: Category.get_category(args[0]),
            'categories': lambda args: Category.get_many_categories(),
            'user': lambda args: User.get_user_by_name(args[0]),
            'article': lambda args: Article.get_article(args[0]),
            'articles': lambda args: Article.get_many_articles_by_category(args[0])
        }

        self.remove_callbacks = {
            'user': lambda args: User.delete_user(args[0])
        }

        self.edit_callbacks = {
            'article': lambda args: Article.edit_article(args[0], args[1], args[2])
        }

    def run(self, instruction, data_object, args):
        self.data_args = args
        self.env[instruction](data_object)
        db.session.commit()

    def hashpass(self, rawpass):
        return hashlib.sha512(rawpass.encode('utf-8')).hexdigest()

    def add(self, callback):
        res = self.add_callbacks[callback]()
        print(res)
        db.session.add_all([res])

    def get(self, callback):
        print(self.get_callbacks[callback](self.data_args))

    def edit(self, callback):
        print(self.edit_callbacks[callback](self.data_args))

    def remove(self, callback):
        print(self.remove_callbacks[callback](self.data_args))

    def new_category(self):
        return Category(category=self.data_args[0])

    def new_user(self):
        return User(username=self.data_args[0],
                    password_hash=self.env['hashpass'](self.data_args[1]),
                    email=self.data_args[2])

    def new_article(self):
        return Article(title=self.data_args[0],
                       rawcontent=self.data_args[1],
                       content=markdown2.markdown2(self.data_args[1]),
                       category=Category.get_category(self.data_args[2]),
                       author=User.get_user_by_name(self.data_args[3]))


manager = Manager()

while True:
    tokens = input('> ').split(' ')
    if len(tokens) == 0 or tokens[0] == '':
        continue
    if tokens[0] == 'exit':
        break
    manager.run(tokens[0], tokens[1], tokens[2:])
