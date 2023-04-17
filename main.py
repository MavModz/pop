from flask import Flask, jsonify, render_template, request, redirect, session, url_for
import mysql.connector
import os, re

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

    # Perform email validation using regular expression
    email_regex = r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if not re.match(email_regex, email):
        return jsonify({'status': 'failure', 'message': 'Please enter a valid email address!'})

    # Perform registration logic and check if email and password match in database
    cursor.execute(""" SELECT * FROM `users` where `email` LIKE '{}' AND `password` LIKE '{}' """
                   .format(email, password))
    users = cursor.fetchall()
    if len(users) > 0:
        session['user_id'] = users[0][0]
        return jsonify({'status': 'success', 'message': 'Login successful!'})  # Return success status and message as JSON response
    else:
        return jsonify({'status': 'failure', 'message': 'Email or password is incorrect!'})  # Return failure status and message as JSON response



@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.form.get('uname')
    email = request.form.get('uemail')
    password = request.form.get('upassword')

    cursor.execute("SELECT `email` FROM `users`")
    users = cursor.fetchall()
    print(users)
    print(email)

    if any(user[0] == email for user in users):
        print('Email already exists!')
        return "fail"
    else:
        cursor.execute("""INSERT INTO `users` (`user_id`, `name`, `email`, `password`) VALUES (NULL, '{}', '{}', '{}')""".format(name, email, password))
        conn.commit()
        print('Registration successful!')
        return "success"

@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')


@app.route('/new_login')
def new_login():
        return render_template('new_login.html')

@app.route('/get_user_name')
def get_user_name():
    if 'user_id' in session:
        user_id = session['user_id']
        cursor.execute("SELECT name FROM users WHERE id = %s", (user_id,))
        row = cursor.fetchone()
        if row:
            name = row[0]
            return jsonify({'success': True, 'name': name})
        else:
            return jsonify({'success': False, 'message': 'User not found'})
    else:
        return jsonify({'success': False, 'message': 'User not logged in'})    

if __name__ == "__main__":
    app.run(debug=True)