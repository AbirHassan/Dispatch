from flask import Flask, request, render_template, session, url_for, redirect
from flask import request
import pymysql.cursors
import hashlib
app = Flask(__name__)

#Configure MySQL
conn = pymysql.connect(host='localhost',
                      port=3306,
                      user='root',
                      password='',
                      db='dispatch',
                      charset='latin1',
                      cursorclass=pymysql.cursors.DictCursor)

@app.route('/')
def login():
    return render_template('login.html')

#page that appears when you log in
def home():
    return render_template('index.html')
	
@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
	username = request.form['username']
	password = request.form['password']
	print(password)
	
	#md5 hashes password user enters
	m = hashlib.md5()
	m.update(password)
	password = m.digest()
	print(password)
	
	cursor = conn.cursor()
	query = 'SELECT * FROM person WHERE username = %s AND password = %s'
	cursor.execute(query, (username, password))
	print(cursor.fetchone())
	data = cursor.fetchone()
	cursor.close()

	if(data):
		return render_template('index.html')
	else:
		error = "Invalid Login or Username"
		return render_template('login.html', error=error)

@app.route('/register')
def register(): 
    return render_template('register.html')

@app.route('/registerAuth', methods = ['GET', 'POST'])
def registerAuth():
	username = request.form['username']
	password = request.form['password']
	fname = request.form['First Name']
	lname = request.form['Last Name']
	
	m = hashlib.md5()
	m.update(password)
	password = m.digest()
	print(password)
	
	cursor = conn.cursor()
	query = 'INSERT INTO person VALUES (%s, %s, %s, %s)'
	cursor.execute(query, (username, password, fname, lname))
	data = cursor.fetchone()
	cursor.close()
	
	return render_template('login.html')
	#return "Welcome Home!"

app.run()

'''
#change this
app.secret_key = "qwertyuiop"
if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug=True)
'''