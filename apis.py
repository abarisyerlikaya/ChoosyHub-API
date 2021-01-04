from flask_restful import Resource, request
from flask.json import jsonify
from pymongo import MongoClient
from re import I, compile
from math import ceil


class Products(Resource):
    def __init__(self):
        self.conn = MongoClient(
            "mongodb+srv://admin:choosyhub@cluster0.axzel.mongodb.net/choosyhub?retryWrites=true&w=majority")
        self.db = self.conn["choosyhub"]
        self.collection = self.db["products"]

    def get(self):
        key = request.args.get("key") if request.args.get(
            "key") is not None else ""
        page = int(request.args.get("page")) if request.args.get(
            "page") is not None else 1

        expression = compile(f'.*{key}.*', I)

        query = {"name": {"$regex": expression}}
        returning_fields = {"_id": 1, "name": 1, "price": 1, "rating": 1,
                            "number_of_reviews": 1, "number_of_comments": 1, "pictures": 1}

        if request.args.get("minPrice") is not None and request.args.get("maxPrice") is not None:
            query["price"] = {"$gte": int(request.args.get("minPrice")), "$lte": int(request.args.get("maxPrice"))}
        elif request.args.get("minPrice") is not None:
            query["price"] = {"$gte": int(request.args.get("minPrice"))}
        elif request.args.get("maxPrice") is not None:
            query["price"] = {"$lte": int(request.args.get("maxPrice"))}
        if request.args.get("minRating") is not None:
            query["rating"] = {"$gte": int(request.args.get("minRating"))}
        if request.args.get("minReviewCount") is not None:
            query["number_of_reviews"] = {
                "$gte": int(request.args.get("minReviewCount"))}
        if request.args.get("minCommentCount") is not None:
            query["number_of_comments"] = {
                "$gte": int(request.args.get("minCommentCount"))}

        sort_by = [("number_of_reviews", -1)]

        if request.args.get("sortBy") is not None:
            if request.args.get("sortBy") == "numberOfReviews":
                sort_by = [("number_of_reviews", -1)]
            elif request.args.get("sortBy") == "numberOfComments":
                sort_by = [("number_of_comments", -1)]
            elif request.args.get("sortBy") == "rating":
                sort_by = [("rating", -1)]
            elif request.args.get("sortBy") == "priceAsc":
                sort_by = [("price", 1)]
            elif request.args.get("sortBy") == "priceDsc":
                sort_by = [("price", -1)]

        cursor = self.collection.find(query, returning_fields).sort(sort_by)
        page_count = ceil(cursor.count() / 10)

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
