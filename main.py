from flask import Flask, render_template, request, session
from accounts import *
app = Flask("Bank")
app.secret_key = "admin"


def handle_account():
    if 'login' in session and not session['login'] in accounts:
        del session["login"]
    if request.method == 'POST':
        if 'log_out' in request.form:
            del session["login"]
            return None
        elif 'log_in' in request.form:
            login = request.form['login']
            password = request.form['password']
            if login in accounts:
                if password == accounts[login].password:
                    session["login"] = login
                    return None
                else:
                    return render_template("error.html", error="Неправильный пароль")
            else:
                return render_template("error.html", error="Пользователя с таким именем не существует")
        elif 'register' in request.form:
            login = request.form['login']
            password = request.form['password']
            if login in accounts:
                return render_template("error.html", error="Пользователь с таким именем уже существует")
            else:
                accounts[login] = Account(login, password, 0)
                session["login"] = login
                return None
    return None


@app.route("/", methods=['GET', 'POST'])
def draw_index():
    x = handle_account()
    if x is not None:
        return x
    elif "login" in session:
        return render_template("index.html", logged_in=True, login=session["login"])
    else:
        return render_template("index.html", logged_in=False)


@app.route("/account", methods=['GET', 'POST'])
def draw_account():
    x = handle_account()
    if x is not None:
        return x
    elif "login" in session:
        if 'change_password' in request.form:
            accounts[session["login"]].password = request.form['password']
        return render_template("account.html", logged_in=True, login=session["login"],
                               balance=accounts[session["login"]].balance)
    else:
        return render_template("error.html", error="Для того чтобы пользоваться этой страницой необходимо войти в "
                                                   "учётную запись")


app.run()
