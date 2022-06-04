from flask import Flask, render_template, request, redirect, url_for, session ,flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import mysql.connector
from werkzeug.utils import secure_filename, send_from_directory
import os
from datetime import datetime


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
        # print(files)
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                full_filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                mycursor.execute("INSERT INTO patient_records (patient_id, file_name, uploaded_on) VALUES (%s, %s, %s)", [patient_id, filename, now])
                mydb.commit()
                mycursor.execute("SELECT file_name FROM patient_records ")
                img_files= mycursor.fetchall()
                #cur.close()
                flash('File(s) successfully uploaded')
                #return render_template("display_img.html", img_files=img_files)
                return render_template("index.html")
    else:
        return render_template('index.html')
###########################################################################################################
@app.route("/view_rec", methods=["POST", "GET"])
def view_rec():
    if request.method == 'GET':
        pat_id = session['p_id']
        mycursor.execute("SELECT patient_id FROM patient_records")
        ids = mycursor.fetchall()
        for x in ids:
            if ( x[0] == int(pat_id) ):
                print("yes")
                mycursor.execute("SELECT * FROM patient_records WHERE patient_id = %s", (pat_id,))
                record = mycursor.fetchone()
                #print(record)
                full_filename = os.path.join(app.config['UPLOAD_FOLDER'], record[1] )
                return render_template("display_img.html", image=full_filename)
        return render_template("display_img.html")
##############################################################################################################
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
        session.clear()
        idd = request.form['id']
        password = request.form['password']
        #print(type(idd))
        #print(idd[0])
        if (idd[0] == str(3)):
            session["p_id"] = idd
            session['log'] = 'pat'
            mycursor.execute("SELECT id,password FROM patient")
            account = mycursor.fetchall()
            for x in account:
                if (str(x[0]) == idd and x[1] == password):
                    #print("TRUE")
                    flash("Logged in successfuly")
                    return redirect(url_for("patient"))
            # return render_template("login.html")
        elif (idd[0] == str(2)):
            session["d_id"] = idd
            session['log'] = 'doc'
            mycursor.execute("SELECT id,password FROM doctor")
            account = mycursor.fetchall()
            for x in account:
                if (str(x[0]) == idd and x[1] == password):
                    #print("TRUE")
                    return redirect(url_for("doctor"))
            # return render_template("login.html")
        elif (idd[0] == str(1)):
            #print("True")
            session["a_id"] = idd
            session['log'] = 'adm'
            mycursor.execute("SELECT id,password FROM admin")
            account = mycursor.fetchall()
            #print(account)
            for x in account:
                if (str(x[0]) == idd and x[1] == password):
                    #print("TRUE")
                    flash("Logged in successfuly")
                    return redirect(url_for("admin"))
        #print("False")
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
        id = request.form['id']
        # Conditions on entering the attributes in the database
        if len(email) < 2:
            flash('Email must be greater than 4 characters.', category='error')
        elif len(user_name) < 2:
            flash('Username must be greater than 2 character.', category='error')
        elif len(password) < 4:
            flash('Password must be at least 4 characters.', category='error')
        elif len(address) < 2:
            flash('Address must be greater than 2 character.', category='error')       
        else: # if all inputs are right -> start creating the account
            if id[0] == str(2) : # Adding new doctor
                sql = "INSERT INTO doctor (user_name,email,password,ssn,address,id) VALUES (%s, %s, %s,%s,%s,%s)"
                val = (user_name,email,password,ssn,address,id)
                mycursor.execute(sql, val)
                mydb.commit() # commit the changes in database
                #flash('Dr Account successfully created', category='success')
                return render_template('register.html')
            elif id[0] == str(3) :  #Adding new patient
                sql = "INSERT INTO patient (user_name,email,password,ssn,address,id) VALUES (%s, %s, %s,%s,%s,%s)"
                val = (user_name,email,password,ssn,address,id)
                mycursor.execute(sql, val)
                mydb.commit() # commit the changes in database
                #flash('Patient Account successfully created', category='success')
                return render_template('register.html')
            else :
                #flash('Id is not correct', category='success')
                return render_template('register.html')
    else:
        return render_template('register.html')
##########################################################################################################
@app.route('/adveiw', methods=['GET','POST'])
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

##################################### The Admin Page ####################################################
@app.route('/admin', methods=['GET','POST'])
def admin():
   return render_template("admin.html")
# def admin():
#     mycursor.execute("SELECT * FROM doctor")
#     row_headers=[x[0] for x in mycursor.description]
#     doctor_result = mycursor.fetchall()
#     doctor={
#          'message':"data retrieved",
#          'rec':doctor_result,
#          'header':row_headers
#       }
#     mycursor.execute("SELECT * FROM patient")
#     row_headers=[y[0] for y in mycursor.description]
#     patient_result = mycursor.fetchall()
#     patient={
#          'message':"data retrieved",
#          'rec':patient_result,
#          'header':row_headers
#       }
#     return render_template("admin.html ",patient=patient_result,doctor=doctor_result)

########################################### Add doctor Page ###################################################
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
#############################################  Delete Doctor #################################################
@app.route('/delete_doctor' , methods = ['GET', 'POST'])
def delete_doctor():
    if request.method == 'POST' and 'id' in request.form :
        id = int(request.form['id'])
        mycursor.execute("DELETE FROM doctor WHERE id = %s",(id,))
        mydb.commit()
        return render_template('delete_doctor.html')

    else :
        return render_template('delete_doctor.html')
###########################################  Delete Patient ################################################
@app.route('/delete_patient' , methods = ['GET', 'POST'])
def delete_patient():
    if request.method == 'POST' and 'id' in request.form :
        id = request.form['id']
        mycursor.execute("DELETE FROM patient WHERE id = %s", (id,))
        mydb.commit()
        return render_template('delete_patient.html')

    else :
        return render_template('delete_patient.html')
