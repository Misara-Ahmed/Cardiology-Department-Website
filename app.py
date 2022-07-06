##################################### Cardiovascular Hospital Departement ###############################
# TEAM:9 
########## TEAM MEMBERS: ########## 
# Rahma AbdEkhader        # Arwa Esam              # Misara Ahmed
# Sama Mostafa            # Yousr Hejy             # Doha Eid
##########################################################################################################
from flask import Flask, render_template, request, redirect, url_for, session ,flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import mysql.connector
from functools import wraps
from werkzeug.utils import secure_filename, send_from_directory
import os
from datetime import datetime

################################## Authorization Conditions ######################################################
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        # if logged in -> Acess the Pages
        # if not logged in -> return to the login Page
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash('Not logged in!',category='error')   
            return redirect(url_for('login'))    
    return wrap   

##################################### Connecting to the database ####################################################
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="root_123_456_789",
  database="project"
)
mycursor = mydb.cursor()

##################################### Defining the Program ####################################################  
app = Flask(__name__)
app.secret_key = "super secret key"
mysql = MySQL(app)
# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"

########################################################################################################################
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/upload", methods=["POST", "GET"])
def upload():
    #cursor = mysql.connection.cursor()
    #cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    now = datetime.now()
    if request.method == 'POST' and 'patient_id' in request.form:
        patient_id = request.form['patient_id']
        files = request.files.getlist('files[]')
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                full_filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                mycursor.execute("INSERT INTO patient_records (patient_id, file_name, uploaded_on) VALUES (%s, %s, %s)", [patient_id, filename, now])
                mydb.commit()
                mycursor.execute("SELECT file_name FROM patient_records ")
                img_files= mycursor.fetchall()
                flash('File(s) successfully uploaded')
                return render_template("index.html")
    else:
        return render_template('index.html')
##################################### View the Records ###########################################################
@app.route("/view_rec", methods=["POST", "GET"])
def view_rec():
    if request.method == 'GET':
        pat_id = session['p_id']
        mycursor.execute("SELECT patient_id FROM patient_records")
        ids = mycursor.fetchall()
        for x in ids:
            if ( x[0] == int(pat_id) ):
                mycursor.execute("SELECT * FROM patient_records WHERE patient_id = %s", (pat_id,))
                record = mycursor.fetchone()
                mycursor.reset()
                full_filename = os.path.join(app.config['UPLOAD_FOLDER'], record[1] )
                return render_template("display_img.html", image=full_filename)
        return render_template("display_img.html")
##############################################################################################################

########################################### The Main Page ####################################################
@app.route('/')
def main():
    return render_template('home.html')

##################################### The Home Page ####################################################
@app.route('/home')
def home():
    return render_template('home.html')    

####################################### The Register Page ####################################################    
@app.route('/register', methods =['GET', 'POST'])
def register():
    # Registration Fields: user_name, email, password, ssn, address, id
    if request.method == 'POST' and 'username' in request.form and 'email' in request.form  and 'password' in request.form and 'ssn' in request.form and 'address' in request.form  and 'id' in request.form:
        user_name = request.form['username']
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']
        salary = request.form['salary']
        bdate = request.form['bdate']
        ssn = request.form['ssn']
        address = request.form['address']
        id= request.form['id']
        # Conditions on entering the attributes in the database
        # Conditions on entering the attributes in the database
        sql = 'SELECT * FROM admin WHERE email = %s OR password = %s OR ssn= %s OR id =%s'
        val = (email,password,ssn,id)
        mycursor.execute(sql, val)
         # Fetch user's record
        account = mycursor.fetchone()
        mycursor.reset();
         # If account exists show error and validation checks
        if account:
            flash('one of the fields duplicated!',category='error')
            return render_template('register.html')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Invalid email address!',category='error')
            return render_template('register.html')
        elif not email or not password or not id or not ssn:
            flash('Fill out the Registration Form!')
            return render_template('register.html')
        elif len(email) < 2:
            flash('Email must be greater than 4 characters.', category='error')
            return render_template('register.html')
        elif len(user_name) < 2:
            flash('Username must be greater than 2 character.', category='error')
            return render_template('register.html')
        elif len(password) < 4:
            flash('Password must be at least 4 characters.', category='error')
            return render_template('register.html')
        elif len(phone) < 11:
            flash('Phone is not correct', category='error')
            return render_template('register.html')
        elif len(salary) < 3:
            flash('Salary is not correct', category='error')
            return render_template('register.html')
        elif len(bdate) < 6:
            flash('Birthdate is not correct', category='error')
            return render_template('register.html')
        elif len(address) < 2:
            flash('Address must be greater than 2 character.', category='error')
            return render_template('register.html')
       
        else:
           # if all condition of input fiels are true -> store the new account in the database
           sql = "INSERT INTO admin (user_name,email,password,phone,salary,bdate,ssn,address,id) VALUES (%s, %s,%s ,%s,%s, %s,%s,%s,%s)"
           val = (user_name,email,password,phone,salary,bdate,ssn,address,id)
           mycursor.execute(sql, val)
           mydb.commit()
           flash('Account successfully created', category='success')
    return render_template('register.html')

