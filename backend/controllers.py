from flask import Flask,redirect,request, render_template
from flask import current_app as app

@app.route('/')
def home():
  return redirect('/userlogin')

@app.route('/userlogin', methods = ['GET', 'POST'])
def userlogin():
  if request.method=='POST':
    return redirect('/user')
  return render_template('login.html')

@app.route('/user/summary')
def view_summary():
  return render_template('customer-summary.html')

@app.route('/user')
def user_dash():
  return render_template('customer-dash.html')

@app.route('/register')
def register():
  return render_template('customer-signup.html')

@app.route('/register/pro')
def registerpro():
  return render_template('prof-signup.html')