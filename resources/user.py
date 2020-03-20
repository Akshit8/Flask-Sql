import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel
 
        
class userRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username'
            ,type=str
            ,required=True
            ,help="this field is required")

    parser.add_argument('password'
            ,type=str
            ,required=True
            ,help="this filed is required")

    def post(self):
        
        data = userRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': 'user already registered'}, 400
        
        user = UserModel(data['username'], data['password'])
        user.save_to_db()

        return {'message': 'user was created successfully'} , 201

