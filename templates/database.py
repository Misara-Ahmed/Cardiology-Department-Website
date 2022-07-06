import mysql.connector
#from numpy import insert

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="doha01152824065",
  database="project"
)

mycursor = mydb.cursor()
# mycursor.execute("CREATE DATABASE project")
# mycursor.execute("CREATE TABLE admin (user_name VARCHAR(255),email VARCHAR(255) UNIQUE,password VARCHAR(255) UNIQUE,ssn INT UNIQUE,address VARCHAR(255),id INT UNIQUE,PRIMARY KEY (ssn) )")
# mycursor.execute("CREATE TABLE doctor (user_name VARCHAR(255),email VARCHAR(255) UNIQUE,password VARCHAR(255) UNIQUE,ssn INT UNIQUE,address VARCHAR(255),id INT UNIQUE,PRIMARY KEY (ssn) )")
# mycursor.execute("CREATE TABLE patient (user_name VARCHAR(255),email VARCHAR(255) UNIQUE,password VARCHAR(255) UNIQUE,ssn INT UNIQUE,address VARCHAR(255),id INT UNIQUE,PRIMARY KEY (ssn) )")
# mycursor.execute("CREATE TABLE if not exists appointment (patient_name VARCHAR(255),dr_name VARCHAR(255) ,id VARCHAR(255) UNIQUE ,description VARCHAR(255),date VARCHAR(255) UNIQUE,PRIMARY KEY (id) )")
# mycursor.execute("CREATE TABLE if not exists contact (user_name VARCHAR(255), email VARCHAR(255) UNIQUE, phone INT, message VARCHAR(255), PRIMARY KEY (email) )")
# mycursor.execute("CREATE TABLE patient_records (`patient_id` int,`file_name` varchar(255) COLLATE utf8_unicode_ci ,`uploaded_on` datetime ,`report` VARCHAR(255))")
# for x in mycursor:
#       print(x)
##################################################################################################################################################
# mycursor.execute("ALTER TABLE admin ADD  salary INT")
# mycursor.execute("ALTER TABLE admin ADD  bdate VARCHAR(255)")
# mycursor.execute("ALTER TABLE admin ADD  phone VARCHAR(255)")
# mycursor.execute("ALTER TABLE patient ADD  bdate VARCHAR(255)")
# mycursor.execute("ALTER TABLE patient ADD  phone INT")
# mycursor.execute("ALTER TABLE doctor ADD  salary INT")
# mycursor.execute("ALTER TABLE doctor ADD  bdate VARCHAR(255)")
# mycursor.execute("ALTER TABLE doctor ADD  phone VARCHAR(255)")
# mycursor.execute("ALTER TABLE doctor ADD  work_day VARCHAR(255)")