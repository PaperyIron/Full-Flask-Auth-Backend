from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from config import db, bcrypt

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    _password_hash = db.Column(db.String(100), nullable=False)

@hybrid_property
def password_hash(self):
    raise AttributeError('cannot read password hashes')

@password_hash.setter
def password_hash(self, password):
    self._password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

def authenticate(self, password):
    return bcrypt.check_password_hash(self._password_hash, password)

def __repr__(self):
    return f'<User: {self.username}>'


