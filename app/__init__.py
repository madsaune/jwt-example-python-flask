from flask import Flask, request, jsonify
from pymongo import MongoClient
import bcrypt
import jwt
import datetime

app = Flask(__name__)
client = MongoClient('localhost', port=27017)
db = client.test

@app.route('/api/auth/login', methods=['POST'])
def login():
    r = request.get_json()
    
    user = db.users.find_one({ "username": r["username"] })
    if user is None:
        return jsonify({
            "auth": False,
            "message": "Username or password is incorrect."
        }), 401
    
    if not bcrypt.checkpw(r["password"].encode('utf-8'), user['password'].encode('utf-8')):
        return jsonify({
            "auth": False,
            "message": "Username or password is incorrect."
        }), 401
    else:
        payload = {
            'username': user['username'],
            'email': user['email'],
            'name': user['name'],
            'roles': user['roles'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=12)
        }

        token = jwt.encode(payload, 'helloyellow').decode('utf-8')
        print(token)

        return jsonify({
            "auth": True,
            "token": token,
            "message": "Username or password was correct."
        }), 200
