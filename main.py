from http import HTTPStatus

from flask import Flask
from flask import request
from flask_restx import Api
from flask_restx import Resource
from flask_restx import fields

from app.data_reader import DataReader
from app.model import serialize
from app.user_manager import UserManager

flask_app = Flask(__name__)
app = Api(app=flask_app)
user_manager = UserManager()
data_reader = DataReader()


login = app.namespace('login', description='Login')
files = app.namespace('files', description='File operations')
db = app.namespace('db', description='Database operations')
data = app.namespace('data', description='Data operations')


file_source = app.model('FileSource', {
    'type': fields.String(required=True, description='The file type', enum=['csv', 'xls']),
    'path': fields.String(required=True, description='Path'),
    'offset': fields.Integer(required=True, description='Number of rows to offset'),
    'delimiter': fields.String(required=False, description='Delimiter')
})

db_source = app.model('DbSource', {
    'connection_url': fields.String(required=True, description='Database URL'),
    'table': fields.String(required=True, description='Table'),
    'query': fields.String(required=False, description='Query')
})

user = app.model('UserCred', {
    'login': fields.String(required=True, description='login'),
    'password': fields.String(required=True, description='password'),
})


@login.route('/')
class LoginView(Resource):

    @login.expect(user)
    @login.doc('Login')
    @login.response(HTTPStatus.OK, 'Success')
    @login.response(HTTPStatus.UNAUTHORIZED, 'Wrong credentials')
    @login.response(HTTPStatus.BAD_REQUEST, 'Validation Error')
    @login.response(HTTPStatus.INTERNAL_SERVER_ERROR, 'Internal server error')
    def post(self):
        try:
            data = request.json
            if 'login' not in data or 'password' not in data:
                return 'Invalid parameters', HTTPStatus.BAD_REQUEST
            u = user_manager.authorize(data['login'], data['password'])
            return serialize(u), HTTPStatus.OK
        except ValueError:
            return f'Wrong creds', HTTPStatus.UNAUTHORIZED
        except Exception as e:
            return f'Unexpected error: {e}', HTTPStatus.INTERNAL_SERVER_ERROR


@files.route('/<user_id>/read')
class Files(Resource):

    @files.expect(file_source)
    @files.doc('Read data from file source')
    @files.response(HTTPStatus.OK, 'Success')
    @files.response(HTTPStatus.INTERNAL_SERVER_ERROR, 'Internal server error')
    def post(self, user_id):
        try:
            data = request.json
            df = data_reader.read_from_file(data['path'], data['offset'], data['delimiter'])
            user_manager.add_data(user_id, df)
            return 'Data read', HTTPStatus.OK
        except ValueError:
            return 'No such user', HTTPStatus.NOT_FOUND
        except Exception as e:
            return f'Unexpected error: {e}', HTTPStatus.INTERNAL_SERVER_ERROR


@db.route('/<user_id>/read')
class Db(Resource):

    @db.expect(db_source)
    @db.doc('Read data from db source')
    @db.response(HTTPStatus.OK, 'Success')
    @db.response(HTTPStatus.INTERNAL_SERVER_ERROR, 'Internal server error')
    def post(self, user_id):
        try:
            data = request.json
            df = data_reader.read_from_database(data['connection_url'], data['table'], data['query'])
            user_manager.add_data(user_id, df)
            return 'Data read', HTTPStatus.OK
        except ValueError:
            return 'No such user', HTTPStatus.NOT_FOUND
        except Exception as e:
            return f'Unexpected error: {e}', HTTPStatus.INTERNAL_SERVER_ERROR


if __name__ == '__main__':
    flask_app.run(debug=True)
