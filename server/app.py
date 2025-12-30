from flask import Flask, request, session, jsonify
from flask_migrate import Migrate
from flask_restful import Resource, Api
from config import db, bcrypt
from models import User
import os

app = Flask(__name__)

app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

db.init_app(app)
bcrypt.init_app(app)
migrate = Migrate(app, db)
api = Api(app)

@app.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No data'}), 400
        
        username = data.get('username')
        password = data.get('password')
        password_confirmation = data.get('password_confirmation')

        if not username or not password:
            return jsonify({'error': 'Username and password required'}), 400
        
        if password != password_confirmation:
            return jsonify({'error': 'Passwords do not match'}), 400
        
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return jsonify({'error': 'Username already exists'}), 422
        


        new_user = User(username=username)
        new_user.password_hash = password
        db.session.add(new_user)
        db.session.commit()

        session['user_id'] = new_user.id

        return jsonify({
            'id': new_user.id,
            'username': new_user.username  
        }), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'error': 'Username and password required'}), 400
        
        user = User.query.filter_by(username=username).first()

        if not user or not user.authenticate(password):
            return jsonify({'error': 'Invalid username or password'}), 401
        
        session['user_id'] = user.id

        return jsonify({
            'id': user.id,
            'username': user.username
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
@app.route('/check_session', methods=['GET'])
def check_session():
    user_id = session.get('user_id')

    if user_id:
        user = User.query.get(user_id)
        if user:
            return jsonify({
                'id': user.id,
                'username': user.username
            }), 200
        
    return jsonify({}), 200

@app.route('/logout', methods=['DELETE'])
def logout():
    session.pop('user_id', None)
    return jsonify({}), 204


if __name__ == '__main__':
    app.run(port=5555, debug=True)