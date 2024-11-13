from flask import Flask,redirect,request, render_template
from flask import current_app as app
from .models import *
import datetime

@app.route('/')
def home():
  return redirect('/userlogin')

@app.route('/userlogin', methods = ['GET', 'POST'])
def userlogin():
  if request.method=='POST':
    u_name = request.form.get("u_name")
    pwd = request.form.get("pwd")
    user = Users.query.filter_by(username = u_name, password = pwd).first()
    if not user:
      return redirect('/userlogin')
    if user.role=='admin':
      return redirect('/admin')
    elif user.role=='professional':
      return redirect(f"user/prof/{user.user_id}")
    else:
      return redirect(f"user/customer/{user.user_id}")
    
  return render_template('login.html')







