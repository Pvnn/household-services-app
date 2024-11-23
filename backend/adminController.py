from flask import Flask,redirect,request, render_template
from flask import current_app as app
from .models import *
import datetime
from sqlalchemy import or_

@app.route('/admin')
def admin_dash():
  services = Services.query.all()
  professionals = ServiceProfessionals.query.all()
  service_requests = ServiceRequests.query.all()
  return render_template('admin-dash.html', services = services, professionals = professionals, service_requests = service_requests)

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

@app.route('/admin/view/pro/<int:pro_id>', methods =['GET'])
def view_pro(pro_id):
  pro = ServiceProfessionals.query.get(pro_id)
  return render_template('admin-view-pro.html', pro = pro)

@app.route('/admin/service/edit/<int:service_id>', methods =['GET', 'POST'])
def edit_service(service_id):
  service = Services.query.get(service_id)
  category_list = [category[0] for category in db.session.query(Services.category).distinct().all()]
  if request.method=='POST':
    print(request.form)
    name = request.form.get('name')
    category = request.form.get('category')
    description = request.form.get('description')
    price = request.form.get('price')
    time = request.form.get('time')
    service.name = name
    service.category = category
    service.description = description
    service.base_price = float(price)
    service.time_required = int(time)
    db.session.flush()
    db.session.commit()
    return redirect(request.referrer)

  return render_template('service-edit.html', service = service, category_list = category_list)

@app.route('/admin/view/customer/<int:customer_id>', methods =['GET'])
def view_customer(customer_id):
  customer = Customers.query.get(customer_id)
  return render_template('admin-view-customer.html', customer = customer)

@app.route('/admin/view/request/<int:request_id>', methods =['GET'])
def view_request(request_id):
  request = ServiceRequests.query.get(request_id)
  return render_template('admin-view-request.html', request= request)

@app.route('/admin/view/service/<int:service_id>', methods =['GET'])
def view_service(service_id):
  service = Services.query.get(service_id)
  return render_template('admin-view-service.html', service= service)

@app.route('/admin/approve/prof/<int:professional_id>', methods =['GET'])
def approve_professional(professional_id):
  pro = ServiceProfessionals.query.get(professional_id)
  pro.profile_verified = True
  db.session.commit()
  return redirect(request.referrer)

@app.route('/admin/block/prof/<int:professional_id>')
def block_professional(professional_id):
  pro = ServiceProfessionals.query.get(professional_id)
  user = Users.query.get(pro.user_id)
  user.is_blocked = True
  for s_request in pro.service_requests:
    if s_request.service_status=='accepted':
      s_request.service_status = 'requested'
      s_request.professional_id = None
  db.session.commit()
  return redirect(request.referrer)

@app.route('/admin/unblock/prof/<int:professional_id>')
def unblock_professional(professional_id):
  pro = ServiceProfessionals.query.get(professional_id)
  user = Users.query.get(pro.user_id)
  user.is_blocked = False
  db.session.commit()
  return redirect(request.referrer)

