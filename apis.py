from flask_restful import Resource, request
from flask.json import jsonify
from pymongo import MongoClient
from re import I, compile


class Products(Resource):
    def __init__(self):
        self.conn = MongoClient(
            "mongodb+srv://admin:choosyhub@cluster0.axzel.mongodb.net/choosyhub?retryWrites=true&w=majority")
        self.db = self.conn["choosyhub"]
        self.collection = self.db["products"]

    def get(self):
        name = request.args["name"]
        page = int(request.args["page"])

        expression = compile(f'.*{name}.*', I)

        cursor = self.collection.find({"name": {"$regex": expression}}, {
                                      "_id": 1, "name": 1, "price": 1, "rating": 1, "number_of_reviews": 1, "number_of_comments": 1, "pictures": 1})
        page_count = cursor.count() // 10 + 1

        response = {"meta": {"currentPage": page, "pageCount": page_count},
                    "body": [doc for doc in cursor.skip((page-1)*10).limit(10)]}

        return response


class Product(Resource):
    def __init__(self):
        self.conn = MongoClient(
            "mongodb+srv://admin:choosyhub@cluster0.axzel.mongodb.net/choosyhub?retryWrites=true&w=majority")
        self.db = self.conn["choosyhub"]
        self.collection = self.db["products"]

    def get(self):
        id = request.args["id"]
        response = self.collection.find_one({"_id": id})
        return response
