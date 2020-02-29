from flask import Flask, request, jsonify,redirect,url_for
from flask_pymongo import PyMongo
import json
import os
import re
from bson.json_util import dumps

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

#app.config['MONGO_DBNAME'] = 'voucher'
#app.config['MONGO_URI'] = 'mongodb://localhost:27017/voucher'
#Main db
app.config['MONGO_URI'] ='mongodb+srv://donjoe:praise1234@cluster0-of0j7.azure.mongodb.net/voucher?retryWrites=true&w=majority'

#app.config['MONGO_URI'] = 'mongodb+srv://captain204:hQF4xoLiPw5rXQ2c@cluster0-fa1lj.mongodb.net/test?retryWrites=true&w=majority'
#mongodb+srv://captain204:<password>@cluster0-fa1lj.mongodb.net/test?retryWrites=true&w=majority
#mongodb+srv://captain204:<password>@cluster0-fa1lj.mongodb.net/test?retryWrites=true&w=majority
#shell

#mongo "mongodb+srv://cluster0-fa1lj.mongodb.net/test"  --username captain204

mongo = PyMongo(app)

@app.route('/', methods=['GET'])
def card():
    cards = mongo.db.voucher.find()
    response = dumps(cards)
    return response

@app.route('/search/<string>',methods = ['GET'])
def search_by_keyword(string):
    #Partial search
    partial=mongo.db.voucher.find({'pin': {"$regex":text,"$options":'i'}})
    for result in partial:
        return dumps(result)
    return{'message':'No match found'}

    # Full text search
    text ="/{}/".format(string)
    search = mongo.db.voucher.find({"$text": { "$search": string } } )
    for item in search:    
        return dumps(item)
    #return ("E no dey work")
    
        

if __name__ == "__main__":
  app.run(debug=True)