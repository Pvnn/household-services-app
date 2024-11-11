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


@app.route('/user/customer/<int:user_id>')
def customer_dash(user_id):
  user = Users.query.filter_by(user_id = user_id).first()
  customer = Customers.query.filter_by(user_id = user_id).first()
  return render_template('customer-dash.html', customer = customer, user = user, service_requests = customer.service_requests)

@app.route('/user/summary')
def view_summary():
  return render_template('customer-summary.html')

@app.route('/user/<int:user_id>/service/category/<string:category>')
def display_category(user_id, category):
  user = Users.query.filter_by(user_id = user_id).first()
  customer = Customers.query.filter_by(user_id = user_id).first()
  services = Services.query.filter_by(category = category).all()
  return render_template('customer-dash-category.html', user = user, customer = customer, services = services, service_requests = customer.service_requests)

@app.route('/user/<int:user_id>/service/book/<int:service_id>', methods= ['GET', 'POST'])
def book_service(user_id, service_id):
  user = Users.query.filter_by(user_id = user_id).first()
  customer = Customers.query.filter_by(user_id = user_id).first()
  service = Services.query.filter_by(service_id = service_id).first()
  if request.method== 'POST' :
    date = request.form.get('date')
    add_requests = request.form.get('add_requests')
    ex_request = ServiceRequests.query.filter_by(service_id = service_id, customer_id = customer.customer_id, service_status = 'requested', additional_requests = add_requests, requested_service_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()).first()
    if not ex_request:
      new_servicerequest = ServiceRequests(service_id = service_id, customer_id = customer.customer_id, service_status = 'requested', additional_requests = add_requests, requested_service_date = datetime.datetime.strptime(date, "%Y-%m-%d").date())
      db.session.add(new_servicerequest)
      db.session.commit()
    return redirect(f"/user/customer/{user.user_id}")
  return render_template('customer-book-service.html', user = user, customer = customer, service = service)

@app.route('/admin')
def admin_dash():
  services = Services.query.all()
  professionals = ServiceProfessionals.query.all()
  return render_template('admin-dash.html', services = services, professionals = professionals)

@app.route('/user/prof/<int:user_id>')
def prof_dash(user_id):
  user = Users.query.filter_by(user_id = user_id).first()
  pro = ServiceProfessionals.query.filter_by(user_id = user_id).first()
  return render_template('prof-dash.html', user = user, pro=pro)

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

@app.route('/register/pro', methods =['GET', 'POST'])
def registerpro():
  if request.method=='POST':
    name = request.form.get('name')
    u_name = request.form.get('u_name')
    pwd = request.form.get('pwd')
    print(pwd)
    service_name = request.form.get('service')
    exp = request.form.get('exp')
    address = request.form.get('address')
    pin = request.form.get('pin')
    phone = request.form.get('phone')
    user = user = Users.query.filter_by(username = u_name, password = pwd).first()
    if user:
      return redirect('/userlogin')
    new_user = Users(username = u_name, password= pwd, role = 'professional')
    db.session.add(new_user)
    db.session.commit()
    service = Services.query.filter_by(name = service_name).first()
    new_prof = ServiceProfessionals(name = name, user_id = new_user.user_id, address= address, pin_code = pin, phone = phone, service_id = service.service_id, profile_verified = False, experience_years = exp)
    db.session.add(new_prof)
    db.session.commit()

    return redirect('/userlogin')
  services = Services.query.all()
  return render_template('prof-signup.html', services = services)

@app.route('/service/create', methods =['GET', 'POST'])
def create_service():
  if request.method=='POST':
    name = request.form.get('name')
    category = request.form.get('category')
    description = request.form.get('description')
    price = request.form.get('price')
    time = request.form.get('time')
    new_service = Services(name = name, description = description, base_price = price, time_required = time, category = category)
    db.session.add(new_service)
    db.session.commit()
    return redirect('/admin')
  
  category_list = [category[0] for category in db.session.query(Services.category).distinct().all()]
  return render_template('service-create.html', category_list = category_list)

