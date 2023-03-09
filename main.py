from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy
import random

# create the flask app object
app = Flask(__name__)
# secret key is used to encrypt the session data
app.secret_key = "hello"

# settings for sql database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# create the database object
db = SQLAlchemy(app)

class Student(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.Integer())
    rp = db.Column(db.Integer())

    def __init__(self, name, email):
        self.name = name
        self.email = email
        # TODO: password should be initialized to a random n-digit number
        randomPassword = random.randint(0000, 9999)
        if randomPassword in Student.password:
            randomPassword = random.randint(0000, 9999)
        self.password = random
        self.rp = 0

# route for the home page (it's just login)
@app.route("/", methods=["POST", "GET"])
@app.route("/home", methods=["POST", "GET"])
@app.route("/login", methods=["POST", "GET"])
def home():
    # first check if you're already logged in
    if 'student' in session:
        flash('You are already logged in!')
        return redirect(url_for("student"))
    elif 'teacher' in session:
        flash('You are already logged in!')
        return redirect(url_for("teacher"))
        
    return render_template("login.html")

# route for the signup page
@app.route("/signup", methods=["POST", "GET"])
def signup():
    # first check if you're already logged in
    if 'student' in session:
        return redirect(url_for("student"))
    elif 'teacher' in session:
        return redirect(url_for("teacher"))
    
    # if not, check if you're trying to sign up
    if request.method == "POST":
        
        # get the form data
        name = request.form["name"]
        period = request.form["period"]
        email = request.form["email"]
        
        # check if the email is already in the database
        if Student.query.filter_by(email=email).first():
            flash("Email already in use")
            return redirect(url_for("signup"))
        
        # if not, create a new student object and add it to the database
        student = Student(name, email)
        db.session.add(student)
        db.session.commit()
        
        # log the student in
        session['student'] = student.email
        return redirect(url_for("student"))
    
    # if you're not trying to sign up, just render the page
    return render_template("sign.html")

# route for the student view
@app.route("/student", methods=["POST", "GET"])
def student():
    return render_template("student.html", student=session['student'])

# route for the teacher view
@app.route("/teacher")
def teacher():
    return render_template("teacher.html")


if __name__ == "__main__":
    # create the database
    with app.app_context():
        db.create_all()
    # run the app
    app.run(debug=True)