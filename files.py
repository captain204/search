from flask import Flask, request, jsonify,redirect,url_for
from flask_pymongo import PyMongo
import json
import os
import re
from bson.json_util import dumps

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['MONGO_DBNAME'] = 'voucher'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/voucher'
#app.config['MONGO_URI'] = 'mongodb+srv://captain204:hQF4xoLiPw5rXQ2c@cluster0-fa1lj.mongodb.net/test?retryWrites=true&w=majority'
#mongodb+srv://captain204:<password>@cluster0-fa1lj.mongodb.net/test?retryWrites=true&w=majority
#mongodb+srv://captain204:<password>@cluster0-fa1lj.mongodb.net/test?retryWrites=true&w=majority
#shell

#mongo "mongodb+srv://cluster0-fa1lj.mongodb.net/test"  --username captain204

mongo = PyMongo(app)

@app.route('/search', methods=['GET'])
def card():
    cards = mongo.db.cards.find()
    response = dumps(cards)
    return response

@app.route('/search/<string>',methods = ['GET'])
def search_by_keyword(string):
    #Full search
    search = mongo.db.cards.find({"$text": { "$search": string } } )
    for item in search:    
        return dumps(item)
    #return ("E no dey work")
    # Partial search
    text ="{}.*".format(string)
    partial = mongo.db.cards.find({
        "$or":[
                {'pin': {"$regex":text,"$options":'i'}},
                {'batch_no': {"$regex":text,"$options":'i'}},
                {'price': {"$regex":text,"$options":'i'}},
                {'date': {"$regex":text,"$options":'i'}},
                {'transactions': {"$regex":text,"$options":'i'}}
             ]
          })
    for result in partial:
        return dumps(result)
    return{'message':'No match found'}


    partial = mongo.db.voucher.find({
        "$or":[
                
                {'date': {"$regex":text,"$options":'i'}},
                {'time': {"$regex":text,"$options":'i'}},
                {'price': {"$regex":text,"$options":'i'}},
                {'state': {"$regex":text,"$options":'i'}},
                {'used': {"$regex":text,"$options":'i'}},
                {'pin': {"$regex":text,"$options":'i'}},
                {'serial_no': {"$regex":text,"$options":'i'}},
                {'activation_status': {"$regex":text,"$options":'i'}},
                {'dealer_id': {"$regex":text,"$options":'i'}},
                {'batch': {"$regex":text,"$options":'i'}}                
                
             ]
          })

mongo = PyMongo(app)

@app.route('/', methods=['GET'])
def card():
    cards = mongo.db.voucher.find()
    response = dumps(cards)
    return response

@app.route('/search/<string>',methods = ['GET'])
def search_by_keyword(string):
    #Partial search
    text ="{}.*".format(string)
    partial=mongo.db.voucher.find({'pin': {"$regex":text,"$options":'i'}})
    for result in partial:
        return dumps(result)
    # Full text search
   
    search = mongo.db.voucher.find({"$text": { "$search": string } } )
    for item in search:    
        return dumps(item)
    #return ("E no dey work")
    return{'message':'No match found'}


    # Search by pin number
    if value[:].isdigit() and int(value[:]) <= 999999999999999:
        search = ["pin1","pin2"]
        for item in search:
            return item
    #Search by username
    if value[:].isalpha():
        #search = mongo.db.user.find({username:value})
        search = ["userone","usertwo"]
        for item in search:
            return item
        #state = mongo.db.user.find({username:value})
        state = ["one","two"]
        for item in state:
            return item 
    #Search by state
    if value[:].isalpha():
        #search = mongo.db.user.find({username:value})
        search = ["userone","usertwo"]
        for item in search:
            return item
    @app.route('/search',methods = ['GET','POST'])
def Post():
    keyword = request.json

    if keyword.isdigit():
        value = int(keyword)
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
 










    
        

if __name__ == "__main__":
  app.run(debug=True)