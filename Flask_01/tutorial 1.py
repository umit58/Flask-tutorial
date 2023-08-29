from flask import Flask, redirect, url_for,render_template, request, flash, session
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'abcdefg'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes=5)

db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email

@app.route('/')
def home():
    return  render_template("index.html")

@app.route("/views")
def views():
    return  render_template("views.html", values=users.query.all())

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.permanent = True
        user = request.form['nm']
        session["user"] = user

        found_user = users.query.filter_by().first()
        if found_user:
            session["email"] = found_user.email

        else:
            usr = users(user, "")
            db.session.add(usr)
            db.session.commit()
        flash("Login Successfuly!")
        return redirect(url_for("user"))

    elif "user" in session:
        flash("Already Logged In!")
        return redirect(url_for("user"))
    else:
        return  render_template("login.html")

@app.route("/user", methods=['GET', 'POST'])
def user():
    email = None
    if "user" in session:
        user = session["user"]
        if request.method == 'POST':
            email = request.form["email"]
            session["email"] = email
            found_user = users.query.filter_by().first()
            found_user.email = email
            db.session.commit()
            flash("Email was saved!")
        else:
            if "email" in session:
                email = session["email"]
        return  render_template("user.html", email=email, user=user)
    else:
        flash("You are not Logged In!")
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    if "user" in session:
        user = session["user"]
        flash(f"You have been logged out, {user}!", "info")
    session.pop("user", None)
    session.pop("email", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    with app.app_context():
      db.create_all()
    app.run(debug=True)