from flask import request
from flask_restx import Resource, fields, Namespace
import uuid

from models.user import UserModel
from schemas.user import UserSchema

USER_NOT_FOUND = "User not found."
USER_ALREADY_EXISTS = "User '{}' Already exists."

user_ns = Namespace('user', description='User related operations')
users_ns = Namespace('users', description='Users related operations')

user_schema = UserSchema()
user_list_schema = UserSchema(many=True)

# Model required by flask_restx for expect
user =  user_ns.model('User', {
    # 'public_id': str(uuid.uuid4()),
    'username': fields.String('Name of the User'),
    'email': fields.String('Email of the User'),
    'password': fields.String('Password'),
    'is_admin': False
})

class User(Resource):
    def get(self, id):
        user_data = UserModel.find_by_id(id)
        if user_data:
            return user_schema.dump(user_data)
        return {'message': USER_NOT_FOUND}, 404

    def delete(self, id):
        user_data = UserModel.find_by_id(id)
        if user_data:
            user_data.delete_from_db()
            return {'message': "User Deleted successfully"}, 200
        return {'message': USER_NOT_FOUND}, 404


class UserList(Resource):
    @users_ns.doc('Get all the Users')
    def get(self):
        return user_list_schema.dump(UserModel.find_all()), 200

    @users_ns.expect(user)
    @users_ns.doc('Create a User')
    def post(self):
        user_json = request.get_json()
        print('THIS IS USER_JSON DATA GETTING:', user_json)
        # public_id = str(uuid.uuid4())
        username = user_json['username']
        email = user_json['email']
        password = user_json['password']
        is_admin = False
        # print('THIS IS ALL DETAIL ADDED TO POST', public_id, username, email, password, is_admin)
        
        if UserModel.find_by_email(email):
            return {'message': USER_ALREADY_EXISTS.format(username)}, 400

        user_data = user_schema.load(user_json)
        print('THIS IS USER_DATA TO SAVE ON DB:', user_data)
        user_data.save_to_db()

        return user_schema.dump(user_data), 201