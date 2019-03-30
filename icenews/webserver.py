from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

from icenews.nlp import parse_ins

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
        return parse_ins(ins), 200


def main():
    api.add_resource(ParseV1, '/v1/parse')
    app.run(debug=True)


if __name__ == '__main__':
    main()
