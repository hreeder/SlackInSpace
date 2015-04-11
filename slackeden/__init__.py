from flask import Flask
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate

# Init app
app = Flask(__name__)
app.config.from_object('config')

# Load extensions
lm = LoginManager(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

lm.login_view = "welcome"

from slackeden.tasks import make_celery
celery = make_celery(app)

# Fix "MySQL server has gone away" issues
from sqlalchemy import exc
from sqlalchemy import event
from sqlalchemy.pool import Pool

@event.listens_for(Pool, "checkout")
def ping_connection(dbapi_connection, connection_record, connection_proxy):
    cursor = dbapi_connection.cursor()
    try:
        cursor.execute("SELECT 1")
    except:
        # optional - dispose the whole pool
        # instead of invalidating one at a time
        # connection_proxy._pool.dispose()

        # raise DisconnectionError - pool will try
        # connecting again up to three times before raising.
        print "raise error"
        raise exc.DisconnectionError()
    cursor.close()

# Import SlackEden
from slackeden import views

from slackeden.tasks.eve import update_character_info, update_corp_info, update_alliances