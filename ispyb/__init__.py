from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine.url import URL

db = SQLAlchemy()
Base = db.Model

# Use config module if provided:
# db_config = {
#   'user' : 'dbuser',
#   'password' : 'dbpassword',
#   'host' : 'localhost',
#   'port' : '3306',
#   'name' : 'test_db',
# }
try:
    from config import db_config

    db_url = URL(drivername='mysql+pymysql',
                 username=db_config.get('user'),
                 password=db_config.get('password'),
                 host=db_config.get('host'),
                 port=db_config.get('port'),
                 database=db_config.get('name'))
except ImportError:
    db_url = 'mysql+pymysql://ispyb:integration@192.168.33.11:3306/ispyb'


def init_app(app):
    """
    Initialise the database connection and flask-sqlalchemy
    """
    print("Using database connection URL: {}".format(db_url))

    app.config['SQLALCHEMY_DATABASE_URI'] = db_url

    db.init_app(app)
