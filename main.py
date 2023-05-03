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
                               balance="Неограниченно" if accounts[session["login"]].unlimited_money else accounts[
                                   session["login"]].balance)
    else:
        return render_template("error.html", error="Для того чтобы пользоваться этой страницой необходимо войти в "
                                                   "учётную запись")


@app.route("/send_money", methods=['GET', 'POST'])
def draw_send_money():
    x = handle_account()
    if x is not None:
        return x
    elif "login" in session:
        if 'send_money' in request.form:
            user = request.form['user']
            money_count = request.form['money_count']
            if not money_count.isnumeric():
                return render_template("error.html", error="Количество денег должно быть числом")
            money_count = int(money_count)
            if money_count <= 0:
                return render_template("error.html", error="Количество денег должно быть положительным")
            if user not in accounts:
                return render_template("error.html", error="Заданного пользователя не существует")
            if not accounts[session["login"]].send_money(money_count, accounts[user]):
                return render_template("error.html", error="Недостаточно средств")
        return render_template("send_money.html", logged_in=True, login=session["login"])
    else:
        return render_template("error.html", error="Для того чтобы пользоваться этой страницой необходимо войти в "
                                                   "учётную запись")


app.run()
