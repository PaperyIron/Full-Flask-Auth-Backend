from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from config import db, bcrypt

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    _password_hash = db.Column(db.String(100), nullable=False)
    
    recipes = db.relationship('Recipe', back_populates='user', cascade='all, delete-orphan')
    
    @hybrid_property
    def password_hash(self):
        raise AttributeError('Password hashes cannot be viewed')
    
    @password_hash.setter
    def password_hash(self, password):
        if len(password) < 8:
            raise ValueError('Password must be at least 8 characters')
        self._password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password)
    
    def to_dict(self, include_recipes=False):
        user_dict = {
            'id': self.id,
            'username': self.username
        }
        if include_recipes:
            user_dict['recipes'] = [recipe.to_dict(include_user=False) for recipe in self.recipes]
        return user_dict
    
    def __repr__(self):
        return f'<User: {self.username}>'


class Recipe(db.Model):
    __tablename__ = 'recipes'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    minutes_to_complete = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    user = db.relationship('User', back_populates='recipes')
    
    @validates('title')
    def validate_title(self, key, title):
        if not title or len(title.strip()) == 0:
            raise ValueError('Title cannot be empty')
        if len(title) > 100:
            raise ValueError('Title must be less than 100 characters')
        return title
    
    @validates('instructions')
    def validate_instructions(self, key, instructions):
        if not instructions or len(instructions.strip()) == 0:
            raise ValueError('Instructions cannot be empty')
        if len(instructions) < 50:
            raise ValueError('Instructions must be at least 50 characters')
        return instructions
    
    @validates('minutes_to_complete')
    def validate_minutes(self, key, minutes):
        if minutes is None or minutes < 1:
            raise ValueError('Minutes to complete must be at least 1')
        return minutes
    
    def to_dict(self, include_user=True):
        recipe_dict = {
            'id': self.id,
            'title': self.title,
            'instructions': self.instructions,
            'minutes_to_complete': self.minutes_to_complete,
            'user_id': self.user_id
        }
        if include_user:
            recipe_dict['user'] = {
                'id': self.user.id,
                'username': self.user.username
            }
        return recipe_dict
    
    def __repr__(self):
        return f'<Recipe: {self.title}>'