from app import app
from config import db
from models import User

def seed_data():
    with app.app_context():
        User.query.delete()
        db.session.commit()
        
        users = [
            {
                'username': 'alice',
                'password': 'password123'
            },
            {
                'username': 'bob',
                'password': 'password123'
            },
            {
                'username': 'charlie',
                'password': 'password123'
            },
            {
                'username': 'demo',
                'password': 'demo1234'
            },
            {
                'username': 'testuser',
                'password': 'test1234'
            }
        ]
        
        for user_data in users:
            user = User(username=user_data['username'])
            user.password_hash = user_data['password']
            db.session.add(user)
        
        db.session.commit()

if __name__ == '__main__':
    seed_data()