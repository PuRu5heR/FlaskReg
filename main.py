from flask import Flask, render_template, request, flash, redirect

import users
from users import Users
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, logout_user, current_user, login_required, login_user
from UserLogin import UserLogin
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = "546t5i6tn54ui54i84u7eh584e"
login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    return UserLogin().fromDB(user_id, Users())


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/reg")
@app.route("/reg", methods=["POST"])
def forma():
    flash("")
    if request.method == "POST":
        if request.form['password'] != request.form['password_repeat']:
            print("fdsfs")
            flash("Passwords doesnt't match")
        elif request.form['login'] == "":
            flash("Login is empty")
        elif request.form['password'] == "":
            flash("Password is empty")
        elif request.form['e_mail'] == "":
            flash("E-mail is empty")
        elif request.form['birth_date'] == "":
            flash("Birth date is empty")
        elif request.form['full_name'] == "":
            flash("Full name is empty")
        elif len(request.form['full_name'].split(" ")) != 3:
            flash("Incorrect full name")
        elif len(request.form['e_mail'].split("@")[1].split(".")) != 2 or \
                len(request.form['e_mail'].split("@")[1].split(".")[1]) > 4:
            flash("Incorrect e-mail")
        elif Users().login_is_unique(request.form['login']):
            flash("Login already exists")
        else:
            print(request.form)
            Users().new_user(request.form['login'], generate_password_hash(request.form['password']),
                             request.form['e_mail'],
                             request.form['full_name'], request.form['birth_date'])
            return redirect("/")
    return render_template("registration.html")


@app.route("/login")
@app.route("/login", methods=["POST"])
def login():
    flash("")
    if request.method == "POST":
        user = Users().get_data_by_login(request.form['login'])
        if user is not None and check_password_hash(user[2], request.form['password']):
            ls = UserLogin().create_user(user)
            login_user(ls)
            return redirect("/homepage")
        else:
            flash("Wrong password")
    return render_template("login.html")


@app.route("/homepage")
@login_required
def homepage():
    user = current_user.get_user()
    return render_template("homepage.html", user=user)


@app.route("/files")
@login_required
def files():
    D = app.root_path + "\\files\\" + str(current_user.get_user()[1])
    directory = os.listdir(D)
    out = ""
    for file in directory:
        print(file)
        out += "<a href=http://192.168.58.2:5000/download/" + file + ">" + file + "</a><br>"

    out += "<a href=/homepage>Home page</a>"
    return out


@app.route("/download/<file>")
def download(file):
    D = app.root_path + "\\files\\" + str(current_user.get_user()[1] + "\\")
    print(D)
    return send_from_directory(directory=D, path=file)


@app.route("/logout")
@login_required
def log_out():
    logout_user()
    return redirect("/")


@app.route("/test")
@login_required
def testing():
    return "OK"


@app.route("/upload")
@app.route("/upload", methods=["POST"])
def upload():
    if request.method == "POST":
        try:
            request.files['file'].save(
                os.path.join("files\\" + str(current_user.get_user()[1]), request.files['file'].filename))
        except FileNotFoundError:
            print(current_user.get_user()[1])
            os.mkdir("files\\" + str(current_user.get_user()[1]))
            request.files['file'].save(
                os.path.join("files\\" + str(current_user.get_user()[1]), request.files['file'].filename))
        import qrcode
        QR = qrcode.make("http://192.168.58.2:5000/download/" + request.files['file'].filename)
        QR.save("static\\images\\qr.png")
        return """<img src=/static/images/qr.png alt=QR-код>
        <a href="/homepage">Home page</a>"""
    return render_template("upload.html")


if __name__ == "__main__":
    app.run(debug=True)
