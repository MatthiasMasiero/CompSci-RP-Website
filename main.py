from flask import Flask, redirect, url_for, request, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
import random
# custom package import
from email_helper.send_mail import sendEmail

# create the flask app object
app = Flask(__name__)
# set the secret key for the session
app.secret_key = "hello"

# settings for sql database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# create the database object
db = SQLAlchemy(app)

teacherPassword = '314159'


class Student(db.Model):
    # create columns
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    period = db.Column(db.Integer())
    email = db.Column(db.String(100))
    password = db.Column(db.String(6))
    rp = db.Column(db.Integer())

    def __init__(self, name, period, email):
        self.name = name
        self.period = period
        self.email = email

        # password is initialized to a random 6-digit number
        random_password = random.randint(000000, 999999)

        # make sure the password is unique
        # get all the passwords from the database
        passwords = Student.query.with_entities(Student.password).all()
        # check if the random password is already in the database
        while str(random_password) in passwords:
            random_password = random.randint(000000, 999999)

        # add leading zeroes to the password if it's less than 6 digits
        random_password = str(random_password)
        while len(random_password) < 6:
            random_password = "0" + random_password

        # set the password
        self.password = random_password


        self.rp = 0

    def __repr__(self):
        return f"Name ({self.name}), Password ({self.password}), Points ({self.rp}), Email ({self.email}), Period ({self.period})\n"
    

# TODO: create the send_email method for registering students
def send_email(email, password):
    return None


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
            
            # prompt password again if it's not 6 digits
            if len(password) != 6:
                flash("Please enter a 6-digit number!")
                return redirect(url_for("login"))
            
            # check if the teacher is trying to log in
            if password == teacherPassword:
                # log the teacher in
                session['teacher'] = 'teacher'
                flash("Logged in!")
                return redirect(url_for("teacher"))
            
            # if password found, log the user in
            found_user = Student.query.filter_by(password=password).first()
            if found_user:
                # log the student in
                print('logging in student')
                session['student'] = found_user.name
                flash("Logged in!")
                return redirect(url_for("student"))
            
            # if password not found, display an error message
            else:
                flash("Password not found!")
                return redirect(url_for("login"))
        else:
            # user is not trying to log in -> display the login page
            return render_template("login.html")
    

# route for the register page
# *to be used only by students
@app.route("/signup", methods=["POST", "GET"])
@app.route("/register", methods=["POST", "GET"])
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
            session.permanent = True

            # user is trying to register

            # get the form data
            name_in = request.form["name"]
            period_in = request.form["period"]
            email_in = request.form["email"]

            # TODO: make sure the email does not already exist in the database

            # create a new student object
            new_student = Student(name_in, int(period_in), email_in)

            # add the new student to the database
            db.session.add(new_student)
            db.session.commit()
            print('added to database')

            # # TODO: send the new student's password to their email
            # send_email(email, new_student.password)

            # redirect to the student view
            try:
                sendEmail(reciever_email=email_in, user_password=new_student.password)
            except:
                print('email not sent')
            flash("Registered! Your password has been sent to your school email.")
            print('redirecting to login page')
            return redirect(url_for("login"))

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
    print('student view')
    # first check if the student is logged in
    if 'student' in session:
        # if logged in, display the student's info
        found_student = Student.query.filter_by(name=session['student']).first()
        return render_template("student.html", student=found_student, random_tail_length=random.randint(1, 10))
    
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
        return render_template("teacher.html", students=Student.query.all())
    
    else:
        # user is not logged in -> login page
        flash("You are not logged in!")
        return redirect(url_for("login"))
    
# FOR DEVELOPMENT PURPOSES ONLY, DELETE THESE IN PRODUCTION

# route for clearing the table
@app.route("/clear-table")
def clear_table():
    # clear the database
    db.drop_all()
    return "Table cleared!"

# route for adding a student to the table
@app.route("/add-student")
def add_student():
    # create a new student object
    new_student = Student('name', 7, '123@mail.com')

    # add the new student to the database
    db.session.add(new_student)
    db.session.commit()

    return "Student added!"

# route to see the student view without logging in
@app.route("/student-view")
def student_view():
    return render_template("student.html", student=Student.query.first(), random_tail_length=random.randint(1, 10))




# run the app
if __name__ == "__main__":
    with app.app_context():
        print('Creating Database...')
        db.drop_all()
        db.create_all()
    app.run(debug=True)