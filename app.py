from flask import Flask
from flask import jsonify
from flask import request,redirect
from flask_pymongo import PyMongo
import json
from bson import json_util

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'voucher'
#app.config['MONGO_URI'] = 'mongodb://localhost:27017/voucher'
app.config['MONGO_URI'] = 'mongodb+srv://captain204:<password>@cluster0-fa1lj.mongodb.net/test?retryWrites=true&w=majority'
#mongodb+srv://captain204:<password>@cluster0-fa1lj.mongodb.net/test?retryWrites=true&w=majority
#mongodb+srv://captain204:<password>@cluster0-fa1lj.mongodb.net/test?retryWrites=true&w=majority
#shell
#mongo "mongodb+srv://cluster0-fa1lj.mongodb.net/test"  --username captain204

mongo = PyMongo(app)

@app.route('/', methods=['GET'])
def search():
    card = mongo.db.cards
    result = []
    for output in card.find():
        result.append({'pin':output['pin'],
                       'batch_no':output['batch_no'],
                       'price':output['price'],
                       'date':output['date'],
                    })
    return jsonify({'results':result})



@app.route('/search/<string>', methods = ['GET'])
def search_by_keyword(string):
    search_by_keyword = mongo.db.cards
    q = search_by_keyword.find( { "$text": { "$search": string } } )
    #q = search_by_keyword.find({'batch_no':price})
    output = []
    if q is None:
        return redirect('/search')
    else:
        for result in q:
            obj = json.dumps(result, default=json_util.default)
            output.append(obj)

    """                         
    if output is None:                   
        card = mongo.db.cards
        for cards in card.find():
                obj = json.dumps(cards, default=json_util.default)
                output.append(obj)    
    """
    return jsonify({'results' : output})    
    


