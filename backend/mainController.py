from flask import Flask,redirect,request, render_template
from flask import current_app as app
from .models import *

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
      return render_template('login.html', key=1)
    if user.is_blocked:
      return render_template('login-denied.html')
    if user.role=='admin':
      return redirect('/admin')
    elif user.role=='professional':
      if not user.service_professional.profile_verified:
        return render_template('login.html', key=2)
      return redirect(f"user/prof/{user.user_id}")
    else:
      return redirect(f"user/customer/{user.user_id}")
    
  return render_template('login.html', key=0)







