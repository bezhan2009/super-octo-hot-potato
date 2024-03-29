from flask import Flask, jsonify, url_for, request, render_template, redirect, session

app = Flask(__name__)
app.secret_key = 'bezhan200910203040'
import psycopg2

db_name = "postgres"
user = "postgres"
password = "bezhan2009"
port = "5432"
host = "127.0.0.1"

conn = psycopg2.connect(
        dbname=db_name,
        user=user,
        password=password,
        host=host,
        port=port
    )

cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS people(id SERIAL PRIMARY KEY,user_name VARCHAR(50) UNIQUE,last_name VARCHAR(50) NOT NULL,password VARCHAR(50) NOT NULL,age INT NOT NULL,UNIQUE (id))")
cursor.execute("CREATE TABLE IF NOT EXISTS Accounts_users(id serial, user_id INT NOT NULL , user_name_id VARCHAR(40), account_number VARCHAR(70), balance  INT DEFAULT 10000, FOREIGN KEY (user_id) REFERENCES people (id));")
cursor.execute("CREATE TABLE IF NOT EXISTS Transactions_users(id serial, user_id_1 INT NOT NULL, account_number_1 VARCHAR(70), account_number_2 VARCHAR(70), sum_transfer INT NOT NULL)")
cursor.execute("CREATE TABLE IF NOT EXISTS Logined_users(id serial, login_user_p VARCHAR(40))")
# cursor.execute("DROP TABLE IF EXISTS people CASCADE")
# cursor.execute("DROP TABLE IF EXISTS Logined_users CASCADE")
# cursor.execute("DROP TABLE IF EXISTS Transactions_users CASCADE")
# cursor.execute("DROP TABLE IF EXISTS Accounts_users CASCADE")
# conn.commit()
# cursor.execute("ALTER TABLE Accounts_users ADD is_deleted bool DEFAULT false")
conn.commit()
cursor.execute("SELECT * FROM Accounts_users")
view_for_bugs = cursor.fetchall()
cursor.execute("SELECT * FROM people")
view_for_bugs_2 = cursor.fetchall()
if not view_for_bugs and not view_for_bugs_2:
    cursor.execute("INSERT INTO people(user_name, last_name, password, age) VALUES ('1', '1', '1', '1')")
    cursor.execute("INSERT INTO Accounts_users(user_id, account_number) VALUES (%s, %s)", (1, '9847293'))
    conn.commit()

elif not view_for_bugs:
    cursor.execute("INSERT INTO Accounts_users(user_id, account_number) VALUES (%s, %s)", (1, '9847293'))
    conn.commit()

elif not view_for_bugs_2:
    cursor.execute("INSERT INTO Accounts_users(user_id, account_number) VALUES (%s, %s)", (1, '9847293'))
    conn.commit()

def manually_connect(_db_name, _user, _password):
    if not _db_name:
        _db_name = "postgres"
    elif not _user:
        _user = "postgres"
    elif not _user and not _db_name:
        _user = "postgres"
        _db_name = "postgres"

    db_name = _db_name
    user = _user
    password = _password
    port = "5432"
    host = "127.0.0.1"

    conn = psycopg2.connect(
        dbname=db_name,
        user=user,
        password=password,
        host=host,
        port=port
    )


def get_err(err):
    with app.app_context():
        return render_template("error_p.html", reall_error=err)


def login_user(login, password):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM people WHERE user_name = %s AND password = %s", (login, password))
    x = cursor.fetchone()
    if x:
        return True
    else:
        return False

def create_an_account(_id, acc_num):
    cursor = conn.cursor()
    x = True
    try:
        cursor.execute('INSERT INTO Accounts_users  '
                       '(user_id, account_number) '
                       'VALUES (%s, %s)', (_id, acc_num,))
        conn.commit()

        cursor.execute('SELECT user_name FROM people WHERE id = %s', (_id, ))
        get_name = cursor.fetchone()[0]

        cursor.execute('UPDATE Accounts_users SET user_name_id = %s WHERE user_id = %s', (get_name, _id))
        conn.commit()
    except BaseException as e:
        x = False
    return x

def delete_an_account(_id, acc_num):
    cursor = conn.cursor()
    cursor.execute("SELECT account_number FROM Accounts_users WHERE user_id = %s AND account_number = %s AND is_deleted = 'False'", (_id, acc_num))
    result = cursor.fetchall()
    if result:
        cursor.execute("UPDATE Accounts_users SET is_deleted = 'True' WHERE user_id = %s AND account_number = %s", (_id, acc_num))
        conn.commit()
        return True
    else:
        return False

def withdraw_money(_id, acc_num, amount):
    cursor = conn.cursor()
    cursor.execute("SELECT account_number FROM Accounts_users WHERE user_id = %s AND account_number = %s AND is_deleted = 'False'", (_id, acc_num))
    result = cursor.fetchall()
    if result:
        cursor.execute(
            "SELECT balance FROM Accounts_users WHERE user_id = %s AND account_number = %s AND is_deleted = 'False'",
            (_id, acc_num))
        get_balance = cursor.fetchall()
        if get_balance[0][0] > int(amount):
            cursor.execute("UPDATE Accounts_users SET balance = balance - %s WHERE user_id = %s AND account_number = %s", (amount ,_id, acc_num))
            conn.commit()
            return True

        else:
            return render_template('amount_error.html')
    else:
        return False

def fill_money(_id, acc_num, amount):
    cursor = conn.cursor()
    cursor.execute("SELECT account_number FROM Accounts_users WHERE user_id = %s AND account_number = %s AND is_deleted = 'False'", (_id, acc_num))
    result = cursor.fetchall()
    if result:
        cursor.execute("UPDATE Accounts_users SET balance = balance + %s WHERE user_id = %s AND account_number = %s", (amount, _id, acc_num))
        conn.commit()
        return True

    else:
        return False

def transfer_money(_id, acc_num_1, acc_num_2, amount):
    cursor = conn.cursor()
    cursor.execute("SELECT account_number FROM Accounts_users WHERE user_id = %s AND account_number = %s AND is_deleted = 'False'", (_id, acc_num_1))
    result_1 = cursor.fetchall()
    cursor.execute(
        "SELECT account_number FROM Accounts_users WHERE account_number = %s AND is_deleted = 'False'",
        (acc_num_2, ))
    result_2 = cursor.fetchall()
    if result_1 and result_2:
        cursor.execute(
            "SELECT balance FROM Accounts_users WHERE user_id = %s AND account_number = %s AND is_deleted = 'False'",
            (_id, acc_num_1))
        cursor.execute(
            "SELECT balance FROM Accounts_users WHERE account_number = %s AND is_deleted = 'False'",
            (acc_num_2, ))
        get_balance = cursor.fetchall()
        if get_balance[0][0] > int(amount):
            cursor.execute("UPDATE Accounts_users SET balance = balance - %s WHERE user_id = %s AND account_number = %s", (amount ,_id, acc_num_1))
            cursor.execute(
                "UPDATE Accounts_users SET balance = balance + %s WHERE account_number = %s",
                (amount, acc_num_2))

            conn.commit()
            return True

        else:
            return render_template('amount_error.html')
    else:
        return False