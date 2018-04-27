from app import db
from app.models import User, Article, Category
import hashlib

class Manager():
    def __init__(self):
        self.env = {
            'add': lambda callback: self.add(callback),
            'hashpass': lambda rawpass: self.hashpass(rawpass)
        }

        self.data_objects = {
            'category': lambda: self.category(),
            'user': lambda: self.user()
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

manager = Manager()

while True:
    tokens = input('> ').split(' ')
    if tokens[0] == 'exit':
        break
    manager.run(tokens[0], tokens[1], tokens[2:])
