from app import db
from app.models import User, Article, Category
import hashlib
import markdown

class Manager():
    def __init__(self):
        self.env = {
            'add': lambda callback: self.add(callback),
            'hashpass': lambda rawpass: self.hashpass(rawpass)
        }

        self.data_objects = {
            'category': lambda: self.category(),
            'user': lambda: self.user(),
            'article': lambda: self.article()
        }

    def run(self, instruction, data_object, args):
        self.data_args = args
        self.env[instruction](self.data_objects[data_object])
        db.session.commit()

    def hashpass(self, rawpass):
        return hashlib.sha512(rawpass.encode('utf-8')).hexdigest()

    def add(self, callback):
        res = callback()
        print(res)
        db.session.add_all([res])

    def category(self):
        return Category(category=self.data_args[0])

    def user(self):
        return User(username=self.data_args[0], \
            password_hash=self.env['hashpass'](self.data_args[1]), \
            email=self.data_args[2])

    def article(self):
        return Article(title=self.data_args[0], \
            rawcontent=self.data_args[1], \
            content=markdown.markdown(self.data_args[1]), \
            category=Category.get_category(self.data_args[2]), \
            author=User.get_user_by_name(self.data_args[3]))

manager = Manager()

while True:
    tokens = input('> ').split(' ')
    if len(tokens) == 0 or tokens[0] == '':
        continue
    if tokens[0] == 'exit':
        break
    manager.run(tokens[0], tokens[1], tokens[2:])
