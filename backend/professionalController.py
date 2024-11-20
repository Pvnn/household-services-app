from flask import Flask,redirect,request, render_template
from flask import current_app as app
from .models import *
import datetime
from sqlalchemy import or_

@app.route('/user/prof/<int:user_id>')
def prof_dash(user_id):
  user = Users.query.filter_by(user_id = user_id).first()
  pro = ServiceProfessionals.query.filter_by(user_id = user_id).first()
  rejected_services = ServiceRejections.query.filter_by(professional_id = pro.professional_id).all()
  rejected_service_ids =[request.request_id for request in rejected_services]
  requested_services = ServiceRequests.query.filter(
    ServiceRequests.service_id == pro.service_id,ServiceRequests.service_status.in_(['requested', 'accepted']), ~ServiceRequests.request_id.in_(rejected_service_ids)).all()
  for service in requested_services:
    if service.professional_id and service.professional_id!=pro.professional_id:
      requested_services.remove(service)
  closed_services = ServiceRequests.query.filter_by(service_id = pro.service_id, service_status = 'closed').all()
  return render_template('prof-dash.html', user = user, pro=pro, requested_services = requested_services, closed_services = closed_services)



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

@app.route('/user/prof/<int:user_id>/service/<int:request_id>/accept')
def accept_service(user_id, request_id):
  pro = ServiceProfessionals.query.filter_by(user_id = user_id).first()
  request = ServiceRequests.query.get(request_id)
  request.service_status = 'accepted'
  request.professional = pro
  request.professional_id = pro.professional_id
  ServiceRejections.query.filter_by(request_id = request_id).delete()
  db.session.commit()
  return redirect(f"/user/prof/{user_id}")

@app.route('/user/prof/<int:user_id>/service/<int:request_id>/reject')
def reject_request(user_id, request_id):
  pro = ServiceProfessionals.query.filter_by(user_id = user_id).first()
  new_rejection = ServiceRejections(request_id = request_id, professional_id= pro.professional_id)
  db.session.add(new_rejection)
  db.session.commit()
  return redirect(f"/user/prof/{user_id}")

@app.route('/prof/<int:professional_id>/search', methods = ['GET', 'POST'])
def prof_search(professional_id):
  pro = ServiceProfessionals.query.get(professional_id)
  results = ServiceRequests.query.filter_by(professional_id = pro.professional_id).all()
  if request.method=='POST':
    query_string = request.form.get('query_string')
    if query_string:
      for word in query_string.split():
        results=[]
        name_filter = ServiceRequests.query.join(Customers).filter(ServiceRequests.professional_id==pro.professional_id, Customers.name.ilike(f"%{word}%")).all()
        address_filter = ServiceRequests.query.join(Customers).filter(ServiceRequests.professional_id==pro.professional_id, Customers.address.ilike(f"%{word}%")).all()
        if word[0].isdigit():
          if "/" in word or "-" in word:
            word = word.strip().replace("/", "-")
            query_date = datetime.datetime.strptime(word.strip(), "%Y-%m-%d").date()
            date_filter = ServiceRequests.query.filter(ServiceRequests.professional_id==pro.professional_id, or_(ServiceRequests.date_of_request== query_date, ServiceRequests.date_of_completion == query_date, ServiceRequests.requested_service_date == query_date)).all()
            print(date_filter)
            if date_filter:
              results.extend(date_filter)
          else:
            pin_filter = ServiceRequests.query.join(Customers).filter(ServiceRequests.professional_id==pro.professional_id, Customers.pin_code==int(word)).all()
            if pin_filter:
              results.extend(pin_filter)
        if name_filter:
          results.extend(name_filter)
        if address_filter:
          results.extend(address_filter)
      return render_template('prof-search.html', pro=pro, results = results)

  return render_template('prof-search.html', pro=pro, results = results)