import logging

"""
logger, SeesionManager
"""

logging.basicConfig(filename='log.log', level=logging.DEBUG)
logger = logging.getLogger('root-logger')

class SessionManager():
    
    @staticmethod
    def login_on(session, username):
        try:
            session['logined'] = True
            session['username'] = username
        except TypeError:
            logger.error('Session Error: unable to change login status')        

    @staticmethod
    def login_off(session):
        try:
            session['logined'] = False
            session['username'] = None
        except TypeError:
            logger.error('Session Error: unable to change login status')        
