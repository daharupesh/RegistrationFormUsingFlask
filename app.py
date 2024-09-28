from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

db_config = {
    'host': 'localhost',
    'database': 'mydatabase',
    'user': 'root',
    'password': ''
}

@app.route('/')
def index():
    return redirect(url_for('register'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password'] 

        try:
            connection = mysql.connector.connect(**db_config)
            if connection.is_connected():
                cursor = connection.cursor()
                insert_query = """INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"""
                cursor.execute(insert_query, (name, email, password))
                connection.commit()
                cursor.close()
                connection.close()
                return redirect(url_for('success'))
        except Error as e:
            print(f"Error: {e}")
            return "An error occurred. Please try again."

    return render_template('register.html')

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True)
