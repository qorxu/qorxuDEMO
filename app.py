from flask import Flask, redirect, render_template, session, request
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3, database

app = Flask(__name__)
app.secret_key = 'app.secret'

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

#Функция регистрации
@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        #Хеширование пароля
        hashed_password = generate_password_hash(password)


        #Уникальный логин при регистрации
        cursor.execute("SELECT * FROM Users WHERE login = ?", (login, ))
        if cursor.fetchone():
            error_login = "Такой логин уже существует"
            conn.close()
            return render_template('register.html', error_login=error_login)

        cursor.execute("INSERT INTO Users (login, password, role_id) VALUES (?, ?, ?)", (login, hashed_password, 1))
        
        conn.commit()
        conn.close()
        return redirect('/auther')

#Функция авторизации   
@app.route('/auther', methods=['POST'])
def auther():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']

        if login == 'Admin' and password == "AdminServ":
            session['login'] = 'Admin'
            return redirect('/admin_panel')

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Users WHERE login = ?", (login, ))
        user = cursor.fetchone()

        if user and check_password_hash(user[2], password):
            session['user_id'] = user[0]
            session['login'] = user[1]
            return redirect('/index')
        else:
            error = "Неверный логин или пароль"
            return render_template('auther.html', error=error)

#Функция записи
@app.route('/application', methods=['POST'])
def application():
    if request.method == 'POST':
        name_service = request.form['name_service']
        date = request.form['date']
        payment = request.form['payment']
        user_id = session['user_id']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute("INSERT INTO Applications (name_service, date, payment, user_id) VALUES (?, ?, ?, ?)", (name_service, date, payment, user_id))
        
        conn.commit()
        conn.close()
        return redirect('/my_application')
    
@app.route('/feedback', methods=['POST'])
def feedback():
    if request.method == 'POST':
        application_id = request.form['application_id']
        comment = request.form['comment']
        user_id = session['user_id']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute("INSERT INTO Feedbacks (application_id, comment, user_id) VALUES (?, ?, ?)", (application_id, comment, user_id))
        
        conn.commit()
        conn.close()
        return redirect('/index')

#Функция просмотра моих записей
@app.route('/my_application', methods=['GET'])
def my_application():
    if request.method == 'GET':
        user_id = session['user_id']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Applications WHERE user_id = ?", (user_id, ))
        user_application = cursor.fetchall()
        
        conn.close()
        return render_template('my_application.html', user_application=user_application)

#Админ панель
@app.route('/admin_panel', methods=['GET'])
def admin_panel():
    if request.method == 'GET':

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Applications")
        admin_application = cursor.fetchall()
        
        conn.close()
        return render_template('admin_panel.html', admin_application=admin_application)
    
@app.route('/update_status', methods=['POST'])
def update_status():
    id = request.form['id']
    status = request.form['status']

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("UPDATE Applications SET status = ? WHERE id = ?", (status, id))

    conn.commit()
    conn.close()
    return redirect('/admin_panel')

#Маршруты
@app.route('/')
def registers():
    return render_template('register.html')

@app.route('/auther')
def authers():
    return render_template('auther.html')

@app.route('/index')
def indexs():
    return render_template('index.html')

@app.route('/application')
def applications():
    return render_template('application.html')

@app.route('/my_application')
def my_applications():
    return render_template('my_application.html')

@app.route('/logout')
def logouts():
    session.clear()
    return redirect('/auther')

if __name__ == '__main__':
    app.run(debug=True)