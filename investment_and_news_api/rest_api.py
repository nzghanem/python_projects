from flask import Flask, request
from flask_restful import Resource, Api, abort
from flask_pymongo import PyMongo
import json
from bson import json_util
import datetime


app = Flask(__name__)
api = Api(app)


app.config["MONGO_URI"] = "mongodb://localhost:27017/rest_api"
mongodb_client = PyMongo(app)
db = mongodb_client.db


class GetCoins(Resource):  # works as expected
    def get(self):  # tested
        try:
            data = json.loads(json_util.dumps(
                db.listcoins.find_one()))
            del data["_id"]
            return data, 200
        except:
            abort(404, message="Requested data is not available.")

    def post(self):  # tested
        try:
            args = request.get_json(force=True)
            db.listcoins.insert_one(args)
            return {"Message": "Recored, created successfully in database!"}, 201
        except:
            abort(409, message="Error occured operation failed.")

    def delete(self):  # tested
        db.listcoins.delete_many({})
        return {"Message": "Document, deleted successfully from database!"}, 200


class MarketShare(Resource):  # works as expected
    def get(self):  # tested
        try:
            data = json.loads(json_util.dumps(
                db.marketshare.find_one({"date_": str(datetime.date.today())})))
            del data["_id"]
            return data, 200
        except:
            abort(404, message="Requested data is not available.")

    def post(self):  # tested
        try:
            args = request.get_json(force=True)
            db.marketshare.insert_one(args)
            return {"Message": "Recored, created successfully in database!"}, 201
        except:
            abort(409, message="Error occured operation failed.")

    def put(self):  # tested
        data = json.loads(json_util.dumps(
            db.marketshare.find_one({"date_": str(datetime.date.today())})))
        try:
            if data["date_"] == str(datetime.date.today()):
                args = request.get_json(force=True)
                db.marketshare.replace_one(
                    {"date_": str(datetime.date.today())}, args)
        except:
            abort(404, message="Nothing was found in database!")

    def delete(self):  # tested
        db.marketshare.delete_one({"date_": str(datetime.date.today())})
        return {"Message": "Document, deleted successfully from database!"}, 200


class HistoricalData(Resource):  # works as expected
    def get(self, coin, currency, _date):  # tested
        try:
            data = json.loads(json_util.dumps(
                db.historicaldata.find_one({"Coin": coin, "Currency": currency,
                                            "Date": _date})))
            del data["_id"]
            return data, 200
        except:
            abort(404, message="Requested data is not available.")

    def post(self, coin, currency, _date):  # tested
        try:
            args = request.get_json(force=True)
            structure = {"Coin": coin, "Currency": currency,
                         "Date": _date, "Data": args}
            db.historicaldata.insert_one(structure)
            return {"Message": "Recored, created successfully in database!"}, 201
        except:
            abort(409, message="Error occured operation failed.")

    def put(self, coin, currency, _date):  # tested
        data = json.loads(json_util.dumps(
            db.historicaldata.find_one({"Coin": coin, "Currency": currency,
                                        "Date": _date})))
        try:
            if data["Date"] == _date:
                args = request.get_json(force=True)
                structure = {"Coin": coin, "Currency": currency,
                             "Date": _date, "Data": args}
                db.historicaldata.replace_one(
                    {"Coin": coin, "Currency": currency,
                     "Date": _date}, structure)
                return {"Message": "Document, updated successfully in database!"}, 200
        except:
            abort(404, message="Nothing was found in database!")

    def delete(self, coin, currency, _date):  # tested
        db.historicaldata.delete_one({"Coin": coin, "Currency": currency,
                                      "Date": _date})
        return {"Message": "Document, deleted successfully from database!"}, 200


class CurrentPrice(Resource):  # works as expected
    def get(self, coin, currency):  # tested
        try:
            data = json.loads(json_util.dumps(
                db.currentprice.find_one({"Coin": coin, "Currency": currency})))
            del data["_id"]
            return data, 200
        except:
            abort(404, message="Requested data is not available.")

    # {"current_price": get_current_price_for_coin("bitcoin", "usd")}
    def post(self, coin, currency):  # tested
        try:
            args = request.form.get("price")
            structure = {"Coin": coin,
                         "Currency": currency, "CurrentPrice": args}
            db.currentprice.insert_one(structure)
            return {"Message": "Recored, created successfully in database!"}, 201
        except:
            abort(409, message="Error occured operation failed.")

    def put(self, coin, currency):  # tested
        data = json.loads(json_util.dumps(
            db.currentprice.find_one({"Coin": coin, "Currency": currency})))
        try:
            if data["Coin"] == coin:
                args = request.form.get("price")
                structure = {"Coin": coin,
                             "Currency": currency, "CurrentPrice": args}
                db.currentprice.replace_one(
                    {"Coin": coin, "Currency": currency}, structure)
                return {"Message": "Document, updated successfully in database!"}, 200
        except:
            abort(404, message="Nothing was found in database!")

    def delete(self, coin, currency):  # tested
        db.currentprice.delete_one({"Coin": coin, "Currency": currency})
        return {"Message": "Document, deleted successfully from database!"}, 200


class GetNews(Resource):  # works as expected
    def get(self, coin):  # tested
        try:
            data = json.loads(json_util.dumps(
                db.news.find_one({"name": coin})))
            del data["_id"]
            return data, 200
        except:
            abort(404, message="Requested data is not available.")

    def post(self, coin):  # tested
        try:
            args = request.get_json(force=True)
            structure = {"name": coin, coin: args}
            db.news.insert_one(structure)
            return {"Message": "Recored, created successfully in database!"}, 201
        except:
            abort(409, message="Error occured operation failed.")

    def put(self, coin):  # tested
        try:
            data = json.loads(json_util.dumps(
                db.news.find_one({"name": coin})))
            if data["name"] == coin:
                args = request.get_json(force=True)
                structure = {"name": coin, coin: args}
                db.news.replace_one(
                    {"name": coin}, structure)
                return {"Message": "Document, updated successfully in database!"}, 200
        except:
            abort(404, message="Nothing was found in database!")

    def delete(self, coin):  # tested
        db.news.delete_one({"name": coin})
        return {"Message": "Document, deleted successfully from database!"}, 200


api.add_resource(GetCoins, "/list-coins")
api.add_resource(MarketShare, "/market-share")
api.add_resource(
    HistoricalData, "/historical-data/<string:coin>/<string:currency>/<string:_date>")
api.add_resource(
    CurrentPrice, "/current-price/<string:coin>/<string:currency>")
api.add_resource(
    GetNews, "/news/<string:coin>")

if __name__ == "__main__":
    app.run()