##################################### The Login Page ####################################################
@app.route("/login", methods =['GET', 'POST']) 
def login():
    if request.method == 'POST' and 'id' in request.form and 'password' in request.form:
        # enter the required fields in login form
        idd = request.form['id']
        password = request.form['password']
        if 'logged_in' in session:
         session.clear()
         flash("Logout First")
         return render_template("login.html") 
        if (idd[0] == str(3)):
         sql = 'SELECT * FROM patient WHERE id = %s AND password = %s'
         val = (idd, password)
         mycursor.execute(sql, val)
      # Fetch user's record
         account = mycursor.fetchone()
         mycursor.reset()
      # Check if account exists in the database
         if account:
         #create session data
             session['logged_in'] = True
             session['p_id'] = idd
             session['log'] = 'pat'
             flash("signed in successfully!")
             return redirect(url_for('patient'))
         else:
         # If account doesnt exist or email/password incorrect
           flash('Your email or password were incorrect')
           return render_template('login.html')
        # incase ID starts with 2 -> login as doctor
        elif (idd[0] == str(2)):
         sql = 'SELECT * FROM doctor WHERE id = %s AND password = %s'
         val = (idd, password)
         mycursor.execute(sql, val)
      # Fetch user's record
         account = mycursor.fetchone()
         mycursor.reset()
      #check if account exists in the database
         if account:
         #create session data
             session['logged_in'] = True
             session['d_id'] = idd
             session['dr_name'] = account[0]
             session['log'] = 'doc'
             flash("signed in successfully!")
             return redirect(url_for('doctor'))
         else:
         #if account doesnt exist or email/password incorrect
           flash('Your email or password were incorrect')
           return render_template('login.html')   
        # incase ID starts with 1 -> login as admin
        elif (idd[0] == str(1)):
         sql = 'SELECT * FROM admin WHERE id = %s AND password = %s'
         val = (idd, password)
         mycursor.execute(sql, val)
      # Fetch user's record
         account = mycursor.fetchone()
         mycursor.reset()
      #check if account exists in the database
         if account:
         # create session data
             session['logged_in'] = True
             session['a_id'] = idd
             session['log'] = 'adm'
             flash("signed in successfully!")
             return redirect(url_for('admin'))
         else:
         # if account doesnt exist or email/password incorrect
           flash('Your email or password were incorrect')
           return render_template('login.html')
        else:
            flash('Your email or password were incorrect')
            return render_template('login.html')
    else:
      return render_template('login.html')

####################################### Log Out ##########################################################
@app.route('/logout')
def logout():
    session.pop('logged_in',None)
    return redirect(url_for('home'))

##################################### The Admin Page ####################################################
@app.route('/admin', methods=['GET' , 'POST'])
@is_logged_in
def admin():
    return render_template("admin.html")

###################################### Edit Admin ######################################################
@app.route('/edit_admin' , methods = ['GET', 'POST'])
@is_logged_in
def edit_admin():
    mycursor = mydb.cursor()
    a_id = session["a_id"]
    if request.method == 'GET':
        mycursor.execute("SELECT * FROM admin WHERE id = %s", (a_id,))
        result = mycursor.fetchone()
        row_headers = [x[1] for x in mycursor.description]
        mycursor.reset()
        return render_template('edit_admin.html', result=result)
    elif request.method == 'POST':
        user_name = request.form['username']
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']
        address = request.form['address']
        mycursor.execute(
            "UPDATE admin SET user_name = %s, email = %s, password = %s,phone = %s, address = %s  WHERE id = %s",
            (user_name, email, password, phone ,address, a_id))
        mydb.commit()
        return redirect(url_for("admin"))

