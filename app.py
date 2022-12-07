import pyodbc
from flask import Flask, render_template, redirect, url_for, request
import os

app = Flask(__name__)

@app.route("/", methods = ['GET'])
def home():
    return render_template("index.html", list=list, add_user_msg=add_user_msg, update_user_msg=update_user_msg,
                           delete_user_msg = delete_user_msg)

@app.route("/refresh_users", methods = ['GET'])
def refresh_users():
    global list
    list = get_all_users()
    return redirect(url_for("home"))

@app.route("/add_user", methods = ['GET'])
def add_user():
    global add_user_msg
    name = request.args.get('name')
    login = request.args.get('login')
    password = request.args.get('password')
    if name == '' or login == '' or password == '':
        add_user_msg = 'Specify `name`, `login` and `password` to register new user!'
    else:
        add_user_msg = 'New user registered successfully!'
        connection = open_connection()
        insert_user(connection, name, login, password)
        connection.close()
    return redirect(url_for("home"))

@app.route("/update_user", methods = ['GET'])
def update_user():
    global update_user_msg
    id = request.args.get('id2')
    name = request.args.get('name2')
    login = request.args.get('login2')
    password = request.args.get('password2')
    if id == '':
        update_user_msg = 'Specify id of the user you want to update!'
    elif name == '' and login == '' and password == '':
        update_user_msg = 'Specify `name`, `login` or `password` to update!'
    else:
        if name != '':
            connection = open_connection()
            update_user_name(connection, id, name)
            connection.close()
        if login != '':
            connection = open_connection()
            update_user_login(connection, id, login)
            connection.close()
        if password != '':
            connection = open_connection()
            update_user_password(connection, id, password)
            connection.close()
        update_user_msg = 'Updated successfully!'
    return redirect(url_for("home"))

@app.route("/delete_user", methods = ['GET'])
def delete_user():
    global delete_user_msg
    id = request.args.get('id3')
    if id == '':
        delete_user_msg = 'Specify id of the user you want to delete!'
    else:
        connection = open_connection()
        delete_user(connection, id)
        connection.close()
        delete_user_msg = 'User deleted successfully!'
    return redirect(url_for("home"))


def open_connection():
    connection = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=tcp:ctl-server.database.windows.net,1433;Database=individual_db;'
                    'Uid=azureuser;Pwd=Ind_1111;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
    connection.autocommit = True
    return connection

def select_users(connection):
    with connection.cursor() as cursor:
        cursor.execute(
            """SELECT * FROM users;"""
        )
        users = cursor.fetchall()
    return users

def insert_user(connection, name, login, password):
    new_id = select_max_id(connection) + 1
    with connection.cursor() as cursor:
        cursor.execute(
            f"""INSERT INTO users (id, name, login, password) VALUES
            ({new_id}, '{name}', '{login}', '{password}');"""
        )

def update_user_name(connection, id, name):
    with connection.cursor() as cursor:
        cursor.execute(
            f"""UPDATE users SET login = '{name}' WHERE id = {id};"""
        )

def update_user_login(connection, id, login):
    with connection.cursor() as cursor:
        cursor.execute(
            f"""UPDATE users SET login = '{login}' WHERE id = {id};"""
        )

def update_user_password(connection, id, password):
    with connection.cursor() as cursor:
        cursor.execute(
            f"""UPDATE users SET login = '{password}' WHERE id = {id};"""
        )

def delete_user(connection, id):
    with connection.cursor() as cursor:
        cursor.execute(
            f"""DELETE FROM users WHERE id = {id};"""
        )

def select_max_id(connection):
    with connection.cursor() as cursor:
        cursor.execute(
            f"""SELECT MAX(id) FROM users;"""
        )
        id = int(str(cursor.fetchone()[0]))
    return id

def get_all_users():
    connection = open_connection()
    users = select_users(connection)
    result = []
    for user in users:
        result.append(' - id: ' + str(user[0]) + '; name: ' + user[1] + '; login: ' + user[2] + '; password: ' + user[3])
    connection.close()
    return result


list = get_all_users()
add_user_msg = ''
update_user_msg = ''
delete_user_msg= ''

if __name__ == '__main__':
    print(pyodbc.version)
    '''connection = open_connection()
    with connection.cursor() as cursor:
        cursor.execute(
            """INSERT INTO plants (user_id, name) VALUES
        (1, 'orchid'),
        (1, 'cactus'),
        (2, 'rose'),
        (2, 'cactus'),
        (3, 'rose');"""
        )
    connection.close()'''
    server_port = os.environ.get('PORT', '7777')
    app.run(debug=True, port=server_port, host='0.0.0.0')