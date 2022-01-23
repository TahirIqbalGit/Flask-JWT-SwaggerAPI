from flask import Flask, Blueprint, jsonify, request
from flask_restx import Api
import bcrypt
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, get_jwt_identity
)
# Expetions for sqlaclemy
from sqlalchemy.exc import IntegrityError

from models.user import UserModel

from resources import user
from resources import product
from main import db, ma

from marshmallow import ValidationError
from routes import site

app = Flask(__name__)
blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(blueprint, doc='/doc', title='Flask API')
app.register_blueprint(blueprint)
app.register_blueprint(site)

app.config['SECRET_KEY'] = "b3s3cr3tk3y"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

api.add_namespace(product.product_ns)
api.add_namespace(product.products_ns)
api.add_namespace(user.user_ns)
api.add_namespace(user.users_ns)

@app.before_first_request
def create_tables():
    db.create_all()
    
@api.errorhandler(ValidationError)
def handle_validation_error(error):
    return jsonify(error.messages), 400

product.product_ns.add_resource(product.Product, '/<int:id>')
product.products_ns.add_resource(product.ProductList, "")
user.user_ns.add_resource(user.User, '/<int:id>')
user.users_ns.add_resource(user.UserList, "")


if __name__ == '__main__':
    db.init_app(app)
    ma.init_app(app)
    app.run(debug=True)