from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

app = Flask(__name__,')
client = MongoClient('mongodb://localhost:27017/')
db = client['phonicly_db']
users_collection = db['users']

# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = users_collection.find_one({'email': email, 'password': password})
        if user:
            return render_template('home.html', message='Login successful!')
        else:
            return render_template('login.html', error='Invalid email or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        if users_collection.find_one({'email': email}):
            return render_template('signup.html', error='Email already exists')
        user_data = {'username': username, 'email': email, 'password': password}
        users_collection.insert_one(user_data)
        return render_template('login.html', message='User registered successfully!')
    return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True)
