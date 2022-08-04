from crypt import methods
import email
from flask import Flask, render_template, request, redirect, request_started, url_for, flash
from flask import session as login_session
import pyrebase

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

config = {
  "apiKey": "AIzaSyCLlMevTWrTcPtGY7PVU9dRyZ1R_Qhs3cY",
  "authDomain": "myprojectnoway.firebaseapp.com",
  "projectId": "myprojectnoway",
  "storageBucket": "myprojectnoway.appspot.com",
  "messagingSenderId": "508677742215",
  "appId": "1:508677742215:web:2ee07564f9dcfb37556222",
  "measurementId": "G-T6LNK24JMJ",
  "databaseURL": "https://myprojectnoway-default-rtdb.firebaseio.com"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/signin', methods = ['GET', 'POST'])
def signin():
  error = ''
  if request.method == 'POST':
    email = request.form['email']
    password = request.form['password']
    try:
      login_session['user'] = auth.sign_in_with_email_and_password(email, password)
      return redirect(url_for('wall'))
    except:
      error = 'smth went wrong in signing in'
  return render_template('signinn.html')

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
  error = ''
  if request.method == 'POST':
    email = request.form['email']
    password = request.form['password']
    try:
      login_session['user'] = auth.create_user_with_email_and_password(email, password)
      user = {'email': email, 'password': password}
      db.child('Users').child(login_session['user']['localId']).set(user)

      return redirect(url_for('add_post'))
    except:
      error = 'smth went wrong in signing up'
  return render_template('signup.html')



@app.route('/profile')
def profile():
  return render_template('portfolio.html')

@app.route('/wall')
def wall():
  return render_template('wall.html')

@app.route('/add_post', methods = ['GET', 'POST'])
def add_post():
  error = ''
  if request.method == 'POST':
    try:
      post = {'question': request.form['question'], 'description': request.form['description']}
      db.child('Posts').push(post)
      return render_template('postsmth.html')
    except:
      error = 'sdfsdfsdf'

  return render_template('postsmth.html')

@app.route('/walldemo')
def walldemo():
  posts = db.child('Posts').get().val()
  return render_template('allpostsdemo.html', posts = posts)

if __name__ == '__main__':
    app.run(debug=True)