import argparse

from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

from .similar import important_words

_MAX_LENGTH = 2000

app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()
parser.add_argument('in')


class ParseV1(Resource):
    def post(self):
        args = parser.parse_args()
        ins = args['in']
        if not ins or len(ins) == 0:
            abort(400, message='Missing \'in\' data.')
        if len(ins) > _MAX_LENGTH:
            abort(400, message='Input too large - current maximum is {} characters.'.format(_MAX_LENGTH))
        result = {
            'important_words': important_words(ins)
        }
        return result, 200


def main():
    argparser = argparse.ArgumentParser(
        description='Analyze Icelandic text with icenews')

    argparser.add_argument('-b', '--bind', type=str, default='127.0.0.1', help='Address to bind to')
    argparser.add_argument('-p', '--port', type=int, default=8000, help='Port number to use')
    argparser.add_argument('-d', '--debug', action='store_true', help='Start in debug mode')

    args = argparser.parse_args()

    app.run(host=args.bind, port=args.port, debug=args.debug)


api.add_resource(ParseV1, '/v1/parse')

if __name__ == '__main__':
    main()
