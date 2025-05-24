from flask import Flask
from flask_restx import Api, Resource, reqparse
from model_backend import predict_genre



app = Flask(__name__)

api = Api(
    app,
    version='1.0',
    title='Predicción Género de una Película',
    description='API que predice el género de una película con base en algunas características',
    mask=None
)

ns = api.namespace('predict', description='Predicción de género de películas')

parser = reqparse.RequestParser(trim=True)
parser.add_argument('year', type=float, required=True, help='Año de la película (1984 a 2015)', location='args')
parser.add_argument('rating', type=float, required=True, help='rating de la película (1.2 a 9.3)', location='args')
parser.add_argument('title', type=str, required=True, help='Título de la película', location='args')
parser.add_argument('plot', type=str, required=True, help='Trama de la película', location='args')

@ns.route('/')
class GenreApi(Resource):
    @api.expect(parser)
    def get(self):
        args = parser.parse_args()
        try:
            result = predict_genre(**args)
            return {
                "input": args,
                "prediction": {
                    "genre": result["predicted_genre"],
                    "top_5_genres": result["top_5_genres"]
                }
            }, 200
        except ValueError as e:
            return {'message': str(e)}, 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
