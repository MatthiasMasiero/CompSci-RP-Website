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

# TODO: add a show password button to the password column in teacher view

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
                # flash("Logged in!")
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
            email_in = request.form["email"].lower()

            # make sure the email does not already exist in the database
            emails_found = Student.query.filter_by(email=email_in).first()
            if emails_found:
                flash("Email already exists!")
                return redirect(url_for("register"))

            # create a new student object
            new_student = Student(name_in, int(period_in), email_in)

            # add the new student to the database
            db.session.add(new_student)
            db.session.commit()
            print('added to database')

            # send the new student's password to their email
            sendEmail(reciever_email=email_in, user_password=new_student.password, forgot_password=False)


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
@app.route("/teacher", methods=["POST", "GET"])
@app.route("/t", methods=["POST", "GET"])
def teacher():
    # first check if the teacher is logged in
    if 'teacher' in session:
        # if logged in, first check if the save button was pressed
        if request.method == "POST":
            users = []
            for i in range(len(Student.query.all())):
                str_id = "studentid" + str(i)
                str_name = "studentname" + str(i)
                str_period = "studentperiod" + str(i)
                str_email = "studentemail" + str(i)
                str_password = "studentpassword" + str(i)
                str_rp = "studentrp" + str(i)


                id_input = request.form[str_id]


                name_input = request.form[str_name]


                try:
                    period_input = int(request.form[str_period])
                except:
                    # someone put an "e" in the period input (we don't know how to prevent them from doing it)
                    flash(f"Please enter a valid period number for {name_input} (id: {id_input})")
                    return redirect(url_for("teacher"))
                
                # make sure period is a number between 1 and 8, inclusive
                if period_input < 1 or period_input > 8:
                    flash(f"Please enter a valid period number for {name_input} (id: {id_input})")
                    return redirect(url_for("teacher"))
                

                email_input = request.form[str_email]

                # first check if the email has been changed/edited
                if email_input != Student.query.filter_by(_id=id_input).first().email:
                    # make sure email is unique
                    emails_found = Student.query.filter_by(email=email_input).first()
                    if emails_found and emails_found._id != id_input: # also making sure the matching email is not the same student
                        flash(f"The email you're trying to change for {name_input} (id: {id_input}) is already taken by {emails_found.name} (id: {emails_found._id})")
                        return redirect(url_for("teacher"))
                    
                    # make sure email is valid
                    # for now, just checking if it's empty
                    if email_input == "":
                        flash(f"Please enter a valid email for {name_input} (id: {id_input})")
                        return redirect(url_for("teacher"))
                    

                password_input = request.form[str_password]
                # LOGIC FOR VALIDATING NEW PASSWORD:
                # 1. check if the password has been changed/edited
                if password_input != Student.query.filter_by(_id=id_input).first().password:
                # 2. make sure password is made up of only numbers
                    if not password_input.isdigit():
                        flash(f"Please enter a valid password for {name_input} (id: {id_input})")
                        return redirect(url_for("teacher"))
                # 3. remove leading zeroes
                    password_input = str(int(password_input))
                # 4. make sure password is 6 digits or less
                    if len(password_input) > 6:
                        flash(f"Please enter a valid password for {name_input} (id: {id_input})")
                        return redirect(url_for("teacher"))
                # 4a. if it's less than 6 digits, add leading zeroes
                    if len(password_input) < 6:
                        password_input = password_input.zfill(6)
                # 5. make sure password is unique (doesn't already belong to another student)
                    password_found = Student.query.filter_by(password=password_input).first()
                    if password_found and password_found._id != id_input: # also making sure the matching password is not the same student
                        flash(f"The password you're trying to change for {name_input} (id: {id_input}) is already taken by {password_found.name} (id: {password_found._id})")
                        return redirect(url_for("teacher"))

                try:
                    rp_input = int(request.form[str_rp])
                except:
                    # someone put an "e" in the rp input (we don't know how to prevent them from doing it)
                    flash(f"Please enter a valid number of RP for {name_input} (id: {id_input})")
                    return redirect(url_for("teacher"))


                users.append([id_input, name_input, period_input, email_input, password_input, rp_input])
            

            # update the database
            for i in range(len(users)):
                # using the id for the filter because that can't be changed
                found_user = Student.query.filter_by(_id=users[i][0]).first()

                # IF YOU MAKE ALL TABLE CELLS INTO INPUTS, UNCOMMENT THIS
                found_user.name = users[i][1]
                found_user.period = users[i][2]
                found_user.email = users[i][3]
                found_user.password = users[i][4]
                found_user.rp = users[i][5]


                db.session.commit()

            flash("Saved!")
            return redirect(url_for("teacher"))

        # display the table of students
        # sort the students by period, then name when you pass it to the html
        return render_template("teacher.html", students=Student.query.order_by(Student.period, Student.name).all())

    else:
        # user is not logged in -> login page
        flash("You are not logged in!")
        return redirect(url_for("login"))
    
@app.route("/forgotpassword", methods=["GET", "POST"])
@app.route("/forgot", methods=["GET", "POST"])
def forgotpassword():
    if request.method == "POST":
        # get the email from the form
        email_in = request.form["email"]

        # make sure the email exists in the database
        user_found = Student.query.filter_by(email=email_in).first()
        if user_found:
            # send the user an email containing their password
            sendEmail(reciever_email=email_in, user_password=user_found.password, forgot_password=True)
            flash("An email containing your password has been sent to you!")
            return redirect(url_for("login"))
        else:
            flash("The email you entered is not registered!")
            return redirect(url_for("forgotpassword"))

    else:
        return render_template("forgotpassword.html")
    
# FOR DEVELOPMENT PURPOSES ONLY, DELETE/COMMENT THESE IN PRODUCTION

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
    return render_template("student.html", student=Student.query.first())




# run the app
if __name__ == "__main__":
    with app.app_context():
        print('Creating Database...')
        # TODO: Uncomment this line in production
        db.drop_all()
        db.create_all()
        # TODO: Comment this loop in production
        for i in range(3):
            add_student()
    app.run(debug=True)