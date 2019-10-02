from flask import Flask
from flask import request
import json
from flask_cors import CORS
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from bson.json_util import dumps
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/circle"
mongo = PyMongo(app)
CORS(app)


@app.route('/users',methods=['GET'])
def get_users():
    return dumps(mongo.db.users.find({}))

@app.route('/blogs',methods=['GET'])
def get_blogs():
    return dumps(mongo.db.blogs.find({}))


@app.route('/create',methods=['POST'])
def create_users():
    users=[]
    Add={}
    doc_count=mongo.db.users.count_documents({})
    count=0
    if doc_count > 0:
        count=doc_count
    else:
        count=0
    for x in range(0,100):
        count=count+1
        Add["_id"]=ObjectId()
        Add["name"]=request.json["name"]+str(count)
        Add["phone"]=request.json["phone"]+str(count)
        mongo.db.users.insert(Add)
        # users.append(Add)
    print(users)
    return dumps("users created")

@app.route('/createblogs',methods=['POST'])
def create_blogs():
    blogs={}
    doc_count=mongo.db.blogs.count_documents({})
    count=0
    if doc_count > 0:
        count=doc_count
    else:
        count=0
    for x in range(0,100):
        count=count+1
        blogs["_id"]=ObjectId()
        blogs["heading"]=request.json["heading"]+str(count)
        blogs["text"]=request.json["text"]+str(count)
        mongo.db.blogs.insert(blogs)
    return dumps("blogs created")

@app.route('/comtblogs/<ObjectId:userid>/<ObjectId:blogid>',methods=['POST'])
def comment(userid,blogid):
    comment={}
    comment["_id"]=userid
    comment["comment"]=request.json["comment"]
    mongo.db.users.update({"_id":userid},{"$push":{"blog_id":blogid,"comment":comment}})
    return ("user commented")

@app.route('/users/<ObjectId:userid>/level/<int:levelNo>',methods=['GET'])
def level_freinds(userid,levelNo):
    blogs=mongo.db.users.find_one({"_id":userid},{"blog_id":{"$exists":True}})
    print(blogs)
    return dumps(blogs)
    



