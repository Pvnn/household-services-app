from flask import Flask,redirect,request, render_template
from flask import current_app as app
from .models import *

@app.route('/user/prof/<int:user_id>')
def prof_dash(user_id):
  user = Users.query.filter_by(user_id = user_id).first()
  pro = ServiceProfessionals.query.filter_by(user_id = user_id).first()
  requested_services = ServiceRequests.query.filter(
    ServiceRequests.service_id == pro.service_id,
    ServiceRequests.service_status.in_(['requested', 'accepted'])
).all()
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
  db.session.commit()
  return redirect(f"/user/prof/{user_id}")