####################################### Add doctor Page #######################################################       
@app.route('/add_doctor', methods =['GET', 'POST'])
@is_logged_in
def add_doctor():
    # the Admin have axcess to add new doctor
    if request.method == 'POST' and 'username' in request.form and 'email' in request.form  and 'password' in request.form and 'ssn' in request.form and 'address' in request.form  and 'id' in request.form:
        user_name = request.form['username']
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']
        salary = request.form['salary']
        bdate = request.form['bdate']
        wday = request.form['wday']
        ssn = request.form['ssn']
        address = request.form['address']
        id= request.form['id']
        sql = 'SELECT * FROM doctor WHERE email = %s OR password = %s OR ssn= %s OR id =%s'
        val = (email,password,ssn,id,)
        mycursor.execute(sql, val)
         # Fetch user's record
        account = mycursor.fetchone()
        mycursor.reset()
         # If account exists show error and validation checks
        if account:
            flash('Account already exists!',category='error')
            return render_template('add_doctor.html')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Invalid email address!',category='error')
            return render_template('add_doctor.html')
        elif not email or not password or not id or not ssn or not ssn:
            flash('Fill out the Registration Form!')
            return render_template('add_doctor.html')
        elif len(email) < 2:
            flash('Email must be greater than 4 characters.', category='error')
            return render_template('add_doctor.html')
        elif len(user_name) < 2:
            flash('Username must be greater than 2 character.', category='error')
            return render_template('add_doctor.html')
        elif len(password) < 4:
            flash('Password must be at least 4 characters.', category='error')
            return render_template('add_doctor.html')
        elif len(address) < 2:
            flash('Address must be greater than 2 character.', category='error')
            return render_template('add_doctor.html') 
        else:
          sql = "INSERT INTO doctor (user_name,email,password,ssn,address,id,phone,salary,bdate,work_day) VALUES (%s,%s,%s,%s,%s, %s, %s,%s,%s,%s)"
          val = (user_name,email,password,ssn,address,id,phone,salary,bdate,wday)
          mycursor.execute(sql,val)
          mydb.commit()
          return render_template('add_doctor.html')
    else:
        return render_template("add_doctor.html")

############################################# Add Patient  ################################################################
@app.route('/add_patient', methods =['GET', 'POST'])
@is_logged_in
def add_patient():
    # the Admin have axcess to add new patient
    if request.method == 'POST' and 'username' in request.form and 'email' in request.form  and 'password' in request.form and 'ssn' in request.form and 'address' in request.form  and 'id' in request.form:
        user_name = request.form['username']
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']
        bdate = request.form['bdate']
        ssn = request.form['ssn']
        address = request.form['address']
        id= request.form['id']
        sql = 'SELECT * FROM patient WHERE email = %s OR password = %s OR ssn= %s OR id =%s'
        val = (email,password,ssn,id,)
        mycursor.execute(sql, val)
         # Fetch user's record
        account = mycursor.fetchone()
        mycursor.reset()
         # If account exists show error and validation checks
        if account:
            flash('Account already exists!',category='error')
            return render_template('add_patient.html')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Invalid email address!',category='error')
            return render_template('add_patient.html')
        elif not email or not password or not id or not ssn or not ssn:
            flash('Fill out the Registration Form!')
            return render_template('add_patient.html')
        elif len(email) < 2:
            flash('Email must be greater than 4 characters.', category='error')
            return render_template('add_patient.html')
        elif len(user_name) < 2:
            flash('Username must be greater than 2 character.', category='error')
            return render_template('add_patient.html')
        elif len(password) < 4:
            flash('Password must be at least 4 characters.', category='error')
            return render_template('add_patient.html')
        elif len(address) < 2:
            flash('Address must be greater than 2 character.', category='error')
            return render_template('add_patient.html')
        else:
            sql = "INSERT INTO patient (user_name,email,password,phone,bdate,ssn,address,id) VALUES (%s, %s, %s,%s,%s,%s,%s,%s)"
            val = (user_name,email,password,phone,bdate,ssn,address,id)
            mycursor.execute(sql, val)
            mydb.commit()
            return render_template('add_patient.html')
    else:
        return render_template("add_patient.html")
        
