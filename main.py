from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

ma = Marshmallow()
db = SQLAlchemy()

db_user, db_password, database = "pythonic", "coder123", "flask_api"