from flask import Flask
from flask_restx import Api, Resource, reqparse
from model_backend import predict_genre  # asegúrate que este nombre coincida

app = Flask(__name__)
api = Api(app, version='1.0', title='API Predicción de Género de Películas')

ns = api.namespace('predict', description='Predicción')

parser = reqparse.RequestParser()
parser.add_argument('year', type=float, required=True)
parser.add_argument('rating', type=float, required=True)
parser.add_argument('title', type=str, required=True)
parser.add_argument('plot', type=str, required=True)

@ns.route('/')
class GenreAPI(Resource):
    @api.expect(parser)
    def get(self):
        args = parser.parse_args()
        try:
            result = predict_genre(**args)
            return {
                "input": args,
                "prediction": result
            }, 200
        except Exception as e:
            return {"message": str(e)}, 400

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
