from flask import Flask, redirect, url_for, request, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
import random
import requests

# create the flask app object
app = Flask(__name__)
# set the secret key for the session
app.secret_key = "hello"

# settings for sql database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# create the database object
db = SQLAlchemy(app)

teacherPassword = 314159


class Student(db.Model):
    # create columns
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    period = db.Column(db.Integer())
    email = db.Column(db.String(100))
    password = db.Column(db.Integer())
    rp = db.Column(db.Integer())

    def __init__(self, name, period, email):
        self.name = name
        self.period - period
        self.email = email
        # password is initialized to a random 6-digit number
        randomPassword = random.randint(000000, 999999)
        # make sure the password is unique
        if Student.query.filter_by(password=randomPassword).first():
            randomPassword = random.randint(000000, 999999)
        self.password = randomPassword
        self.rp = 0
    

# TODO: create the send_email method for registering students
def send_email(email, password):
    return


# route for the home page (it's just the login page)
@app.route("/", methods=["POST", "GET"])
@app.route("/home", methods=["POST", "GET"])
@app.route("/login", methods=["POST", "GET"])
def login():
    # first check if you're already logged in
    if 'student' in session:
        # redirect to the student view
        flash("You are already logged in!")
        return redirect(url_for("student"))
    elif 'teacher' in session:
        # redirect to the teacher view
        flash("You are already logged in!")
        return redirect(url_for("teacher"))
    else:
        # user is not logged in

        # check if the user is trying to log in
        if request.method == "POST":
            # get the form data
            password = request.form["password"]
            
            # prompt password again if it's not a number
            if not password.isdigit():
                flash("Please enter a number!")
                return redirect(url_for("login"))

            # convert the password into a number for checking with the database
            password = int(password)

            found_user = Student.query.filter_by(password=password).first()

            # if password found, log the user in
            if found_user:
                # check if the user is a teacher
                if found_user.password == teacherPassword:
                    # log the teacher in
                    session['teacher'] = found_user.name
                    flash("Logged in!")
                    return redirect(url_for("teacher"))
            # if password not found, display an error message
            else:
                flash("Password not found!")
                return redirect(url_for("login"))
        else:
            # user is not trying to log in -> display the login page
            return render_template("login.html")
    

# route for the register page
# *to be used only by students
@app.route("/signup")
@app.route("/register")
def register():
    # first check if the user is logged in
    if 'student' in session:
        # redirect to the student view
        flash("You are already logged in!")
        return redirect(url_for("student"))
    
    elif 'teacher' in session:
        # redirect to the teacher view
        flash("You are already logged in!")
        return redirect(url_for("teacher"))
    
    else:
        # user is not logged in

        # check if the user is trying to register
        if request.method == "POST":
            # user is trying to register
            
            # get the form data
            name = request.form["name"]
            period = request.form["period"]
            email = request.form["email"]

            # create a new student object
            new_student = Student(name, period, email)

            # TODO: send the new student's password to their email
            send_email(email, new_student.password)

            # add the new student to the database
            db.session.add(new_student)
            db.session.commit()

            # log the student in
            session['student'] = new_student

            # redirect to the student view
            flash("Registered!")
            return redirect(url_for("student"))
        else:
            # user is not trying to register
            # display the register page
            return render_template("register.html")

@app.route("/logout")
def logout():
    # first check if the user is logged in
    if 'student' in session:
        # log the student out
        session.pop('student', None)
        flash("Logged out!")
        return redirect(url_for("login"))
    
    elif 'teacher' in session:
        # log the teacher out
        session.pop('teacher', None)
        flash("Logged out!")
        return redirect(url_for("login"))
    
    else:
        # user is not logged in
        flash("You are not logged in!")
        return redirect(url_for("login"))

# route for the student view
@app.route("/student")
@app.route("/s")
def student():
    # first check if the student is logged in
    if 'student' in session:
        # if logged in, display the student's info
        return render_template("student.html", student=student)
    
    else:
        # user is not logged in -> login page
        flash("You are not logged in!")
        return redirect(url_for("login"))


# route for the teacher view
@app.route("/teacher")
@app.route("/t")
def teacher():
    # first check if the teacher is logged in
    if 'teacher' in session:
        # if logged in, display the table of students
        return render_template("teacher.html", student=Student.query.all())
    
    else:
        # user is not logged in -> login page
        flash("You are not logged in!")
        return redirect(url_for("login"))

# run the app
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)