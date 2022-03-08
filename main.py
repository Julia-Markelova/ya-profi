from http import HTTPStatus

from flask import Flask
from flask import request
from flask_restx import Api
from flask_restx import Resource
from flask_restx import fields

from app.catalog import Catalog
from app import controllers
from app.model import serialize

flask_app = Flask(__name__)
app = Api(app=flask_app)
catalog = Catalog()


products = app.namespace('products', description='Product operations')
categories = app.namespace('categories', description='Category operations')


product_create = app.model('ProductCreate', {
    'name': fields.String(required=True, description='Product name'),
    'description': fields.String(required=True, description='Product details'),
    'category_id': fields.Integer(required=True, description='Category id')
})

product = app.model('ProductModel', {
    'id': fields.Integer(required=True, description='Product id'),
    'name': fields.String(required=True, description='Product name'),
    'description': fields.String(required=True, description='Product details'),
    'category_id': fields.Integer(required=True, description='Category id')
})


@products.route('/')
class ProductView(Resource):

    @products.expect(product_create)
    @products.doc('Create product')
    @products.response(HTTPStatus.CREATED, 'Success')
    @products.response(HTTPStatus.BAD_REQUEST, 'Validation Error')
    @products.response(HTTPStatus.INTERNAL_SERVER_ERROR, 'Internal server error')
    def post(self):
        try:
            data = request.json
            if 'name' not in data or 'description' not in data or 'category_id' not in data:
                return 'Invalid parameters', HTTPStatus.BAD_REQUEST
            p = controllers.add_product(catalog, data['name'], data['description'], data['category_id'])
            return serialize(p), HTTPStatus.CREATED
        except ValueError:
            return f'No such category', HTTPStatus.BAD_REQUEST
        except Exception as e:
            return f'Unexpected error: {e}', HTTPStatus.INTERNAL_SERVER_ERROR

    @products.doc('Get list of products')
    @products.marshal_list_with(product, code=HTTPStatus.OK)
    def get(self):
        p = controllers.get_products(catalog)
        return p, HTTPStatus.OK


@products.route('/<id>')
class ProductIdView(Resource):

    @products.doc('Get product by id')
    @products.response(HTTPStatus.OK, 'Success')
    @products.response(HTTPStatus.NOT_FOUND, 'No such product')
    @products.response(HTTPStatus.INTERNAL_SERVER_ERROR, 'Internal server error')
    def get(self, id):
        try:
            p = controllers.get_product_by_id(catalog, int(id))
            return serialize(p), HTTPStatus.OK
        except ValueError:
            return 'No such product', HTTPStatus.NOT_FOUND
        except Exception as e:
            return f'Unexpected error: {e}', HTTPStatus.INTERNAL_SERVER_ERROR


if __name__ == '__main__':
    flask_app.run(debug=True)
