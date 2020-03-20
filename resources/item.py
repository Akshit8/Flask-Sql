from flask import request
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):

    parser = reqparse.RequestParser() #this parser now belongs to the class item and can be used as used in put method
    parser.add_argument('price',
            type=float,
            required=True,
            help='This field can\'t be empty'
        )
    
    parser.add_argument('store_id',
            type=int,
            required=True,
            help='This field can\'t be empty'
        )

    @jwt_required()
    def get(self,name):
        
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        
        return {'message':'Item not found'} , 404

    # optimizing techniques 
    # for post method first check whether the item already exists
    # if not then extarct json payload and add it to the items

    def post(self,name):

        if ItemModel.find_by_name(name):
            return {'message':'An item with name {} already exists!'.format(name)}, 400

        data = Item.parser.parse_args()     # force = true means no need of headers, silent = true means would return null in case of no json
        item = ItemModel(name, data['price'], data['store_id'])
        
        try:
            item.save_to_db()
        except:
            return {'message' : 'couldn\'t add item to database'} , 500   #internal server error

        return item.json(), 201

    def delete(self, name):
        
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message':'Item Deleted'}, 200

    def put(self, name):
        # parser = reqparse.RequestParser()
        # parser.add_argument('price',
        #     type=float,
        #     required=True,
        #     help='This field can\'t be empty'
        # )

        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, data['price'],data['store_id'])
        else:
            item.price = data['price']

        item.save_to_db()
        return item.json(), 200

    

class ItemList(Resource):
    def get(self):
        return {'item': [item.json() for item in ItemModel.query.all()]}