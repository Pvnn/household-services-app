from flask import Flask,redirect,request, render_template
from flask import current_app as app
from .models import *
import datetime

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
    if len(date)<5:
      date = datetime.date.today()
      date = date.strftime("%Y-%m-%d")
    add_requests = request.form.get('add_requests')
    ex_request = ServiceRequests.query.filter_by(service_id = service_id, customer_id = customer.customer_id, service_status = 'requested', additional_requests = add_requests, requested_service_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()).first()
    if not ex_request:
      print(date)
      new_servicerequest = ServiceRequests(service_id = service_id, customer_id = customer.customer_id, service_status = 'requested', additional_requests = add_requests, requested_service_date = datetime.datetime.strptime(date, "%Y-%m-%d").date())
      db.session.add(new_servicerequest)
      db.session.commit()
    return redirect(f"/user/customer/{user.user_id}")
  return render_template('customer-book-service.html', user = user, customer = customer, service = service)

@app.route('/user/<int:user_id>/service/close/<int:request_id>', methods= ['GET', 'POST'])
def close_service(user_id, request_id):
  user = Users.query.get(user_id)
  service_request = ServiceRequests.query.get(request_id)
  if request.method=='POST':
    remarks = request.form.get('remarks')
    rating = request.form.get('rating')
    service_request.remarks = remarks
    service_request.rating = float(rating)
    service_request.service_status = 'closed'
    service_request.date_of_completion = datetime.datetime.strptime(datetime.date.today().strftime("%Y-%m-%d"), "%Y-%m-%d").date()
    db.session.commit()
    return redirect(f"/user/customer/{user.user_id}")
  return render_template('remarks.html', user = user, service_request = service_request)

@app.route('/user/<int:user_id>/service/cancel/<int:request_id>')
def cancel_request(user_id,request_id):
  ServiceRejections.query.filter_by(request_id = request_id).delete()
  ServiceRequests.query.filter_by(request_id = request_id).delete()
  db.session.commit()
  return redirect(f"/user/customer/{user_id}")


@app.route('/customer/<int:customer_id>/search', methods =['GET', 'POST'])
def customer_search(customer_id):
  customer = Customers.query.get(customer_id)
  if request.method=='POST':
    query_string = request.form.get('query_string')
    result= []
    if query_string:
      for word in query_string.split():
        names_filter= Services.query.filter(Services.name.ilike(f"%{word}%")).all()
        description_filter = Services.query.filter(Services.description.ilike(f"%{word}%")).all()
        category_filter= Services.query.filter(Services.category.ilike(f"%{word}%")).all()
        if word.isdigit():
          pin_filter = []
          pros = ServiceProfessionals.query.filter(ServiceProfessionals.pin_code==int(word)).all()
          for pro in pros:
            pin_filter.append(pro.service)
          if pin_filter:
            result.extend(pin_filter)
        if names_filter:
          result.extend(names_filter)
        if description_filter:
          result.extend(description_filter)
        if category_filter:
          result.extend(category_filter)
      temp = set(result)
      result = list(temp)
      return render_template('customer-search.html', services= result, customer = customer)
  all_services = Services.query.all()
  return render_template('customer-search.html', services= all_services, customer = customer)


@app.route('/user/<int:user_id>/profile')
def view_customer_profile(user_id):
  user = Users.query.get(user_id)
  customer = Customers.query.filter_by(user_id = user_id).first()
  return render_template('customer-profile.html', user=user, customer = customer)


@app.route('/user/<int:user_id>/summary')
def show_summary(user_id):
  labels = [
    'January',
    'February',
    'March',
    'April',
    'May',
    'June',
  ]
 
  data = [0, 10, 15, 8, 22, 18, 25]
  user = Users.query.get(user_id)
  # Return the components to the HTML template 
  return render_template(
    template_name_or_list='customer-summary.html',
    data=data,
    labels=labels,
    user = user
  )
