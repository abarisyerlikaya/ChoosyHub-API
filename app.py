from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from apis import Products, Product


app = Flask(__name__)

app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app, resources={r"/": {"origins": "*"}})


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


api = Api(app)

api.add_resource(Products, "/products")
api.add_resource(Product, "/product")

if __name__ == "__main__":
    app.run(debug=True)
