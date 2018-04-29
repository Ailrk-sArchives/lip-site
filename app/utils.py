import logging
from .models import User, Role

"""
logger, SeesionManager
"""

logging.basicConfig(filename='log.log', level=logging.DEBUG)
logger = logging.getLogger('root-logger')

class SessionManager():
    
    @staticmethod
    def login_on(session, username):
        try:
            user = User.get_user_by_name(username=username)
            session['logined'] = True
            session['username'] = username
            session['roletitle'] = user.role.roletitle
        except TypeError:
            logger.error('Session Error: unable to change login status')        

    @staticmethod
    def login_off(session):
        try:
            session['logined'] = False
            session['user'] = None
            session['roletitle'] = None
        except TypeError:
            logger.error('Session Error: unable to change login status')        
