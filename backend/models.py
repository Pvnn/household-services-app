from .database import db
from datetime import date

class Users(db.Model):
  __tablename__ = 'Users'
  
  user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  username = db.Column(db.String, unique=True, nullable=False)
  password = db.Column(db.String, nullable=False)
  role = db.Column(db.String, nullable=False)
  is_blocked = db.Column(db.Boolean, default=False)
  

  service_professional = db.relationship('ServiceProfessionals', backref='user', uselist=False)
  customer = db.relationship('Customers', backref='user', uselist=False)


class Services(db.Model):
    __tablename__ = 'Services'
    
    service_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    base_price = db.Column(db.Float, nullable=False)
    time_required = db.Column(db.Integer)
    category = db.Column(db.String)
    service_professionals = db.relationship('ServiceProfessionals', backref='service')
    service_requests = db.relationship('ServiceRequests', backref='service')


class ServiceProfessionals(db.Model):
    __tablename__ = 'ServiceProfessionals'
    
    professional_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), unique=True, nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('Services.service_id'), nullable=False)
    experience_years = db.Column(db.Integer)
    profile_verified = db.Column(db.Boolean, default=False)
    name = db.Column(db.String, nullable = False)
    phone = db.Column(db.String)
    address = db.Column(db.String)
    pin_code = db.Column(db.String)
    service_requests = db.relationship('ServiceRequests', backref='professional')


class Customers(db.Model):
    __tablename__ = 'Customers'
    
    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), unique=True, nullable=False)
    name = db.Column(db.String)
    email = db.Column(db.String)
    address = db.Column(db.String)
    pin_code = db.Column(db.String)
    phone = db.Column(db.String)
    service_requests = db.relationship('ServiceRequests', backref='customer')


class ServiceRequests(db.Model):
    __tablename__ = 'ServiceRequests'
    
    request_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    service_id = db.Column(db.Integer, db.ForeignKey('Services.service_id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('Customers.customer_id'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('ServiceProfessionals.professional_id'))
    requested_service_date = db.Column(db.Date, nullable=False)
    date_of_request = db.Column(db.Date, default=date.today)
    date_of_completion = db.Column(db.Date)
    service_status = db.Column(db.String, default='requested')
    additional_requests = db.Column(db.String)
    remarks = db.Column(db.String)