# Flask BackEnd Authorization Lab

## To Run
1. Clone repository to your local machine.
2. Open a terminal in the root directory.
3. Run 'pipenv install' or 'pip3 install -r requirements.txt' to install required dependencies.
4. Run 'pipenv shell'
5. cd into the client-with-sessions folder.
6. Run 'npm install'
7. Run 'npm start'
8. Open a new terminal window in the root directory.
9. Run 'pipenv shell'
10. cd into the server folder
11. Run 'python app.py'
12. (Optional) Run 'python seed.py' if database is not populated
12. Open 'http://localhost:4000' in your browser to view the website.

## To Test Endpoints with Postman
### Signup Endpoint
1. Set method to POST
2. URL: http://localhost:5555/signup
3. Click 'headers' tab and ensure key: Content-Type and value: application/json
4. Click 'body' tab. Select raw radio button and JSON from the dropdown.
5. Paste:
'''json
{
  "username": "testuser",
  "password": "password123",
  "password_confirmation": "password123"
}
'''

### Login Endpoint
1. Set method to POST
2. URL: http://localhost:5555/login
3. Click 'headers' tab and ensure key: Content-Type and value: application/json
4. Click 'body' tab. Select raw radio button and JSON from the dropdown.
5. Paste:
```json
{
  "username": "testuser",
  "password": "password123"
}
```

### Check-Session Endpoint
1. Set method to GET
2. URL: http://localhost:5555/check_session

### Logout Endpoint
1. Set method to DELETE
2. URL: http://localhost:5555/logout

### Create Recipe Endpoint
1. Set method to POST
2. URL: http://localhost:5555/recipes
3. Click 'headers' tab and ensure key: Content-Type and value: application/json
4. Click 'body' tab. Select raw radio button and JSON from the dropdown.
5. Paste:
'''json
{
    "title": "Cookies",
    "instructions": "1. Heat oven. 2. Bake the cookies. 3. Serve",
    "minutes_to_complete": 30
}
'''

### Get All Recipes Endpoint
You must be logged in to get recipes
1. Set method to GET
2. URL: http://localhost:5555/recipes



## API Endpoints Summary

| Endpoint | Method | Auth Required | Description |
|----------|--------|---------------|-------------|
| `/signup` | POST | No | Create new user account |
| `/login` | POST | No | Log in existing user |
| `/check_session` | GET | Yes | Check if logged in |
| `/logout` | DELETE | Yes | Log out current user |
| `/recipes` | GET | Yes | Get all your recipes |
| `/recipes` | POST | Yes | Create a new recipe |
| `/recipes/<id>` | GET | Yes | Get a specific recipe (must own it) |
| `/recipes/<id>` | PATCH | Yes | Update a recipe (must own it) |
| `/recipes/<id>` | DELETE | Yes | Delete a recipe (must own it) |