#############################################  Delete Doctor #################################################
@app.route('/delete_doctor' , methods = ['GET', 'POST'])
@is_logged_in
def delete_doctor():
    # the Admin have axcess to delete a doctor
    if request.method == 'POST' and 'id' in request.form :
        id = int(request.form['id'])
        mycursor.execute("DELETE FROM doctor WHERE id = %s",(id,))
        mydb.commit()
        return render_template('delete_doctor.html')
    else:
        return render_template('delete_doctor.html')

###########################################  Delete Patient ################################################
@app.route('/delete_patient' , methods = ['GET', 'POST'])
@is_logged_in
def delete_patient():
    # the Admin have axcess to delete a patient
    if request.method == 'POST' and 'id' in request.form :
        id = request.form['id']
        mycursor.execute("DELETE FROM patient WHERE id = %s", (id,))
        mydb.commit()
        return render_template('delete_patient.html')
    else :
        return render_template('delete_patient.html')

##############################################  Edit Patient #####################################################
@app.route('/edit_patient' , methods = ['GET', 'POST'])
@is_logged_in
def edit_patient():
    mycursor = mydb.cursor()
    p_id = session["p_id"]
    if request.method == 'GET':
        mycursor.execute("SELECT * FROM patient WHERE id = %s" , (p_id,))
        result = mycursor.fetchone()
        row_headers = [x[1] for x in mycursor.description]
        mycursor.reset()
        print(row_headers)
        print(result[0])
        return render_template('edit_patient.html',result=result)
    elif request.method =='POST':
        user_name = request.form['username']
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']
        address = request.form['address']
        mycursor.execute("UPDATE patient SET user_name = %s, email = %s, password = %s, phone= %s , address = %s  WHERE id = %s" ,
        (user_name, email, password,phone, address, p_id))
        mydb.commit()
        return render_template('patient.html')

########################################### Edit Doctor ######################################################
@app.route('/edit_doctor' , methods = ['GET', 'POST'])
@is_logged_in
def edit_doctor():
    mycursor = mydb.cursor()
    d_id = session["d_id"]
    if request.method == 'GET':
        mycursor.execute("SELECT * FROM doctor WHERE id = %s", (d_id,))
        result = mycursor.fetchone()
        row_headers = [x[1] for x in mycursor.description]
        mycursor.reset()
        return render_template('edit_doctor.html', result=result)
    elif request.method == 'POST':
        user_name = request.form['username']
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']
        wday = request.form['wday']
        address = request.form['address']
        mycursor.execute(
            "UPDATE doctor SET user_name = %s, email = %s, password = %s, phone= %s , work_day= %s , address = %s  WHERE id = %s",
            (user_name, email, password,phone,address, wday,d_id))
        mydb.commit()
        return render_template('doctor.html')

###########################################  Doctor Profile #########################################################
@app.route('/view_doc', methods=['GET','POST'])
@is_logged_in
def doctor_profile():
    mycursor = mydb.cursor()
    d_id = session["d_id"]
    if request.method == "GET":
        mycursor.execute("SELECT * FROM doctor WHERE id = %s", (d_id,))
        result = mycursor.fetchone()
        row_headers = [x[1] for x in mycursor.description]
        return render_template('profile.html', result=result)
    else :
        return render_template('doctor.html')

################################################ Patient profile ################################################
@app.route('/view_pat', methods=['GET','POST'])
@is_logged_in
def patient_profile():
    mycursor = mydb.cursor()
    p_id = session["p_id"]
    if request.method == "GET":
        mycursor.execute("SELECT * FROM patient WHERE id = %s" , (p_id,))
        result = mycursor.fetchone()
        row_headers = [x[1] for x in mycursor.description]
        return render_template('profile.html', result=result)
    else :
        return render_template('patient.html')

########################################### Admin profile ##################################################
@app.route('/view_adm', methods=['GET','POST'])
@is_logged_in
def admin_profile():
    mycursor = mydb.cursor()
    a_id = session["a_id"]
    if request.method == "GET":
        mycursor.execute("SELECT * FROM admin WHERE id = %s", (a_id,))
        result = mycursor.fetchone()
        row_headers = [x[1] for x in mycursor.description]
        return render_template('profile.html', result=result)
    else :
        return render_template('admin.html')        

