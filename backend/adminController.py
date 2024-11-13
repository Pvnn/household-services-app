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