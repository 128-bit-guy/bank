from flask import Flask, render_template, request

app = Flask("Bank")


@app.route("/", methods=['GET', 'POST'])
def draw_index():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        log_in = 'log_in' in request.form
        return login + " " + password + " " + str(log_in)
    return render_template("index.html")


app.run()
