from app import db
from app.models import Category, Role
import hashlib

db.drop_all()
db.create_all()

update_list = []
def update(entry):
    update_list.append(entry)

""" create roles """
update(Role(roletitle='normal_user'))
update(Role(roletitle='admin'))

""" create category """
# RED
update(Category(category='cantonese', color='#EF5350'))
# BLUE
update(Category(category='shanghainese', color='#42A4F5'))
# ORANGE
update(Category(category='afircan dialect', color='#FF7043'))
# AMBER
update(Category(category='mars mars_dialect', color='#FFCA28'))
# GREEN
update(Category(category='moonglish', color='#66BB6A'))


""" commit change"""
db.session.add_all(update_list)
db.session.commit()
