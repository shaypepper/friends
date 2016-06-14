from flask import Flask, render_template, request, redirect, flash, session
from mysqlconnection import MySQLConnector
app = Flask(__name__)
mysql = MySQLConnector(app,'dojo')

@app.route('/')
def index():
  friends = mysql.query_db("SELECT * FROM friends")
  print friends
  return render_template('index.html', all_friends=friends)

@app.route('/add')
def add_user():
  return render_template('edit.html',friend=None, page="add")

@app.route('/add',methods=['POST'])
def insert():
  data = {'name': request.form['name'], 'email': request.form['email']}
  query = "INSERT INTO friends (id, name, email, created_at) VALUES (DEFAULT, :name, :email, NOW())"
  mysql.query_db(query, data)
  return redirect('/')

@app.route('/show/<friend_id>')
def show(friend_id):
  query = "SELECT * FROM friends WHERE id = :id"
  data = {'id': friend_id}
  friend = mysql.query_db(query, data)
  return render_template('displayfriend.html', friend=friend[0])

@app.route('/update/<friend_id>')
def update(friend_id):
  query = "SELECT email, name, id FROM friends WHERE id = :friend_id"
  data = {'friend_id': friend_id}
  friend = mysql.query_db(query, data)[0]
  return render_template('edit.html', friend=friend, page="update")

@app.route('/update/<friend_id>',methods=['POST'])
def updated(friend_id):
  query = "UPDATE friends SET name = :name, email = :email WHERE id = :friend_id"
  data = {
    'name': request.form['name'], 
    'email': request.form['email'],
    'friend_id': friend_id
  }
  mysql.query_db(query,data)
  return redirect('/')

@app.route('/delete/<friend_id>')
def delete(friend_id):
  query = "DELETE FROM friends WHERE id = :friend_id"
  data = {
    'friend_id': friend_id
  }
  mysql.query_db(query, data)
  return redirect('/')



##debug
app.run(debug=True)