@app.route('/admin/search', methods = ['GET', 'POST'])
def admin_search():
  key = None
  if request.method=='POST':
    key = request.form.get('key')
    query_string = request.form.get('query_string')
    if query_string:
      result =[]
      if key=='services':
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
        result = list(set(result))
        return render_template('admin-search.html', results = result, key='services')
      elif key=='requests':
        for word in query_string.split():
          results=[]
          name_filter = ServiceRequests.query.join(Customers).filter(Customers.name.ilike(f"%{word}%")).all()
          address_filter = ServiceRequests.query.join(Customers).filter(Customers.address.ilike(f"%{word}%")).all()
          status_filter = ServiceRequests.query.join(Customers).filter(ServiceRequests.service_status.ilike(f"%{word}%")).all()
          if word[0].isdigit():
            if "/" in word or "-" in word:
              word = word.strip().replace("/", "-")
              query_date = datetime.datetime.strptime(word.strip(), "%Y-%m-%d").date()
              date_filter = ServiceRequests.query.filter(or_(ServiceRequests.date_of_request== query_date, ServiceRequests.date_of_completion == query_date, ServiceRequests.requested_service_date == query_date)).all()
              print(date_filter)
              if date_filter:
                results.extend(date_filter)
            else:
              pin_filter = ServiceRequests.query.join(Customers).filter(Customers.pin_code==int(word)).all()
              if pin_filter:
                results.extend(pin_filter)
          if name_filter:
            results.extend(name_filter)
          if address_filter:
            results.extend(address_filter)
          if status_filter:
            results.extend(status_filter)
        return render_template('admin-search.html', results = results, key='requests')
      elif key=='professionals':
        for word in query_string.split():
          names_filter= ServiceProfessionals.query.filter(ServiceProfessionals.name.ilike(f"%{word}%")).all()
          service_filter = ServiceProfessionals.query.join(Services).filter(Services.name.ilike(f"%{word}%")).all()
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
          if service_filter:
            result.extend(service_filter)
        result = list(set(result))
        return render_template('admin-search.html', results = result, key='professionals')
      elif key=='customers':
        for word in query_string.split():
          names_filter= Customers.query.filter(Customers.name.ilike(f"%{word}%")).all()
          address_filter= Customers.query.filter(Customers.address.ilike(f"%{word}%")).all()
          email_filter= Customers.query.filter(Customers.email.ilike(f"%{word}%")).all()
          if word.isdigit():
            pin_filter = Customers.query.filter_by(pin_code = int(word))
            if pin_filter:
              result.extend(pin_filter)
          if names_filter:
            result.extend(names_filter)
          if address_filter:
            result.extend(address_filter)
          if email_filter:
            result.extend(email_filter)
        result = list(set(result))
        return render_template('admin-search.html', results = result, key='customers')
  all_customers = Customers.query.all()
  all_services = Services.query.all()
  all_requests = ServiceRequests.query.all()
  all_pros = ServiceProfessionals.query.all()
  if not key or key=='customers':
    return render_template('admin-search.html', results = all_customers, key='customers')
  elif key=='services':
    return render_template('admin-search.html', results = all_services, key='services')
  elif key=='requests':
    return render_template('admin-search.html', results = all_requests, key='requests')
  elif key=='professionals':
    return render_template('admin-search.html', results = all_pros, key='professionals')
  
@app.route('/admin/profile')
def view_admin_profile():
  user = Users.query.filter_by(role= 'admin').first()
  return render_template('admin-profile.html', user = user)

@app.route('/admin/profile/edit', methods = ['GET', 'POST'])
def edit_admin_profile():
  user = Users.query.filter_by(role= 'admin').first()
  if request.method=='POST':
    username = request.form.get('username')
    user.username = username
    db.session.commit()
    return redirect('/admin/profile')
  return render_template('admin-profile-edit.html', user = user)


@app.route('/admin/block/customer/<int:customer_id>')
def block_customer(customer_id):
  customer = Customers.query.get(customer_id)
  customer.user.is_blocked = True
  customer_request_ids = [request.request_id for request in ServiceRequests.query.filter_by(customer_id = customer_id)]
  ServiceRejections.query.filter(ServiceRejections.request_id.in_(customer_request_ids)).delete()
  ServiceRequests.query.filter(ServiceRequests.customer_id== customer_id, ServiceRequests.service_status!='closed').delete()
  db.session.commit()
  return redirect('/admin/search')

@app.route('/admin/unblock/customer/<int:customer_id>')
def unblock_customer(customer_id):
  customer = Customers.query.get(customer_id)
  customer.user.is_blocked = False
  db.session.commit()
  return redirect('/admin/search')

@app.route('/admin/service/delete/<int:service_id>')
def delete_service(service_id):
  s_requests = ServiceRequests.query.filter_by(service_id = service_id).all()
  for s_request in s_requests:
    ServiceRejections.query.filter_by(request_id = s_request.request_id).delete()
  pros = ServiceProfessionals.query.filter_by(service_id = service_id).all()
  for pro in pros:
    pro.user.is_blocked = True
    pro.profile_verified = False
  ServiceRequests.query.filter_by(service_id = service_id).delete()
  Services.query.filter_by(service_id = service_id).delete()
  db.session.commit()
  return redirect(request.referrer)
