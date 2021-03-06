from flask import Flask, request, render_template, session, url_for, redirect
from flask import request
from flask import Blueprint
import pymysql.cursors
from friends import friends_blueprint
from content import content_blueprint
from medialib import media_blueprint
from tag import tags_blueprint

import helpers
import sys
if sys.version_info[0] >= 3:
	import urllib.parse
else:
	import urllib

app = Flask(__name__)
app.register_blueprint(friends_blueprint)
app.register_blueprint(content_blueprint)
app.register_blueprint(media_blueprint)
app.register_blueprint(tags_blueprint)

# this is for pulling the port and database password from environment variables
import os

# Configure MySQL
conn = pymysql.connect(host='localhost',
                      port= int(os.environ['DB_PORT']), #get the port from an env var
                      user='root',
                      password=os.environ['DB_PASS'], #get the pswd from an env var
                      db='dispatch',
                      charset='latin1',
                      cursorclass=pymysql.cursors.DictCursor)

@app.route('/')
def login(error = None):
	if (error == None):
		return render_template('login.html')
	else:
		return render_template('login.html', error=error)
		
@app.route('/home/friendgroups', methods=['GET'])
def friendgroups():
	if (helpers.checkSess()):
		return redirect(url_for('login'))
	else:
		username = session['username']

		# Gets a list of all the groups the user is a part of/is the admin of.
		cursor = conn.cursor()
		query = 'SELECT DISTINCT group_name, username_creator 			\
						FROM member 									\
						WHERE username = %s OR username_creator = %s'

		cursor.execute(query, (username, username))
		groups = cursor.fetchall()

		cursor.close()

		return render_template('friendgroups.html', groups=groups)

@app.route('/logout')
def logout():
	#clear session variables
	session['username'] = ""
	session['fname'] = ""
	session['lname'] = ""
	session['color'] = ""
	return render_template('login.html', error="You have successfully logged out")


@app.route('/home')
def home():
	if (helpers.checkSess()):
		return redirect(url_for('login'))
	else:
		return render_template('home.html')


@app.route('/home/settings')
def setting():
	if (helpers.checkSess()):
		return redirect(url_for('login'))
	else:
		return render_template('settings.html', color=session['color'])


@app.route('/changecolor', methods=['GET', 'POST'])
def changecolor():
	col = request.args.get("favcolor")
	print(col)

	session['color'] = col

	cursor = conn.cursor()
	query = 'UPDATE person SET color = %s WHERE username = %s'
	cursor.execute(query, (session['color'], session['username']))
	conn.commit()

	return redirect(url_for('setting'))


@app.route('/settings/changepass')
def changepass():
	if (helpers.checkSess()):
		return redirect(url_for('login'))
	else:
		return render_template('changepass.html')


@app.route('/changePassAuth', methods=['GET', 'POST'])
def changepassAuth():
	currpass = request.form['current_password']
	newpass = request.form['new_password']
	confirmpass = request.form['confirm_password']

	current_password_digest = helpers.md5(currpass)

	cursor = conn.cursor()
	query = 'SELECT * FROM person WHERE username = %s AND password = %s'
	cursor.execute(query, (session['username'], current_password_digest))

	data = cursor.fetchone()
	cursor.close()

	if (data):
		if (newpass != confirmpass):
			error = "Passwords Do Not Match"
			return render_template('changepass.html', error=error)
		else:
			new_password_digest = helpers.md5(newpass)
			confirm_password_digest = helpers.md5(confirmpass)

			cursor = conn.cursor()
			query = 'UPDATE person SET password = %s WHERE username = %s'
			cursor.execute(query, (new_password_digest, session['username']))
			conn.commit()

			query = 'SELECT * FROM person WHERE username = %s AND password = %s'
			cursor.execute(query, (session['username'], new_password_digest))

			data1 = cursor.fetchone()
			cursor.close()
			return redirect(url_for('setting'))
	else:
		error = "Incorrect Password"
		print(error)
		return render_template('changepass.html', error=error)
	
