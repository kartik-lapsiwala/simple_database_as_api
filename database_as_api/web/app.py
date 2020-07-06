from flask import Flask, jsonify, request
from  flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.SentencesDatabase
users = db["Users"]

class Register(Resource):
    def post(self):
        # Get posted data by the user
        postedData = request.get_json()
        username = postedData["username"]
        password = postedData["password"]

        # Hash the password and add salt
        hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
        users.insert({
            "username": username,
            "password": hashed_pw,
            "sentence": "",
            "tokens": 10
        })

        retJson = {
            "status": 200,
            "message": "Signed up was successful"
        }
        return jsonify(retJson)

# create a helper function to verify username and password
def verify_pw(username, password):
    hashed_pw = users.find({"username": username})[0]["password"]
    if bcrypt.hashpw(password.encode("utf8"), hashed_pw) == hashed_pw:
        return True
    else:
        return False

# create a function to count number of tokens
def count_tokens(username):
    num_of_tokens = users.find({"username": username})[0]["tokens"]
    return num_of_tokens


class Store(Resource):
    def post(self):
        postedData = request.get_json()
        username = postedData["username"]
        password = postedData["password"]
        sentence = postedData["sentence"]

        # use a helper function to verify username and password
        correct_pw = verify_pw(username, password)
        if not correct_pw:
            retJson = {
                "status": 302,
                "message": "username or password incorrect"
            }
            return jsonify(retJson)

        # using "count_tokens" helper function, check if a user has more than 0 tokens
        num_tokens = count_tokens(username)
        if num_tokens <= 0:
            retJson = {
                "status": 301,
                "message": "not enough tokens"
            }
            return jsonify(retJson)

        # store the sentence and take one token from the user
        users.update({
        "username":username},
        {
            "$set":{
                "sentence": sentence,
                "tokens": num_tokens - 1
                }
        })

        retJson = {
            "status": 200,
            "message": "sentence saved",
            "remaining tokens": users.find({"username": username})[0]["tokens"]
        }
        return jsonify(retJson)

class Retrieve(Resource):
    def post(self):
        postedData = request.get_json()
        username = postedData["username"]
        password = postedData["password"]

        # use a helper function to verify username and password
        correct_pw = verify_pw(username, password)
        if not correct_pw:
            retJson = {
                "status": 302,
                "message": "username or password incorrect"
            }
            return jsonify(retJson)

        # using "count_tokens" helper function, check if a user has more than 0 tokens
        num_tokens = count_tokens(username)
        if num_tokens <= 0:
            retJson = {
                "status": 301,
                "message": "not enough tokens"
            }
            return jsonify(retJson)

        users.update({
        "username":username},
        {
            "$set":{
                "tokens": num_tokens - 1
                }
        })

        retJson = {
            "status": 200,
            "sentence": users.find({"username": username})[0]["sentence"],
            "remaining tokens": users.find({"username": username})[0]["tokens"]
        }
        return jsonify(retJson)


api.add_resource(Register, "/register")
api.add_resource(Store, "/store")
api.add_resource(Retrieve, "/get")

if __name__ == '__main__':
    app.run(host = '0.0.0.0')



"""
from flask import Flask, jsonify, request
from  flask_restful import Api, Resource
from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.aNewDB
UserNum = db["UserNum"]

UserNum.insert({
    "num_of_users":0
})

class Visit(Resource):
    def get(self):
        prev_num = UserNum.find({})[0]["num_of_users"]
        new_num = prev_num + 1
        UserNum.update({}, {"$set":{"num_of_users":new_num}})
        return str("Hey user: " + str(new_num))

def checkPostedData(jsondata, functionName):
    if functionName == "add" or functionName == "subtract" or functionName == "multiply":
        if "x" not in jsondata or "y" not in jsondata:
            return 301
        else:
            return 200

    if functionName == "divide":
        if "x" not in jsondata or "y" not in jsondata:
            return 301
        elif jsondata["y"] == 0:
            return 302
        else:
            return 200


class Add(Resource):
    def post(self):
        data = request.get_json()
        status_code = checkPostedData(data, "add")
        if status_code != 200:
            retJson = {
            "message": "Empty value",
            "status code": status_code
            }
            return jsonify(retJson)
        x = data["x"]
        y = data["y"]
        x = int(x)
        y = int(y)
        sum = x+y
        sumJson = {
        "message": sum,
        "status code": 200
        }
        return jsonify(sumJson)

class subtract(Resource):
    def post(self):
        data = request.get_json()
        status_code = checkPostedData(data, "subtract")
        if status_code != 200:
            retJson = {
            "message": "Empty value of x or y",
            "status code": status_code
            }
            return jsonify(retJson)
        x = data["x"]
        y = data["y"]
        subtraction = x - y
        retJson = {
        "message": subtraction,
        "status code": status_code
        }
        return jsonify(retJson)

class multiply(Resource):
    def post(self):
        data = request.get_json()
        status_code = checkPostedData(data, "multiply")
        if status_code != 200:
            retJson = {
            "message": "Value of x or y is missing",
            "status code": status_code
            }
            return jsonify(retJson)
        x = data["x"]
        y = data["y"]
        multiplication = x * y
        retJson = {
        "message": multiplication,
        "status code": status_code
        }
        return jsonify(retJson)



class divide(Resource):
    def post(self):
        data = request.get_json()
        status_code = checkPostedData(data, "divide")
        if status_code == 301:
            retJson = {
            "message": "either values of x or y is missing",
            "status code": status_code
            }
            return jsonify(retJson)
        elif status_code == 302:
            retJson = {
            "message": "value of y can not be 0",
            "status code": status_code
            }
            return jsonify(retJson)
        x = data["x"]
        y = data["y"]
        division = x/y
        retJson = {
        "message":  division,
        "status code": status_code
        }
        return jsonify(retJson)


api.add_resource(Add, "/add")
api.add_resource(subtract, "/subtract")
api.add_resource(multiply, "/multiply")
api.add_resource(divide, "/divide")
api.add_resource(Visit, "/hello")

@app.route('/')
def basic():
    return 'Hello World!'

if __name__ == '__main__':
    app.run(host = '0.0.0.0')


# export FLASK_ENV=development
# sudo fuser -k 5000/tcp
"""
