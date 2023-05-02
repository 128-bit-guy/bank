from flask import Flask, render_template, request, session
from accounts import *
app = Flask("Bank")
app.secret_key = "admin"


def handle_account():
    if request.method == 'POST':
        if 'log_out' in request.form:
            del session["login"]
            return None
        else:
            login = request.form['login']
            password = request.form['password']
            if 'log_in' in request.form:
                if login in accounts:
                    if password == accounts[login].password:
                        session["login"] = login
                        return None
                    else:
                        return "Invalid password!"
                else:
                    return "User does not exist!"
            else:
                if login in accounts:
                    return "User already exists!"
                else:
                    accounts[login] = Account(login, password, 0)
                    session["login"] = login
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


app.run()