@app.route('/home/profile',methods=['GET'])
def profile():
	username = session['username']
	cursor = conn.cursor()
	conn.commit()
	
	query = 'SELECT username, color, url \
			 FROM person JOIN ImageContent ON ImageContent.id = person.profilePic  \
			 WHERE username = %s'
	cursor.execute(query, session['username'])
	profs = cursor.fetchall()
	profs = helpers.unquote(profs)
	cursor.close()
	return render_template('profile.html',profs=profs)


@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
	username = request.form['username']
	password = request.form['password']

	password_digest = helpers.md5(password)

	cursor = conn.cursor()
	query = 'SELECT * FROM person WHERE username = %s AND password = %s'
	cursor.execute(query, (username, password_digest))

	data = cursor.fetchone()
	print(data)
	cursor.close()

	if(data):
		session['username'] = username
		session['fname'] = data['first_name']
		session['lname'] = data['last_name']
		session['color'] = data['color']     # color is in the person table now
		return redirect(url_for('home'))
	else:
		error = "Invalid Username or Password"
		return render_template('login.html', error=error)


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/registerAuth', methods=['GET', 'POST'])
def registerAuth():
	# get user input from form
	username = request.form['username']
	password = request.form['password']
	fname = request.form['fname']
	lname = request.form['lname']

	# hash the password
	password_digest = helpers.md5(password)

	# connonect to db and insert new user
	cursor = conn.cursor()
	query = 'SELECT * FROM person WHERE username = %s'
	cursor.execute(query, (username))
	data = cursor.fetchone()
	if(data):
		return render_template('register.html', error="Username already taken.")

	query = 'INSERT INTO person VALUES (%s, %s, %s, %s, %s, 1)'
	cursor.execute(query, (username, password_digest, fname, lname, '#ea4c88'))
	data = cursor.fetchone()

	# commit changes and close connetion
	conn.commit()
	cursor.close()
	session['username'] = username
	session['fname'] = fname
	session['lname'] = lname
	session['color'] = '#ea4c88'
	return redirect(url_for('home'))


@app.route('/home/friendgroups/addfriendgroup')
def addFriendGroup():
	return render_template('addfriendgroup.html')


@app.route('/home/friendgroups/addfriendgroup/addtodatabase', methods=['GET', 'POST'])
def addFriendGroupAuth():
	cursor = conn.cursor()

	groupName = request.form['group_name']
	groupDescription = request.form['group_description']
	username = session['username']

	query = 'SELECT username, group_name FROM friendgroup WHERE username = %s AND group_name = %s'
	cursor.execute(query, (username, groupName))
	data = cursor.fetchone()
	if (data):
		return render_template('addfriendgroup.html', error="You already own a FriendGroup called " + groupName)
	else:
		query = 'INSERT INTO friendgroup VALUES(%s, %s, %s)'
		cursor.execute(query, (groupName, username, groupDescription))
		query = 'INSERT INTO member VALUES(%s, %s, %s)'
		cursor.execute(query, (username, groupName, username))
		conn.commit()
		return redirect(url_for('friendgroups'))

@app.route('/home/friendgroups/addMember')
def addMembersToGroup():
	username = session['username']
	groupName = request.args.get('groupSelected')
	groupCreator = session['username']
	cursor = conn.cursor()

	# Finding friends who you sent a friend request to. 
	query = 'SELECT first_name, last_name, username FROM friends JOIN person ON friends.friend_receive_username = person.username WHERE accepted_request = TRUE AND friend_send_username = %s AND username NOT IN (SELECT username FROM member WHERE group_name = %s AND username_creator = %s)'
	cursor.execute(query, (username, groupName, groupCreator))
	requestSendFriendsNotMembers = cursor.fetchall()

	# Finding friends who you received a friend request from. 
	query = 'SELECT first_name, last_name, username FROM friends JOIN person ON friends.friend_send_username = person.username WHERE accepted_request = TRUE AND friend_receive_username = %s AND username NOT IN (SELECT username FROM member WHERE group_name = %s AND username_creator = %s)'
	cursor.execute(query, (username, groupName, groupCreator))
	requestReceiveFriendsNotMembers = cursor.fetchall()
	cursor.close()

	notGroupMembers = []
	for friend in requestReceiveFriendsNotMembers:
		notGroupMembers.append(friend)
	for friend in requestSendFriendsNotMembers:
		notGroupMembers.append(friend)

	return render_template('addgroupmember.html', group_name = groupName, nonmembers=notGroupMembers )

