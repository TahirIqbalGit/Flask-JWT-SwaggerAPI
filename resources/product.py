from flask import request
from flask_restx import Resource, fields, Namespace

from models.product import ProductModel
from schemas.product import ProductSchema

ITEM_NOT_FOUND = "Item not found."

product_ns = Namespace('product', description='Product related operations')
products_ns = Namespace('products', description='Products related operations')

product_schema = ProductSchema()
product_list_schema = ProductSchema(many=True)

# Model required by flask_restx for expect
product = product_ns.model('Product', {
    'name': fields.String('Name of the Product'),
    'price': fields.Float(0.00),
    'category': fields.String('Enter category: Electronics OR Wearhouse'),
    'user_id': fields.Integer
})


class Product(Resource):
    
    def get(self, id):
        product_data = ProductModel.find_by_id(id)
        if product_data:
            return product_schema.dump(product_data)
        return {'message': ITEM_NOT_FOUND}, 404

    def delete(self,id):
        product_data = ProductModel.find_by_id(id)
        if product_data:
            product_data.delete_from_db()
            return {'message': "Product Deleted successfully"}, 200
        return {'message': ITEM_NOT_FOUND}, 404

    @product_ns.expect(product)
    def put(self, id):
        product_data = ProductModel.find_by_id(id)
        product_json = request.get_json();

        if product_data:
            product_data.price = product_json['price']
            product_data.name = product_json['name']
            product_data.category = product_json['category']
        else:
            product_data = product_schema.load(product_json)

        product_data.save_to_db()
        return product_schema.dump(product_data), 200
    
class ProductList(Resource):
    @products_ns.doc('Get all the Products')
    def get(self):
        return product_list_schema.dump(ProductModel.find_all()), 200

    @products_ns.expect(product)
    @products_ns.doc('Create a Product')
    def post(self):
        product_json = request.get_json()
        product_data = product_schema.load(product_json)
        product_data.save_to_db()

        return product_schema.dump(product_data), 201
