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

@app.route('/new/<string>',methods = ['GET','POST'])
def Post(string):
    value = str(string)
    result = []
    if value[0].isdigit() and int(value) < 3:
        search = mongo.db.voucher.find({"batch":int(value)})
        #search = ["food","people"]
        for item in search:    
            result.append(item)
        return dumps(result)

    if len(value) == 15 and value.isdigit():
        search = mongo.db.voucher.find({"pin":value})
        #search = ["pin1","pin2"]
        for item in search:    
            result.append(item)
        return dumps(result)


    if  value[:].isdigit():
        search = mongo.db.voucher.find({"serial_no":int(value)})
        for item in search:    
            result.append(item)
        return dumps(result)

        
    if re.search('[a-zA-Z]',value) and len(value) != 8:
        search = mongo.db.users.find({"username":value})
        for item in search:
            result.append(item)
        return dumps(result)

    if len(value) == 8 and re.search('[a-zA-Z]',value):
        search = mongo.db.users.find({"role":value})
        for item in search:
            result.append(item)
        return dumps(result)

    
    search = mongo.db.voucher.find({"$text": { "$search": value } } )
    for item in search:    
        result.append(item)
        return dumps(result)
    return{'message':'No match found'}
 


@app.route('/search',methods = ['POST'])
def newPost():    
    keyword = request.json['keyword']
    if not keyword:
        return {"message":"Please enter a search keyword"},400
    result = []
    #Search by batch
    if keyword and len(keyword)< 3:
        search = mongo.db.voucher.find({"batch":int(keyword)})
        for item in search:
            result.append(item)
        if not result:
            return {"message":"No match found"},400
        return dumps(result)
    #Search by pin
    if len(str(keyword)) == 15:
        search = mongo.db.voucher.find({"pin":str(keyword)})
        for item in search:
            result.append(item)
        if not result:
            return {"message":"No match found"},404
        return dumps(result)

    #Search by serial number
    if keyword.isdigit():
        search = mongo.db.voucher.find({"serial_no":int(keyword)})
        for item in search:
            result.append(item)
        if not result:
            return {"message":"No match found"},404
        return dumps(result)
        
    #Search by username
    if re.search('[a-zA-Z]',keyword) and len(keyword) != 8:
        search = mongo.db.users.find({"username":keyword})
        for item in search:
            result.append(item)
        if not result:
            return {"message":"No match found"},404
        return dumps(result)
        
    if len(keyword) == 8 and re.search('[a-zA-Z]',keyword):
        search = mongo.db.users.find({"role":keyword})
        for item in search:
            result.append(item)
        if not result:
            return {"message":"No match found"},404
        return dumps(result)

    #Full text search
    search = mongo.db.voucher.find({"$text": { "$search":keyword}} )
    for item in search:
        result.append(item)
    if not result:
        return {"message":"No match found"},404
    return dumps(result)


if __name__ == "__main__":
  app.run(debug=True)