@app.route('/home/friendgroups/addMember/addMemberAuth')
def addMembersAuth(): 
	addingUsername = request.args.get('adding')
	toGroup = request.args.get('to')

	username = session['username']
	cursor = conn.cursor()

	# Finding friends who you sent a friend request to. 
	query = 'INSERT INTO member VALUES (%s, %s, %s)'
	cursor.execute(query, (addingUsername, toGroup, username))
	conn.commit()
	cursor.close()

	return redirect(url_for('.addMembersToGroup', groupSelected=toGroup))

@app.route('/home/friendgroups/deleteMember')
def deleteMembersFromGroup():
	username = session['username']
	groupName = request.args.get('groupSelected')
	groupCreator = session['username']
	cursor = conn.cursor()

	# Finding friends who you sent a friend request to. 
	query = 'SELECT first_name, last_name, username FROM friends JOIN person ON friends.friend_receive_username = person.username WHERE accepted_request = TRUE AND friend_send_username = %s AND username IN (SELECT username FROM member WHERE group_name = %s AND username_creator = %s)'
	cursor.execute(query, (username, groupName, groupCreator))
	requestSendFriendsMembers = cursor.fetchall()

	# Finding friends who you received a friend request from. 
	query = 'SELECT first_name, last_name, username FROM friends JOIN person ON friends.friend_send_username = person.username WHERE accepted_request = TRUE AND friend_receive_username = %s AND username IN (SELECT username FROM member WHERE group_name = %s AND username_creator = %s)'
	cursor.execute(query, (username, groupName, groupCreator))
	requestReceiveFriendsMembers = cursor.fetchall()
	cursor.close()

	groupMembers = []
	for friend in requestReceiveFriendsMembers:
		groupMembers.append(friend)
	for friend in requestSendFriendsMembers:
		groupMembers.append(friend)

	return render_template('deletegroupmember.html', group_name = groupName, members=groupMembers )

@app.route('/home/friendgroups/deleteMember/deleteMemberAuth')
def deleteMembersAuth(): 
	deletingUsername = request.args.get('deleting')
	fromGroup = request.args.get('from')

	username = session['username']
	cursor = conn.cursor()

	# Finding friends who you sent a friend request to. 
	query = 'DELETE FROM member WHERE username = %s AND group_name = %s AND username_creator = %s'
	cursor.execute(query, (deletingUsername, fromGroup, username))
	conn.commit()
	cursor.close()

	return redirect(url_for('.deleteMembersFromGroup', groupSelected=fromGroup))

@app.route('/home/friendgroups/leaveGroup')
def leaveGroup(): 
	username_creator = request.args.get('username_creator')
	fromGroup = request.args.get('groupSelected')

	leavingUsername = session['username']
	cursor = conn.cursor()

	# Finding friends who you sent a friend request to. 
	query = 'DELETE FROM member WHERE username = %s AND group_name = %s AND username_creator = %s'
	cursor.execute(query, (leavingUsername, fromGroup, username_creator))
	conn.commit()
	cursor.close()

	return redirect(url_for('.friendgroups'))

@app.route('/settings/deleteAccount')
def deleteAccount(): 
	username = session['username']
	cursor = conn.cursor()

	query = 'DELETE FROM person WHERE username = %s'
	cursor.execute(query, (username))
	conn.commit()
	cursor.close()

	session['username'] = ""
	session['fname'] = ""
	session['lname'] = ""
	session['color'] = ""

	return redirect(url_for('.login', error='Your account has been successfully Dispatched.'))


app.secret_key = os.urandom(24)
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask 
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug=True)
app.run()
