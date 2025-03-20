from database import db
from datetime import datetime


class Professional(db.Model):  # Fixed typo in "Proffesional"
    professional_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    description = db.Column(db.String(50), nullable=True)
    service_type = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Professional {self.professional_id} {self.date_created} {self.description} {self.service_type}>'

class Request(db.Model):
    request_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    service_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('professional.professional_id'), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    date_completed = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(50), nullable=False)
    additional_details = db.Column(db.String(50), nullable=True)
    service_type = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Request {self.request_id} {self.user_id} {self.professional_id} {self.date_created} {self.date_completed} {self.status} {self.additional_details} {self.service_type} {self.service_id}>'

class Service(db.Model):
    service_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    service_name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(50), nullable=True)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Service {self.service_id} {self.service_name} {self.description} {self.price}>'

class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    address = db.Column(db.String(50), nullable=True)
    phone = db.Column(db.String(12), nullable=True)
    role = db.Column(db.String(1), nullable=False)
    blocked = db.Column(db.Boolean, nullable=False, default=False)  # Default False for customers

    def __init__(self, username, email, role,password,address,phone):   
        self.username = username
        self.email = email
        self.password = password
        self.address = address
        self.phone = phone
        self.role = role
        self.blocked = True if role == 'P' else False 

    def __repr__(self):
        return f'<Users {self.user_id} {self.username} {self.password} {self.role}>'

class Review(db.Model):
    review_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('professional.professional_id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    review = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return f'<Review {self.review_id} {self.user_id} {self.professional_id} {self.rating} {self.review}>'

class Document(db.Model):
    document_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    professional_id = db.Column(db.Integer, db.ForeignKey('professional.professional_id'), nullable=False)
    file_name = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(50), nullable=False)
    file_data = db.Column(db.LargeBinary, nullable=False)  # Stores the file as binary data
    upload_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<Document {self.document_id} {self.professional_id} {self.file_name}>'