########################################### Patient Appointment ########################################################
@app.route('/appointment', methods =['GET', 'POST'])
@is_logged_in
def appointment():
    if request.method == 'POST' and 'patient_name' in request.form and 'dr_name' in request.form  and 'id' in request.form and 'description' in request.form and 'date' in request.form :
        patient_name= request.form['patient_name']
        dr_name = request.form['dr_name']
        id= request.form['id']
        description = request.form['description']
        date= request.form['date']
        sql = 'SELECT * FROM appointment WHERE id = %s'
        val = (id,)
        mycursor.execute(sql, val)
         # Fetch user's record
        account = mycursor.fetchone()
        mycursor.reset()
         # If account exists show error and validation checks
        
        if account:
            flash('Appointment denied!',category='error')
            return render_template('appointment.html')
        elif not dr_name or not id or not id or not description or not date:
            flash('Fill out the Registration Form!')
            return render_template('appointment.html')
        else:
          sql = "INSERT INTO appointment(patient_name, dr_name,id,description,date) VALUES (%s, %s, %s,%s,%s)"
          val = (patient_name,dr_name,id,description,date)
          mycursor.execute(sql, val)
          mydb.commit()
          return render_template('appointment.html')
    else:
        return render_template("appointment.html")

########################################### Doctors Page ########################################################
@app.route( '/doctor', methods = ['GET', 'POST'])
@is_logged_in
def doctor():
    return render_template("doctor.html")

########################################### Patient Page ########################################################
@app.route( '/patient', methods = ['GET', 'POST'])
@is_logged_in
def patient():
    return render_template("patient.html")

########################################### Appointement ########################################################
@app.route('/appointment_table', methods=['GET','POST'])
@is_logged_in
def appointment_table():
    mycursor=mydb.cursor()
    patient_id= session["p_id"]
    if request.method == "GET":
       mycursor.execute("SELECT * FROM appointment WHERE id= %s ",(patient_id,))
       p_result=mycursor.fetchone()
       row_headers=[x[0] for x in mycursor.description]
       mycursor.reset()
    appointment={
         'message':"data retrieved",
         'rec':p_result,
         'header':row_headers
                   }
    return render_template("appointment_table.html ",appointment=p_result)

######################################### Table in Doctor #################################################
@app.route('/appointment_table2', methods=['GET','POST'])
@is_logged_in
def appointment_table2():
    mycursor=mydb.cursor()
    doctor_name= session["dr_name"]
    if request.method == "GET":
       mycursor.execute("SELECT * FROM appointment WHERE dr_name= %s ",(doctor_name,))
       d_result=mycursor.fetchall()
       row_headers=[x[0] for x in mycursor.description]
    d_appointment={
         'message':"data retrieved",
         'rec':d_result,
         'header':row_headers
                   }
    return render_template("appointment_table2.html ",appointment1=d_result)




########################################### Devices Page ########################################################
@app.route('/devices')
def devices():
    return render_template('devices.html')
########################################### veiwpat Page ########################################################
@app.route('/veiwpat')
@is_logged_in
def veiwpat():
    return render_template('veiwpat.html')

########################################### veiw doct Page ########################################################
@app.route('/veiwdoct')
@is_logged_in
def veiwdoct():
    return render_template('veiwdoct.html')
    
########################################### About Page ########################################################
@app.route('/about')
def about():
    return render_template('about.html')

########################################### View Page #######################################################
@app.route('/veiw')
@is_logged_in
def veiw():
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
    return render_template("veiw.html ",patient=patient_result,doctor=doctor_result)
   
########################################### contact us ########################################################
@app.route( '/contactus' , methods=['GET','POST'])
def contact():
    if request.method == 'POST' and 'user_name' in request.form and 'email' in request.form  and 'phone' in request.form and 'message' in request.form:
        user_name = request.form['user_name']
        email = request.form['email']
        phone = request.form['phone']
        message= request.form['message']
        # Enter the message into the database  
        sql = "INSERT INTO contact(user_name,email,phone,message) VALUES (%s, %s, %s,%s)"
        val = (user_name,email,phone,message)
        mycursor.execute(sql, val)
        # commit the changes in contact database
        mydb.commit()
    return render_template('contactus.html')

####################################### Starting the website ##################################################33
if __name__ == '__main__':
    app.run(debug=True)

