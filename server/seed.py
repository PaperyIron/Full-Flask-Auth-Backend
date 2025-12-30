from app import app
from config import db
from models import User, Recipe

def seed_data():
    with app.app_context():
        User.query.delete()
        Recipe.query.delete()
        db.session.commit()
        
        users_data = [
            {'username': 'alice', 'password': 'password123'},
            {'username': 'bob', 'password': 'password123'},
            {'username': 'charlie', 'password': 'password123'},
        ]
        
        users = []
        for user_data in users_data:
            user = User(username=user_data['username'])
            user.password_hash = user_data['password']
            db.session.add(user)
            users.append(user)
        
        db.session.commit()
        
        recipes_data = [
            {
                'title': 'Chocolate Chip Cookies',
                'instructions': 'Preheat oven to 350°F. Mix butter and sugars until fluffy. Add eggs and vanilla. Combine dry ingredients separately, then mix into wet ingredients. Fold in chocolate chips. Bake for 10-12 minutes.',
                'minutes_to_complete': 30,
                'user': users[0]
            },
            {
                'title': 'Spaghetti Carbonara',
                'instructions': 'Cook spaghetti according to package directions. Fry pancetta until crispy. Mix eggs with parmesan. Toss hot pasta with pancetta, then quickly stir in egg mixture off heat. Season with black pepper.',
                'minutes_to_complete': 25,
                'user': users[0]
            },
            {
                'title': 'Caesar Salad',
                'instructions': 'Tear romaine lettuce into bite-sized pieces. Make dressing with mayo, lemon juice, garlic, anchovies, and parmesan. Toss lettuce with dressing. Top with croutons and extra parmesan cheese.',
                'minutes_to_complete': 15,
                'user': users[1]
            },
            {
                'title': 'Chicken Stir Fry',
                'instructions': 'Cut chicken into bite-sized pieces. Heat oil in wok. Cook chicken until done, remove. Stir fry vegetables in same pan. Return chicken, add soy sauce and ginger. Serve over rice.',
                'minutes_to_complete': 20,
                'user': users[1]
            },
            {
                'title': 'Banana Bread',
                'instructions': 'Mash overripe bananas. Mix with melted butter, sugar, egg, and vanilla. Add flour, baking soda, and salt. Pour into greased loaf pan. Bake at 350°F for 60 minutes until golden brown.',
                'minutes_to_complete': 75,
                'user': users[2]
            },
            {
                'title': 'Tomato Soup',
                'instructions': 'Sauté onions and garlic in butter. Add canned tomatoes, chicken broth, and herbs. Simmer for 20 minutes. Blend until smooth. Stir in cream and season with salt and pepper to taste.',
                'minutes_to_complete': 35,
                'user': users[2]
            },
            {
                'title': 'Grilled Cheese Sandwich',
                'instructions': 'Butter two slices of bread on one side each. Place cheese between unbuttered sides. Grill in pan over medium heat until golden brown on both sides and cheese is melted. Serve hot.',
                'minutes_to_complete': 10,
                'user': users[0]
            },
            {
                'title': 'Pancakes',
                'instructions': 'Mix flour, sugar, baking powder, and salt. In another bowl, whisk milk, egg, and melted butter. Combine wet and dry ingredients. Cook on griddle until bubbles form, then flip. Cook until golden.',
                'minutes_to_complete': 20,
                'user': users[1]
            },
        ]
        
        for recipe_data in recipes_data:
            recipe = Recipe(
                title=recipe_data['title'],
                instructions=recipe_data['instructions'],
                minutes_to_complete=recipe_data['minutes_to_complete'],
                user_id=recipe_data['user'].id
            )
            db.session.add(recipe)
        
        db.session.commit()

if __name__ == '__main__':
    seed_data()