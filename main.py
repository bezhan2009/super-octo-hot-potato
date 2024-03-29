try:

    from flask import Flask, jsonify, url_for, request, render_template, redirect, session

    from funs import *

    app = Flask(__name__)

    app.secret_key = 'bezhan200910203040'


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
    cursor.execute("CREATE TABLE IF NOT EXISTS Logined_users(id serial, login_user_p VARCHAR(40))")



    # cursor.execute("DROP TABLE Accounts_users CASCADE")
    # conn.commit()
    # cursor.execute("CREATE TABLE IF NOT EXISTS Accounts_users(id serial, user_id INT NOT NULL , user_name_id VARCHAR(40), account_number VARCHAR(70) UNIQUE, balance  INT DEFAULT 10000, is_deleted bool DEFAULT false, FOREIGN KEY (user_id) REFERENCES people (id))")
    # conn.commit()



    @app.route('/manually_connect', methods=['POST'])
    def manually_connect_p():
        db_name = request.form['db_name']
        user = request.form['user']
        password = request.form['password']
        manually_connect(db_name, user, password)

    @app.route('/', methods=['GET'])
    def index():
        try:
            cursor.execute("CREATE TABLE IF NOT EXISTS Loogined_users(id serial, login_user_p VARCHAR(40))")
            cursor.execute("SELECT * FROM Logined_users")
            view_logined = cursor.fetchone()
            if view_logined:
                session['user_name'] = view_logined[1]
                cursor.execute("SELECT * FROM people WHERE user_name = %s", (view_logined[1],))
                user_info = cursor.fetchone()
                conn.commit()
                if user_info:
                    user_info_dict = {
                        'user_name': user_info[0],
                        'last_name': user_info[1],
                        'password': user_info[2],
                        'age': user_info[3]
                    }
                    conn.commit()
                    return render_template("index.html", user_info=user_info_dict)

            else:
                return render_template("register.html")

        except BaseException as e:
            return render_template("error_p.html", reall_error=e)


    @app.route('/logout', methods=['GET'])
    def logout_():
        try:
            cursor.execute("DROP TABLE Logined_users CASCADE")
            cursor.execute("CREATE TABLE IF NOT EXISTS Loogined_users(id serial, login_user_p VARCHAR(40))")
            conn.commit()
            return render_template('login.html')

        except BaseException as e:
            return render_template("error_p.html", reall_error=e)


    @app.route('/register', methods=["POST"])
    def registr_add():
        try:
            cursor.execute("CREATE TABLE IF NOT EXISTS Logined_users(id serial, login_user_p VARCHAR(40))")
            conn.commit()
            cursor.execute("SELECT * FROM Logined_users")
            view_logined = cursor.fetchone()
            if view_logined:
                session['user_name'] = view_logined[1]
                cursor.execute("SELECT * FROM people WHERE user_name = %s", (view_logined[1],))
                user_info = cursor.fetchone()
                conn.commit()
                if user_info:
                    user_info_dict = {
                        'user_name': user_info[0],
                        'last_name': user_info[1],
                        'password': user_info[2],
                        'age': user_info[3]
                    }
                    conn.commit()
                    return render_template("index.html", user_info=user_info_dict)

            else:
                name = request.form['name']
                last_name = request.form['last_name']
                password = request.form['password']
                age = request.form['age']
                cursor.execute("SELECT user_name FROM people WHERE user_name = %s", (name, ))
                names = cursor.fetchall()

                if names:
                    return render_template("register_wrong.html")

                else:
                    cursor.execute("INSERT INTO Logined_users(login_user_p) VALUES (%s)", (name, ))
                    cursor.execute("INSERT INTO people(user_name, last_name, password, age) VALUES (%s, %s, %s, %s)",
                                   (name, last_name, password, age))
                    conn.commit()
                    session['user_name'] = name
                    conn.commit()
                    return redirect("http://127.0.0.1:5000/indexing_main")

        except BaseException as e:
            return render_template("error_p.html", reall_error=e)

    @app.route('/registration', methods=['GET'])
    def get_link_reg():
        return render_template('register.html')

    @app.route('/log', methods=['GET'])
    def get_link_log():
        return render_template('login.html')


    @app.route('/login', methods=["POST"])
    def login():
        try:
            cursor.execute("CREATE TABLE IF NOT EXISTS Logined_users(id serial, login_user_p VARCHAR(40))")
            cursor.execute("SELECT * FROM Logined_users")
            view_logined = cursor.fetchone()
            if view_logined:
                session['user_name'] = view_logined[1]
                cursor.execute("SELECT * FROM people WHERE user_name = %s", (view_logined[1],))
                user_info = cursor.fetchone()
                conn.commit()
                if user_info:
                    user_info_dict = {
                        'user_name': user_info[0],
                        'last_name': user_info[1],
                        'password': user_info[2],
                        'age': user_info[3]
                    }
                    conn.commit()
                    return render_template("index.html", user_info=user_info_dict)

            else:
                user_name = request.form['name']
                password = request.form['password']
                y = login_user(user_name, password)
                cursor.execute("SELECT * FROM people WHERE user_name = %s", (user_name, ))
                user_info = cursor.fetchone()
                conn.commit()
                if user_info:
                    user_info_dict = {
                        'user_name': user_info[0],
                        'last_name': user_info[1],
                        'password': user_info[2],
                        'age': user_info[3]
                    }
                    conn.commit()
                    if y:
                        session['user_name'] = user_name
                        cursor.execute("INSERT INTO Logined_users(login_user_p) VALUES (%s)", (user_name,))
                        conn.commit()
                        return render_template("index.html", user_info=user_info_dict)
                return render_template("login_wrong.html")

        except BaseException as e:
            return render_template("error_p.html", reall_error=e)


    @app.route('/accounts/<int:id_us>', methods=["GET"])
    def get_all_tasks(id_us):
        try:
            cursor.execute("SELECT * FROM people WHERE id = %s", (id_us,))
            user_info = cursor.fetchone()
            if user_info:
                user_info_dict = {
                    'user_name': user_info[0],
                    'last_name': user_info[1],
                    'password': user_info[2],
                    'age': user_info[3]
                }
                cursor.execute("SELECT * FROM Accounts_users WHERE user_id = %s AND is_deleted = 'False'", (user_info_dict['user_name'],))
                rows = cursor.fetchall()
                if rows:
                    serialized_accounts = []
                    for row in rows:
                        account = {
                            'user_id': row[1],
                            'user_name': row[2],
                            'acc_num': row[3],
                            'balance': row[4]
                        }
                        serialized_accounts.append(account)
                    return render_template("accounts_op.html", user_info=user_info_dict, account_info=serialized_accounts)
                else:
                    return render_template("no_accounts.html")
            else:
                return render_template('error_p.html')

        except BaseException as e:
            return render_template("error_p.html", reall_error=e)

    @app.route('/create_account/<int:id_us>', methods=["POST"])
    def create_acc(id_us):
        try:
            acc_num = request.form['acc_num']
            user_name = session.get('user_name')
            if user_name:
                cursor.execute("SELECT * FROM people WHERE user_name = %s", (user_name,))
                user_info = cursor.fetchone()
                user_info_dict = {
                    'user_name': user_info[0],
                    'last_name': user_info[1],
                    'password': user_info[2],
                    'age': user_info[3]
                }
                if create_an_account(id_us, acc_num):
                    return render_template('correct.html', user_info=user_info_dict)
                else:
                    return render_template("successfully.html")
            else:
                return render_template("successfully.html")

        except BaseException as e:
            return render_template("error_p.html", reall_error=e)




    @app.route('/dolo/<int:id_us>', methods=["POST"])
    def delete_acc(id_us):
        try:
            user_name = session.get('user_name')
            acc_num = request.form['acc_num']
            if delete_an_account(id_us, acc_num):
                cursor.execute("SELECT * FROM people WHERE user_name = %s", (user_name,))
                user_info = cursor.fetchone()
                user_info_dict = {
                    'user_name': user_info[0],
                    'last_name': user_info[1],
                    'password': user_info[2],
                    'age': user_info[3]
                }
                return render_template('correct.html', user_info=user_info_dict)

            else:
                cursor.execute("SELECT * FROM people WHERE user_name = %s", (user_name,))
                user_info = cursor.fetchone()
                user_info_dict = {
                    'user_name': user_info[0],
                    'last_name': user_info[1],
                    'password': user_info[2],
                    'age': user_info[3]
                }
                return render_template('successfully.html', user_info=user_info_dict)
        except BaseException as e:
            return render_template("error_p.html", reall_error=e)

    @app.route('/accounts_fill/<int:id_us>', methods=['POST'])
    def fill_money_(id_us):
        try:
            user_name = session.get('user_name')
            acc_num_fill = request.form['acc_num']
            amount = request.form['amount']
            if fill_money(id_us, acc_num_fill, amount):
                cursor.execute("SELECT * FROM people WHERE user_name = %s", (user_name,))
                user_info = cursor.fetchone()
                user_info_dict = {
                    'user_name': user_info[0],
                    'last_name': user_info[1],
                    'password': user_info[2],
                    'age': user_info[3]
                }
                return render_template('correct.html', user_info=user_info_dict)

            else:
                cursor.execute("SELECT * FROM people WHERE user_name = %s", (user_name,))
                user_info = cursor.fetchone()
                user_info_dict = {
                    'user_name': user_info[0],
                    'last_name': user_info[1],
                    'password': user_info[2],
                    'age': user_info[3]
                }
                return render_template('successfully.html', user_info=user_info_dict)

        except BaseException as e:
            return render_template("error_p.html", reall_error=e)

    @app.route('/accounts_withdraw/<int:id_us>', methods=['POST'])
    def withdraw_money_(id_us):
        try:
            user_name = session.get('user_name')
            acc_num_fill = request.form['acc_num']
            amount = request.form['amount']
            if withdraw_money(id_us, acc_num_fill, amount):
                cursor.execute("SELECT * FROM people WHERE user_name = %s", (user_name,))
                user_info = cursor.fetchone()
                user_info_dict = {
                    'user_name': user_info[0],
                    'last_name': user_info[1],
                    'password': user_info[2],
                    'age': user_info[3]
                }
                return render_template('correct.html', user_info=user_info_dict)

            else:
                cursor.execute("SELECT * FROM people WHERE user_name = %s", (user_name,))
                user_info = cursor.fetchone()
                user_info_dict = {
                    'user_name': user_info[0],
                    'last_name': user_info[1],
                    'password': user_info[2],
                    'age': user_info[3]
                }
                return render_template('successfully.html', user_info=user_info_dict)

        except BaseException as e:
            return render_template("error_p.html", reall_error=e)

    @app.route('/accounts_transfer/<int:id_us>', methods=['POST'])
    def transfer_money_(id_us):
        try:
            user_name = session.get('user_name')
            acc_num_fill_1 = request.form['acc_num_1']
            acc_num_fill_2 = request.form['acc_num_2']
            amount = request.form['amount']
            if transfer_money(id_us, acc_num_fill_1, acc_num_fill_2, amount):
                cursor.execute("SELECT * FROM people WHERE user_name = %s", (user_name,))
                user_info = cursor.fetchone()
                user_info_dict = {
                    'user_name': user_info[0],
                    'last_name': user_info[1],
                    'password': user_info[2],
                    'age': user_info[3]
                }
                return render_template('correct.html', user_info=user_info_dict)

            else:
                cursor.execute("SELECT * FROM people WHERE user_name = %s", (user_name,))
                user_info = cursor.fetchone()
                user_info_dict = {
                    'user_name': user_info[0],
                    'last_name': user_info[1],
                    'password': user_info[2],
                    'age': user_info[3]
                }
                return render_template('successfully.html', user_info=user_info_dict)

        except BaseException as e:
            return render_template("error_p.html", reall_error=e)


    @app.route('/indexing_main', methods=['GET'])
    def create_to():
        try:
            user_name = session.get('user_name')
            if user_name:
                cursor.execute("SELECT * FROM people WHERE user_name = %s", (user_name,))
                user_info = cursor.fetchone()
                conn.commit()
                user_info_dict = {
                    'user_name': user_info[0],
                    'last_name': user_info[1],
                    'password': user_info[2],
                    'age': user_info[3]
                }
                return render_template('index.html', user_info=user_info_dict)
            else:
                cursor.execute("SELECT * FROM people WHERE user_name = %s", (user_name,))
                user_info = cursor.fetchone()
                user_info_dict = {
                    'user_name': user_info[0],
                    'last_name': user_info[1],
                    'password': user_info[2],
                    'age': user_info[3]
                }
                return render_template('register.html', user_info=user_info_dict)

        except BaseException as e:
            return render_template("error_p.html", reall_error=e)


    if __name__ == '__main__':
        app.run(debug=True)

except BaseException as e:
    get_err(e)

