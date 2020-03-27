from flask import Flask,jsonify,request,jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import datetime
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_jwt_extended import (create_access_token)

app = Flask(__name__)

app.config['MONGO_DBNAME']='MeDiary'
app.config['MONGO_URI']='mongodb://localhost:27017/MeDiary'
app.config['JWT_SECRET_KEY']='secret'

mongo=PyMongo(app)
bcrypt=Bcrypt(app)
jwt=JWTManager(app)

CORS(app)

@app.route('/users/register',methods=['POST'])
def register():
    users=mongo.db.users
    first_name=request.get_json()['first_name']
    last_name=request.get_json()['last_name']
    email=request.get_json()['email']
    password=bcrypt.generate_password_hash(request.get_json()['password']).decode('utf-8')
    created=datetime.utcnow()

    user_id=users.insert({
        'first_name':first_name,
        'last_name':last_name,
        'email':email,
        'password':password,
        'created':created

    })
    new_user=users.find_one({'_id':user_id})
    result ={'email':new_user['email']+'registered'}
    return jsonify({'result':result})

@app.route('/users/login',methods=['POST'])
def login():
    users=mongo.db.users
    email=request.get_json()['email']
    password=request.get_json()['password']
    result=""
    response = users.find_one({'email':email})
    if response:
        if(bcrypt.check_password_hash(response['password'],password)):
            access_token = create_access_token(identity={
                'first_name':response['first_name'],
                'last_name':response['last_name'],
                'email':response['email']
            })
            result=jsonify({"token":access_token})
        else:
            result=jsonify({"error":"invalid email or password"})
    else:
        result=jsonify({"result":"No records found"})
    return result

@app.route('/users/add',methods=['POST'])
def add():
    diary=mongo.db.diary
    email=request.get_json()['email']
    details=request.get_json()['details']
    result=""
    created=datetime.utcnow()
    data=diary.insert({
        'email':email,
        'details':details,
        'created':created
    })
    data_find=diary.find_one({'_id':data})
    result ={'email':data_find['email'],'details':data_find['details']+','+'registered'}
    return jsonify({'result':result})

@app.route('/users/getit',methods=['POST'])
def getit():
    diary=mongo.db.diary
    email=request.get_json()['email']
    result=[]
    cur=diary.find({'email':email})
    len=cur.count()
    details=[]
    for i in range(0,len):
        noteDate=cur[i]['created']
        noteDetails=cur[i]['details']
        noteDate=noteDate.strftime("%d-%b-%Y x (%H:%M:%S)")
        noteData=noteDate[0]
        details.append(noteDate+" x "+noteDetails)
    result={'details':details}

#    result={'date':response['created'],'notes':response['details']}
    return jsonify({'result':result})

if __name__== '__main__':
    app.run(debug=True)