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
      return redirect('/userlogin')
    if user.role=='admin':
      return redirect('/admin')
    elif user.role=='professional':
      return redirect(f"user/prof/{user.user_id}")
    else:
      return redirect(f"user/customer/{user.user_id}")
    
  return render_template('login.html')


@app.route('/user/customer/<int:user_id>')
def customer_dash(user_id):
  user = Users.query.filter_by(user_id = user_id).first()
  customer = Customers.query.filter_by(user_id = user_id).first()
  return render_template('customer-dash.html', customer = customer, user = user)

@app.route('/user/summary')
def view_summary():
  return render_template('customer-summary.html')

@app.route('/admin')
def admin_dash():
  return render_template('admin-dash.html')

@app.route('/user/prof/<int:user_id>')
def prof_dash():
  return render_template('prof-dash.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
  if request.method=='POST':
    print(request.form)
    name = request.form.get('name')
    email = request.form.get('email')
    print(email)
    phone = request.form.get('phone')
    u_name = request.form.get('u_name')
    pwd = request.form.get('pwd')
    address = request.form.get('address')
    pin = request.form.get('pin')
    user = user = Users.query.filter_by(username = u_name, password = pwd).first()
    if user:
      return redirect('/userlogin')
    new_user = Users(username = u_name, password= pwd, role = 'customer')
    db.session.add(new_user)
    db.session.commit()

    new_customer = Customers(name = name, user_id = new_user.user_id, email = email, address= address, pin_code = pin, phone = phone)
    db.session.add(new_customer)
    db.session.commit()
    return redirect('/userlogin')
  return render_template('customer-signup.html') 

@app.route('/register/pro')
def registerpro():
  return render_template('prof-signup.html')