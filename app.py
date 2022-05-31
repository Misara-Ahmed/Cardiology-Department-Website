from flask import Flask, render_template, request, redirect, url_for, session,flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import mysql.connector


##################################### Connecting to the database ####################################################
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="misara2468",
  database="project"
)
mycursor = mydb.cursor()

##################################### Defining the Program ####################################################  
app = Flask(__name__)
mysql = MySQL(app)
  
##################################### The Main Page ####################################################
@app.route('/')
def main():
    return render_template('home.html')

##################################### The Home Page ####################################################
@app.route('/home')
def home():
    return render_template('home.html')    

##################################### The Login Page ####################################################
@app.route("/login", methods =['GET', 'POST'])
def login():
    if request.method == 'POST' and 'id' in request.form and 'password' in request.form:
        idd = request.form['id']
        password = request.form['password']
        #print(type(idd))
        #print(idd[0])
        if (idd[0] == str(3)):
            mycursor.execute("SELECT id,password FROM patient")
            account = mycursor.fetchall()
            for x in account:
                if (str(x[0]) == idd and x[1] == password):
                    #print("TRUE")
                    return redirect(url_for("patient"))
            # return render_template("login.html")
        elif (idd[0] == str(2)):
            mycursor.execute("SELECT id,password FROM doctor")
            account = mycursor.fetchall()
            for x in account:
                if (str(x[0]) == idd and x[1] == password):
                    #print("TRUE")
                    return redirect(url_for("doctor"))
            # return render_template("login.html")
        elif (idd[0] == str(1)):
            #print("True")
            mycursor.execute("SELECT id,password FROM admin")
            account = mycursor.fetchall()
            #print(account)
            for x in account:
                if (str(x[0]) == idd and x[1] == password):
                    #print("TRUE")
                    return redirect(url_for("admin"))
        print("False")
    else:
      return render_template('login.html')

# if check_password_hash(user.password, password):
#                 flash('Logged in successfully!', category='success')
#                 login_user(user, remember=True)
#                 return redirect(url_for('views.home'))
#             else:
#                 flash('Incorrect password, try again.', category='error')
#         else:
#             flash('Email does not exist.', category='error')

##################################### The Register Page ####################################################    
@app.route('/register', methods =['GET', 'POST'])
def register():
    if request.method == 'POST' and 'username' in request.form and 'email' in request.form  and 'password' in request.form and 'ssn' in request.form and 'address' in request.form  and 'id' in request.form:
        user_name = request.form['username']
        email = request.form['email']
        password = request.form['password']
        ssn = request.form['ssn']
        address = request.form['address']
        id= request.form['id']
        # Conditions on entering the attributes in the database
        if len(email) < 2:
            flash('Email must be greater than 4 characters.', category='error')
        elif len(user_name) < 2:
            flash('Username must be greater than 2 character.', category='error')
        elif len(password) < 4:
            flash('Password must be at least 4 characters.', category='error')
        elif len(address) < 2:
            flash('Address must be greater than 2 character.', category='error')       
        else:
            # if all inputs are right -> start creating the account    
            sql = "INSERT INTO admin (user_name,email,password,ssn,address,id) VALUES (%s, %s, %s,%s,%s,%s)"
            # Add new admin
            val = (user_name,email,password,ssn,address,id)
            mycursor.execute(sql, val)
            # commit the changes in database
            mydb.commit()
            #flash('Account successfully created', category='success')
    return render_template('register.html')


##################################### The Admin Page ####################################################
@app.route('/admin', methods=['GET','POST'])
def admin():
    mycursor.execute("SELECT * FROM doctor")
    row_headers=[x[0] for x in mycursor.description]
    doctor_result = mycursor.fetchall()
    doctor={
         'message':"data retrieved",
         'rec':doctor_result,
         'header':row_headers
      }
    mycursor.execute("SELECT * FROM patient")
    row_headers=[y[0] for y in mycursor.description]
    patient_result = mycursor.fetchall()
    patient={
         'message':"data retrieved",
         'rec':patient_result,
         'header':row_headers
      }
    return render_template("admin.html ",patient=patient_result,doctor=doctor_result)

### Add doctor Page ####       
@app.route('/add_doctor', methods =['GET', 'POST'])
def add_doctor():
    if request.method == 'POST' and 'username' in request.form and 'email' in request.form  and 'password' in request.form and 'ssn' in request.form and 'address' in request.form  and 'id' in request.form:
        user_name = request.form['username']
        email = request.form['email']
        password = request.form['password']
        ssn = request.form['ssn']
        address = request.form['address']
        id= request.form['id']
        sql = "INSERT INTO doctor (user_name,email,password,ssn,address,id) VALUES (%s, %s, %s,%s,%s,%s)"
        val = (user_name,email,password,ssn,address,id)
        mycursor.execute(sql, val)
        mydb.commit()
        return render_template('add_doctor.html')
    else:
        return render_template("add_doctor.html")
### Add Patient Page ###
@app.route('/add_patient', methods =['GET', 'POST'])
def add_patient():
    if request.method == 'POST' and 'username' in request.form and 'email' in request.form  and 'password' in request.form and 'ssn' in request.form and 'address' in request.form  and 'id' in request.form:
        user_name = request.form['username']
        email = request.form['email']
        password = request.form['password']
        ssn = request.form['ssn']
        address = request.form['address']
        id= request.form['id']
        sql = "INSERT INTO patient (user_name,email,password,ssn,address,id) VALUES (%s, %s, %s,%s,%s,%s)"
        val = (user_name,email,password,ssn,address,id)
        mycursor.execute(sql, val)
        mydb.commit()
        return render_template('add_patient.html')

    else:
        return render_template("add_patient.html")

########################################### Doctors Page ########################################################
@app.route( '/doctor' , methods=['GET','POST'])
def doctor():
    return render_template("doctor.html")


########################################### Patients Page ########################################################
@app.route( '/patient' , methods=['GET','POST'])
def patient():
    return render_template("patient.html")



########################################### Devices Page ########################################################
@app.route('/devices')
def devices():
    return render_template('devices.html')

########################################### About Page ########################################################
@app.route('/about')
def about():
    return render_template('about.html')

########################################### Contact us Page ########################################################
@app.route('/contactus')
def contact():

    return render_template('contactus.html')


####################################### Starting the website ##################################################33
if __name__ == '__main__':
    app.run(debug=True)