from flask import Flask
from config import config
from .site.routes import site
from .authentification.routes import auth
from .api.routes import api
from .models import db as root_db, login_manager,ma
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

from marvel_inventory.helpers import JSONEncoder

app = Flask(__name__)

app.register_blueprint(site)
app.register_blueprint(auth)
app.register_blueprint(api)
app.config.from_object(config)

root_db.init_app(app)
migrate = Migrate(app,root_db)
login_manager.init_app(app)
login_manager.login_view='signin'

ma.init_app(app)
app.json_encoder = JSONEncoder

CORS(app)

from marvel_inventory import models