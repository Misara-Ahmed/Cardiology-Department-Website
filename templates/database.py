import mysql.connector
#
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="misara2468",
  database="project"
)
#
mycursor = mydb.cursor()
# mycursor.execute("CREATE DATABASE project")
#mycursor.execute("CREATE TABLE mydatabase (user_name VARCHAR(255),email VARCHAR(255) UNIQUE,password VARCHAR(255) UNIQUE,ssn INT UNIQUE,address VARCHAR(255),id INT UNIQUE,PRIMARY KEY (ssn) )")
mycursor.execute("CREATE TABLE patient_records (`patient_id` int,`file_name` varchar(255) COLLATE utf8_unicode_ci ,`uploaded_on` datetime ,`report` VARCHAR(255))")
# for x in mycursor:
#       print(x)