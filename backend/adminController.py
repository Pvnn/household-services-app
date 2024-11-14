from flask import Flask,redirect,request, render_template
from flask import current_app as app
from .models import *

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
    return redirect('/admin')

  return render_template('service-edit.html', service = service, category_list = category_list)

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
  return redirect('/admin')