##############################################  Edit Dr #####################################################
@app.route('/edit_patient' , methods = ['GET', 'POST'])
def edit_patient():
    mycursor = mydb.cursor()
    p_id = session["p_id"]
    if request.method == 'GET':
        mycursor.execute("SELECT * FROM patient WHERE id = %s" , (p_id,))
        result = mycursor.fetchone()
        row_headers = [x[1] for x in mycursor.description]
        #print(row_headers)
        #print(result[0])
        return render_template('edit_patient.html',result=result)
    elif request.method =='POST':
        user_name = request.form['username']
        email = request.form['email']
        password = request.form['password']
        #ssn = request.form['ssn']
        address = request.form['address']
        #id = request.form['id']
        mycursor.execute("UPDATE patient SET user_name = %s, email = %s, password = %s, address = %s  WHERE id = %s" ,
        (user_name, email, password, address, p_id))
        mydb.commit()
        return redirect(url_for("admin"))

########################################### Edit Doctor ######################################################

@app.route('/edit_doctor' , methods = ['GET', 'POST'])
def edit_doctor():
    mycursor = mydb.cursor()
    d_id = session["d_id"]
    if request.method == 'GET':
        mycursor.execute("SELECT * FROM doctor WHERE id = %s", (d_id,))
        result = mycursor.fetchone()
        row_headers = [x[1] for x in mycursor.description]
        #print(row_headers)
        # print(result[0])
        return render_template('edit_doctor.html', result=result)
    elif request.method == 'POST':
        user_name = request.form['username']
        email = request.form['email']
        password = request.form['password']
        # ssn = request.form['ssn']
        address = request.form['address']
        # id = request.form['id']
        mycursor.execute(
            "UPDATE doctor SET user_name = %s, email = %s, password = %s, address = %s  WHERE id = %s",
            (user_name, email, password, address, d_id))
        mydb.commit()
        return redirect(url_for("admin"))

###########################################  View Page #########################################################
@app.route('/view_doc', methods=['GET','POST'])
def doctor_profile():
    mycursor = mydb.cursor()
    d_id = session["d_id"]
    if request.method == "GET":
        mycursor.execute("SELECT * FROM doctor WHERE id = %s", (d_id,))
        result = mycursor.fetchone()
        row_headers = [x[1] for x in mycursor.description]
        return render_template('profile.html', result=result)

    else :
        return render_template('admin.html')
################################################ View
@app.route('/view_pat', methods=['GET','POST'])
def patient_profile():
    mycursor = mydb.cursor()
    p_id = session["p_id"]
    if request.method == "GET":
        mycursor.execute("SELECT * FROM patient WHERE id = %s", (p_id,))
        result = mycursor.fetchone()
        row_headers = [x[1] for x in mycursor.description]
        return render_template('profile.html', result=result)

    else :
        return render_template('admin.html')
##############################################################
@app.route('/view_adm', methods=['GET','POST'])
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

##############################################################################################################################################################
# @app.route('/appointment', methods=['GET', 'POST'])
# def appointment():
#     if request.method == 'POST' and 'patient_name' in request.form and 'dr_name' in request.form and 'id' in request.form and 'description' in request.form and 'date' in request.form:
#         patient_name = request.form['patient_name']
#         dr_name = request.form['dr_name']
#         id = request.form['id']
#         description = request.form['description']
#         date = request.form['date']
#
#         sql = "INSERT INTO appointment(patient_name, dr_name,id,description,date) VALUES (%s, %s, %s,%s,%s)"
#         val = (patient_name, dr_name, id, description, date)
#         mycursor.execute(sql, val)
#         mydb.commit()
#         return render_template('appointment.html')
#
#     else:
#         return render_template("appointment.html")
################################################################################################################
@app.route('/appointment', methods =['GET', 'POST'])
def appointment():
    if request.method == 'POST' and 'patient_name' in request.form and 'dr_name' in request.form  and 'id' in request.form and 'description' in request.form and 'date' in request.form :
        patient_name= request.form['patient_name']
        dr_name = request.form['dr_name']
        id = request.form['id']
        description = request.form['description']
        date= request.form['date']
        mycursor.execute("SELECT user_name,id FROM patient")
        account=mycursor.fetchall()
        mycursor.execute("SELECT patient_name,id,date FROM appointment")
        account2=mycursor.fetchall()
        for y in account2:
                    print(y[0])
                    print(y[1])
                    print(y[2])
                    if(y[0]==patient_name or y[1]==int(id)):
                        print("YES")
                        flash("sorry :( you can not add another appointment.. ")
                        return redirect(url_for("appointment.html"))
                            #return render_template("appointment.html")
                    else:
                        if(y[2]==date):
                            flash("sorry :( this date is not allowed.. ")
                            return redirect(url_for("appointment"))
                            #return render_template("appointment.html")
                        else:
                            for x in account:
                                if(x[0]==patient_name):
                                    if(x[1]==int(id)):
                                        sql = "INSERT INTO appointment(patient_name, dr_name,id,description,date) VALUES (%s, %s, %s,%s,%s)"
                                        val = (patient_name,dr_name,id,description,date)
                                        mycursor.execute(sql, val)
                                        mydb.commit()
                                        return redirect(url_for("appointment"))
                                        #return render_template('appointment.html')
                                    else:
                                            flash("please enter the correct id")
                                            return redirect(url_for("appointment"))
                                            #return render_template('appointment.html')
                                else:
                                        flash("please enter the correct name")
                                        return redirect(url_for("appointment"))
                                        #return render_template ('appointment.html')
    else:
        #return redirect(url_for("appointment"))
        return render_template("appointment.html")

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