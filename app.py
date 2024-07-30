from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Database connection
db_config = {
    'user': 'root',
    'password': '357159',  # Replace with your MySQL root password if any
    'host': 'localhost',
    'database': 'test'
}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    password = generate_password_hash(request.form['password'])

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        return "Sign up successful! <a href='/'>Log in now</a>"
    except mysql.connector.Error as err:
        return f"Error: {err}"
    finally:
        cursor.close()
        conn.close()


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result and check_password_hash(result[0], password):
        return redirect(url_for('welcome'))
    else:
        return "Invalid username or password. <a href='/'>Try again</a>"


@app.route('/welcome')
def welcome():
    return "Welcome! You have successfully logged in."


if __name__ == '__main__':
    app.run(debug=True)
