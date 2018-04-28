from app import db
from app.models import Category, Role
import hashlib

db.drop_all()
db.create_all()

""" create roles """
normal_user = Role(roletitle='normal_user')
admin = Role(roletitle='admin')

""" create category """
# RED
cantonese = Category(category='cantonese', color='#EF5350')
# BLUE
shanghainese = Category(category='shanghainese', color='#42A4F5')
# ORANGE
african_dialect = Category(category='afircan dialect', color='#FF7043')
# AMBER
mars_dialect =  Category(category='mars mars_dialect', color='#FFCA28')
# GREEN
moonglish = Category(category='moonglish', color='#66BB6A')

update_list=[normal_user, admin, cantonese, shanghainese, african_dialect, \
        mars_dialect, moonglish]

db.session.add_all(update_list)
db.session.commit()
