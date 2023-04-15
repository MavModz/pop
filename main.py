from flask import Flask, render_template, request, redirect, session, url_for
import mysql.connector
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

conn = mysql.connector.connect(
    host="localhost", user="root", password="", database="loan_db")
cursor = conn.cursor()


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/popup')
def popup():
    return render_template('popup.html')

@app.route('/login')
def login():
    if 'user_id' not in session:
        return render_template('login.html')
    else:
        return redirect('/dashboard')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        return render_template('dashboard.html')
    else:
        return redirect('/login')


@app.route('/login_validation', methods=['POST'])
def login_validation():
    email = request.form.get('email')
    password = request.form.get('password')

    cursor.execute(""" SELECT * FROM `users` where `email` LIKE '{}' AND `password` LIKE '{}' """
                   .format(email, password))
    users = cursor.fetchall()
    if len(users) > 0:
        session['user_id'] = users[0][0]
        return redirect('/dashboard')
    else:
        return redirect('/')


@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.form.get('uname')
    email = request.form.get('uemail')
    password = request.form.get('upassword')

    cursor.execute(""" SELECT `email` From `users` """ .format(email))
    users = cursor.fetchall()
    print(len(users))
    print(email)

    if (len(users) == 0):
        cursor.execute("""INSERT INTO `users` (`user_id`, `name`, `email`, `password`) VALUES (NULL, '{}', '{}', '{}')""". format(name, email, password))
        conn.commit()
        print('if loop')
        return "success"
    elif (users[0][0] != email):
        cursor.execute("""INSERT INTO `users` (`user_id`, `name`, `email`, `password`) VALUES (NULL, '{}', '{}', '{}')""". format(name, email, password))
        conn.commit()
        print('elif loop')
        return "success"
    else:
        print('else loop')
        return "fail"

@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')

@app.route('/new_login')
def new_login():
    return render_template('/new_login.html')

if __name__ == "__main__":
    app.run(debug=True)