from flask import Flask, request, session, jsonify
from flask_migrate import Migrate
from flask_restful import Resource, Api
from config import db, bcrypt
from models import User, Recipe
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI') or 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
bcrypt.init_app(app)
migrate = Migrate(app, db)
api = Api(app)


@app.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
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
        
        return jsonify(new_user.to_dict()), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        db.session.rollback()
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
        
        return jsonify(user.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/check_session', methods=['GET'])
def check_session():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        if user:
            return jsonify(user.to_dict()), 200
    return jsonify({}), 401


@app.route('/logout', methods=['DELETE'])
def logout():
    if 'user_id' not in session:
        return jsonify({'error': 'No active session'}), 401
    session.pop('user_id', None)
    return jsonify({}), 204


class RecipeList(Resource):
    def get(self):
        if 'user_id' not in session:
            return {'error': 'Unauthorized'}, 401

        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        if per_page > 100:
            per_page = 100
        
        pagination = Recipe.query.filter_by(user_id=session['user_id']).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        recipes = [recipe.to_dict() for recipe in pagination.items]
        
        return {
            'recipes': recipes,
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': pagination.page,
            'per_page': per_page
        }, 200
    
    def post(self):
        if 'user_id' not in session:
            return {'error': 'Unauthorized'}, 401
        
        try:
            data = request.get_json()
            if not data:
                return {'error': 'No data provided'}, 400
            
            title = data.get('title')
            instructions = data.get('instructions')
            minutes_to_complete = data.get('minutes_to_complete')
            
            if not title or not instructions or minutes_to_complete is None:
                return {'error': 'Title, instructions, and minutes_to_complete are required'}, 400
            
            new_recipe = Recipe(
                title=title,
                instructions=instructions,
                minutes_to_complete=minutes_to_complete,
                user_id=session['user_id']
            )
            
            db.session.add(new_recipe)
            db.session.commit()
            
            return new_recipe.to_dict(), 201
            
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 400


class RecipeDetail(Resource):
    def get(self, id):
        if 'user_id' not in session:
            return {'error': 'Unathorized'}, 401

        recipe = Recipe.query.get(id)
        if not recipe:
            return {'error': 'Recipe not found'}, 404
        
        if recipe.user_id != session['user_id']:
            return {'error': 'Unauthorized'}, 401
        
        return recipe.to_dict(), 200
    
    def patch(self, id):
        if 'user_id' not in session:
            return {'error': 'Unauthorized'}, 401
        
        recipe = Recipe.query.get(id)
        if not recipe:
            return {'error': 'Recipe not found'}, 404
        
        if recipe.user_id != session['user_id']:
            return {'error': 'Unauthorized - you can only edit your own recipes'}, 403
        
        try:
            data = request.get_json()
            if not data:
                return {'error': 'No data provided'}, 400
            
            if 'title' in data:
                recipe.title = data['title']
            if 'instructions' in data:
                recipe.instructions = data['instructions']
            if 'minutes_to_complete' in data:
                recipe.minutes_to_complete = data['minutes_to_complete']
            
            db.session.commit()
            
            return recipe.to_dict(), 200
            
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 400
    
    def delete(self, id):
        if 'user_id' not in session:
            return {'error': 'Unauthorized'}, 401
        
        recipe = Recipe.query.get(id)
        if not recipe:
            return {'error': 'Recipe not found'}, 404
        
        if recipe.user_id != session['user_id']:
            return {'error': 'Unauthorized - you can only delete your own recipes'}, 403
        
        try:
            db.session.delete(recipe)
            db.session.commit()
            return {}, 204
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 400


api.add_resource(RecipeList, '/recipes')
api.add_resource(RecipeDetail, '/recipes/<int:id>')


if __name__ == '__main__':
    app.run(port=5555, debug=True)