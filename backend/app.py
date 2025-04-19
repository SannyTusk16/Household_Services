from flask import Flask, jsonify, request
from flask_cors import CORS
from model import *
from database import db
from config import Config
from flask_migrate import Migrate
from datetime import datetime, timedelta
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt
import requests
from werkzeug.utils import secure_filename
import os
from flask import send_file
from io import BytesIO
import traceback
from celery import Celery
from celery.schedules import crontab
# from config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND 
from flask_mail import Mail, Message
from flask_apscheduler import APScheduler
from flask_caching import Cache 
from celery import shared_task
from flask_swagger_ui import get_swaggerui_blueprint
from flask import send_from_directory    
from datetime import datetime
# flask run --cert=cert.pem --key=key.pem --debug

SWAGGER_URL = "/swagger"
API_URL = "/static/swagger.json"




def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
UPLOAD_FOLDER = 'uploads/documents'  # Define where files will be stored
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg',"docx"}  

access_token = None

app = Flask(__name__)


app.config.from_object(Config)
db.init_app(app)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:D:/Codes/HouseHoldServices/backend/instance'
app.config['SECURITY_PASSWORD_SALT'] = 'my_salt'
app.config["JWT_SECRET_KEY"] = 'your_jwt_secret_key'
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['CELERY_BROKER_URL'] = "redis://localhost:6379/0",
app.config['CELERY_RESULT_BACKEND'] = "redis://localhost:6379/0"
app.config['GOOGLE_CHAT_WEBHOOK_URL'] = "https://chat.googleapis.com/v1/spaces/XXXXXX/messages"
app.config['MAIL_SENDER'] = "your-email@example.com"
app.config['MAIL_SERVER'] = "smtp.gmail.com"
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = "your-email@example.com"
app.config['MAIL_PASSWORD'] = "your-email-password"
app.config["MAIL_SERVER"] = "localhost"
app.config["MAIL_PORT"] = 1025
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = False
app.config["CACHE_TYPE"] = "RedisCache"
app.config["CACHE_REDIS_HOST"] = "localhost"
app.config["CACHE_REDIS_PORT"] = 6379
app.config["CACHE_REDIS_DB"] = 0  
app.config["CACHE_DEFAULT_TIMEOUT"] = 300 
app.config["SWAGGER"] = {
    "title": "Home Services API",
    "description": "API documentation for the Home Services App",
    "version": "1.0.0"
}
# swagger = Swagger(app) 

cache = Cache(app)
swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

    
migrate = Migrate(app, db)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)


def make_celery(app):
    celery = Celery(
        app.import_name,
        broker=app.config["CELERY_BROKER_URL"],
        backend=app.config["CELERY_RESULT_BACKEND"]
    )

    celery.conf.beat_schedule = {  
        "send_monthly_reports": {
            "task": "app.send_monthly_activity_report", 
            "schedule": crontab(minute=0, hour=0, day_of_month=1),  # Runs on 1st of every month at midnight
        },
    }

    celery.conf.timezone = "UTC"  
    return celery


CORS(app)
mail = Mail(app)
celery = make_celery(app)

scheduler = APScheduler()

@scheduler.task("cron", hour=18, minute=0)  
def schedule_daily_reminders():
    send_daily_reminders.delay()

scheduler.init_app(app)
scheduler.start()   


@celery.task
def send_daily_reminders():
    print("Sending daily reminders to service professionals...")
    # Your logic to fetch pending requests and send alerts



@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_vue(path):
    if path and os.path.exists(os.path.join("static", path)):
        return send_from_directory("static", path)
    return send_from_directory("static", "index.html")

@app.route("/api/send_mail_with_timestamp")
def send_mail_with_timestamp():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Format: YYYY-MM-DD HH:MM:SS
    msg = Message(
        "Timestamped Email",
        sender="your_email@gmail.com",
        recipients=["recipient@example.com"]
    )
    msg.body = f"Hello,\n\nThis email was sent at {now}.\n\nBest regards!"
    
    try:
        mail.send(msg)
        return "Email with timestamp sent successfully!"
    except Exception as e:
        return f"Error: {str(e)}"


@app.route("/api/send_mail")
def send_mail():
    msg = Message(
        "Your Subject Here",
        sender="your_email@gmail.com",
        recipients=["recipient@example.com"]
    )
    msg.body = "This is a test email from Flask."
    
    try:
        mail.send(msg)
        return "Email sent successfully!"
    except Exception as e:
        return f"Error: {str(e)}"

@app.route("/api/send_html_mail")
def send_html_mail():
    msg = Message(
        "Welcome Email",
        sender="your_email@gmail.com",
        recipients=["recipient@example.com"]
    )
    msg.html = "<h1>Welcome to Our Service</h1><p>We are glad to have you!</p>"

    try:
        mail.send(msg)
        return "HTML email sent successfully!"
    except Exception as e:
        return f"Error: {str(e)}"


@app.route("/api/send_mail_attachment")
def send_mail_attachment():
    msg = Message(
        "Your Report",
        sender="your_email@gmail.com",
        recipients=["recipient@example.com"]
    )
    msg.body = "Here is your requested report."

    with app.open_resource("report.pdf") as pdf:
        msg.attach("report.pdf", "application/pdf", pdf.read())

    try:
        mail.send(msg)
        return "Email with attachment sent successfully!"
    except Exception as e:
        return f"Error: {str(e)}"
@celery.task
def send_async_email(subject, recipient, body):
    msg = Message(subject, sender="your_email@gmail.com", recipients=[recipient])
    msg.body = body
    mail.send(msg)

@app.route("/api/send_async_mail")
def send_async_mail():
    send_async_email.delay("Async Email", "recipient@example.com", "This email was sent in the background!")
    return "Email is being sent in the background!"

@shared_task
def send_monthly_activity_report():
    """Send a monthly activity report to customers via email."""
    customers = Users.query.filter_by(role="C").all()
    
    for customer in customers:
        # Fetch service requests for the past month
        last_month = datetime.now().replace(day=1) - timedelta(days=1)
        service_requests = Request.query.filter(
            Request.customer_id == customer.user_id,
            Request.date_of_request >= last_month.replace(day=1),
            Request.date_of_request <= last_month
        ).all()

        # Generate the report
        service_count = len(service_requests)
        closed_count = sum(1 for req in service_requests if req.status == "Closed")

        email_body = f"""
        <html>
        <body>
            <h2>Monthly Activity Report - Household Services</h2>
            <p>Hi {customer.username},</p>
            <p>Here's your activity report for last month:</p>
            <ul>
                <li>Total Service Requests: {service_count}</li>
                <li>Closed Requests: {closed_count}</li>
            </ul>
            <p>Thank you for using our services!</p>
            <p>Best regards,<br>Household Services Team</p>
        </body>
        </html>
        """

        # Send the email
        try:
            msg = Message(
                subject="Your Monthly Activity Report",
                sender="your_email@gmail.com",
                recipients=[customer.email]
            )
            msg.html = email_body
            mail.send(msg)
            print(f"Sent report to {customer.email}")
        except Exception as e:
            print(f"Error sending report to {customer.email}: {str(e)}")

    return "Monthly reports sent."


EXPORT_FOLDER = "exports"

@shared_task
def export_closed_requests(admin_email):
    """Export closed service requests as CSV and notify admin."""
    file_path = os.path.join(EXPORT_FOLDER, f"closed_requests_{datetime.now().strftime('%Y%m%d')}.csv")

    # Ensure export folder exists
    os.makedirs(EXPORT_FOLDER, exist_ok=True)

    # Fetch closed service requests
    closed_requests = Request.query.filter_by(status="Closed").all()

    # Write CSV file
    with open(file_path, "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Service ID", "Customer ID", "Professional ID", "Date of Request", "Remarks"])
        for req in closed_requests:
            writer.writerow([req.service_id, req.customer_id, req.professional_id, req.date_of_request, req.remarks])

    # Send an email to the admin with the CSV attached
    try:
        msg = Message(
            subject="Closed Service Requests Export",
            sender="your_email@gmail.com",
            recipients=[admin_email]
        )
        msg.body = "Attached is the CSV file containing all closed service requests."
        with open(file_path, "rb") as f:
            msg.attach(os.path.basename(file_path), "text/csv", f.read())
        mail.send(msg)

        print(f"CSV export sent to {admin_email}")

    except Exception as e:
        print(f"Error sending CSV export: {str(e)}")

    return f"CSV export completed: {file_path}"


@app.route("/api/export-closed-requests", methods=["POST"])
def trigger_csv_export():
    """Trigger CSV export as an async Celery task."""
    data = request.get_json()
    admin_email = data.get("admin_email")

    if not admin_email:
        return jsonify({"error": "Admin email is required"}), 400

    task = export_closed_requests.delay(admin_email)
    
    return jsonify({"message": "CSV export started", "task_id": task.id}), 202



with app.app_context():
    db.create_all()
    if not Users.query.filter_by(user_id='1').first():
        user = Users(username='admin', password=bcrypt.generate_password_hash('admin').decode('utf-8'), role='A', email='admin@gmail.com',address="admin",phone=999999999)
        db.session.add(user)
        db.session.commit()
    if not Users.query.filter_by(user_id='2').first():
        user = Users(username='customer', password=bcrypt.generate_password_hash('customer').decode('utf-8'), role='C', email='customer@gmail.com', address='customer', phone=918790621444)
        db.session.add(user)
        db.session.commit()
    if not Users.query.filter_by(user_id='3').first():
        user = Users(username='professional', password=bcrypt.generate_password_hash('professional').decode('utf-8'), role='P', email='pro@gmail.com', address='pro', phone='918790621445')
        professional = Professional(user_id=3, description='pro', service_type='Cleaning', date_created=datetime.now())
        db.session.add(professional)
        db.session.add(user)
        db.session.commit()
    if not Users.query.filter_by(user_id='4').first():
        user = Users(username='professional1', password=bcrypt.generate_password_hash('professional1').decode('utf-8'), role='P', email='pro1@gmail.com', phone='918790621446', address='pro1')
        professional = Professional(user_id=4, description='pro1', service_type='Plumbing', date_created=datetime.now())
        db.session.add(professional)
        db.session.add(user)
        db.session.commit()
    if not Service.query.filter_by(service_id='1').first():
        service = Service(service_name='Cleaning', description='Cleaning', price=100)
        db.session.add(service)
        db.session.commit()
    if not Service.query.filter_by(service_id='2').first():
        service = Service(service_name='Plumbing', description='Plumbing', price=100)
        db.session.add(service)
        db.session.commit()
    if not Service.query.filter_by(service_id='3').first():
        service = Service(service_name='Electrician', description='Electrician', price=100)
        db.session.add(service)
        db.session.commit()
    if not Request.query.filter_by(request_id='1').first():
        request = Request(service_id=1, user_id=2, professional_id=1, date_created=datetime.now(), date_completed=datetime.now(), status='Pending', additional_details='Cleaning', service_type='Cleaning')
        db.session.add(request)
        db.session.commit()
    if not Request.query.filter_by(request_id='2').first():
        request = Request(service_id=2, user_id=2, professional_id=2, date_created=datetime.now(), date_completed=datetime.now(), status='Pending', additional_details='Plumbing', service_type='Plumbing')
        db.session.add(request)
        db.session.commit()
    if not Review.query.filter_by(review_id='1').first():
        review = Review(user_id=1, professional_id=1, review='Good', rating=5)
        db.session.add(review)
        db.session.commit()

@app.route("/api/login", methods=['GET', 'POST'])
def landing():
    """Login"""
    global access_token
    
    if request.method == 'GET':
        return jsonify({'message': 'Welcome to the home page'}), 200
    elif request.method == 'POST':

        if not request.is_json:
            return jsonify({'error': 'Unsupported Media Type, please use application/json'}), 415
        data = request.get_json()
        mail_id = data.get('mail_id')
        password = data.get('password')
        verify_url = "https://www.google.com/recaptcha/api/siteverify"
        payload = {
            "secret": "6Lc1lAsrAAAAABgyTItogKWDu9TUatqKBlwGA6oT",
            "response": data.get("recaptcha_token")
        }
        recaptcha_response = requests.post(verify_url, data=payload)
        result = recaptcha_response.json()

        if not result.get("success"):
            return jsonify({"error": "reCAPTCHA verification failed"}), 401

        # Optional: For v3, check score
        if "score" in result and result["score"] < 0.5:
            return jsonify({"error": "reCAPTCHA score too low"}), 403
        if request.method == 'GET':
            return jsonify({'message': 'Welcome to the home page'}), 200
        elif request.method == 'POST':
            if not request.is_json:
                return jsonify({'error': 'Unsupported Media Type, please use application/json'}), 415

        user = Users.query.filter_by(email=mail_id).first()
        if user and bcrypt.check_password_hash(user.password, password):
            access_token = create_access_token(identity=str(user.user_id))
            return jsonify({'message': 'Login Success', 'access_token': access_token}), 200
        else:
            return jsonify({'message': 'Login failed'}), 401


@app.route("/api/register", methods=["POST"])
def register():
    if request.content_type.startswith("multipart/form-data"):  # Handle file uploads
        form_data = request.form
        file = request.files.get("resume")
    elif request.is_json:  # Handle JSON requests
        form_data = request.get_json()
        file = None
    else:
        return jsonify({"error": "Unsupported Media Type, please use application/json or form-data"}), 415

    # Extract user fields
    username = form_data.get("username")
    password = form_data.get("password")
    role = form_data.get("role")
    email = form_data.get("email")
    address = form_data.get("address")
    phone = form_data.get("phone")

    # Validate required fields
    if not all([username, password, role, email, address, phone]):
        return jsonify({"message": "Please provide all required fields"}), 400

    # Check if user already exists
    if Users.query.filter_by(username=username).first():
        return jsonify({"message": "Username already exists"}), 409
    if Users.query.filter_by(email=email).first():
        return jsonify({"message": "Email already exists"}), 409

    # Create user
    user = Users(
        username=username,
        password=bcrypt.generate_password_hash(password).decode("utf-8"),
        role=role,
        email=email,
        address=address,
        phone=phone
    )
    db.session.add(user)
    db.session.commit()

    # Role-specific logic
    resume_path = None
    if role == "C":
        print("Customer")
    elif role == "P":
        print("Professional")
        service_type = form_data.get("service_type")
        description = form_data.get("description")
        if not service_type or not description:
            return jsonify({"message": "Please provide service type and description"}), 400
        professional = Professional(
            user_id=user.user_id,
            service_type=service_type,
            description=description,
            date_created=datetime.now()
        )
        db.session.add(professional)

        # Handle file upload
        professional = Professional.query.filter_by(user_id=user.user_id).first()
        if file and allowed_file(file.filename):
            file_ext = file.filename.rsplit(".", 1)[1].lower()
            filename = f"{user.user_id}.{file_ext}"
            resume_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(resume_path)
            document = Document(
                professional_id=professional.professional_id,
                file_name=filename,
                file_type=file.content_type,
                file_data=file.read()
            )
            db.session.add(document)
            db.session.commit()
    
    db.session.commit()

    # **Send Welcome Email**
    send_welcome_email(username, email, role)

    return jsonify({
        "message": "User registered successfully",
        "user": {
            "username": username,
            "email": email,
            "role": role,
            "resume_path": resume_path if resume_path else "No file uploaded"
        }
    }), 201

def send_welcome_email(username, email, role):
    """Send a welcome email to the newly registered user"""
    subject = "Welcome to Household Services"
    body = f"""
    Hi {username},

    Welcome to Household Services! We're excited to have you on board.

    Your role: {"Customer" if role == "C" else "Professional"}

    If you have any questions, feel free to reach out.

    Best regards,
    The Household Services Team
    """

    try:
        msg = Message(subject, sender="your_email@gmail.com", recipients=[email])
        msg.body = body
        mail.send(msg)
        print(f"Email sent to {email}")
    except Exception as e:
        print(f"Error sending email: {str(e)}")




@app.route("/api/current_user", methods=["GET"])
@jwt_required()
def get_current_user():
    try:
        user_id = get_jwt_identity()
        user = Users.query.filter_by(user_id=user_id).first()

        if user:
            return jsonify({
                'user_id': user.user_id,
                'username': user.username,
                'email': user.email,
                'role': user.role,
                'address': user.address,
                'phone': user.phone
            }), 200
        else:
            return jsonify({"message": "User not found"}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    

@app.route("/api/upload_document", methods=["POST"])
def upload_document():
    if 'file' not in request.files or not request.form.get('professional_id'):
        return jsonify({"message": "File and professional_id are required"}), 400

    file = request.files['file']
    professional_id = request.form.get('professional_id')

    
    professional = Professional.query.filter_by(professional_id=professional_id).first()
    if not professional:
        return jsonify({"message": "Professional not found"}), 404

    
    new_document = Document(
        professional_id=professional_id,
        file_name=file.filename,
        file_type=file.content_type,
        file_data=file.read()
    )
    db.session.add(new_document)
    db.session.commit()
    print("File uploaded successfully")

    return jsonify({"message": "File uploaded successfully", "document_id": new_document.document_id}), 201

    
@app.route("/api/get_document/<int:document_id>", methods=["GET"])
def get_document(document_id):
    document = Document.query.filter_by(document_id=document_id).first()

    if not document:
        return jsonify({"message": "Document not found"}), 404

    return jsonify({
        "document_id": document.document_id,
        "professional_id": document.professional_id,
        "file_name": document.file_name,
        "file_type": document.file_type,
        "upload_date": document.upload_date.strftime("%Y-%m-%d %H:%M:%S")
    }), 200



@app.route("/api/download_document/<int:document_id>", methods=["GET"])
def download_document(document_id):
    document = Document.query.filter_by(document_id=document_id).first()

    if not document:
        return jsonify({"message": "Document not found"}), 404

    # Serve the file as a response
    return send_file(
        BytesIO(document.file_data),
        mimetype=document.file_type,
        as_attachment=True,
        download_name=document.file_name
    )

@app.route("/api/get_professional_documents/<int:professional_id>", methods=["GET"])
def get_professional_documents(professional_id):
    professional = Professional.query.filter_by(professional_id=professional_id).first()

    if not professional:
        return jsonify({"message": "Professional not found"}), 404

    documents = Document.query.filter_by(professional_id=professional_id).all()

    if not documents:
        return jsonify({"message": "No documents found"}), 404

    documents_list = []
    for document in documents:
        documents_list.append({
            "document_id": document.document_id,
            "file_name": document.file_name,
            "file_type": document.file_type,
            "upload_date": document.upload_date.strftime("%Y-%m-%d %H:%M:%S")
        })

    return jsonify({"documents": documents_list}), 200


@app.route("/api/get_all_customers", methods=["GET"])
@cache.cached(timeout=5)
@jwt_required()
def get_all_customers():

    users = Users.query.filter_by(role="C").all()
    users = list(users)

    user = Users.query.filter_by(user_id=get_jwt_identity()).first()
    print(user.role)

    if(user.role != 'A'):
        return jsonify({"message": "Unauthorized"}), 401

    if not users:
        return jsonify({"message": "No customers found"}), 404

    customers_list = []
    for customer in users:
        customers_list.append({
            "user_id": customer.user_id,
            "username": Users.query.filter_by(user_id=customer.user_id).first().username,
            "email": Users.query.filter_by(user_id=customer.user_id).first().email,
            "blocked": customer.blocked
        })

    return jsonify({"customers": customers_list}), 200



@app.route('/api/get_all_services', methods=['GET'])
@cache.cached(timeout=5)
def get_all_services():
    try:
        services = Service.query.all()
        service_list = [
            {
                "id": service.service_id,
                "name": service.service_name,
                "description": service.description,
                "price": service.price
            }
            for service in services
        ]
        print("Service List \n",service_list)
        return jsonify(service_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/get_service/<int:service_id>", methods=["GET"])
def get_service(service_id):
    service = Service.query.filter_by(service_id=service_id).first()

    if not service:
        return jsonify({"message": "Service not found"}), 404

    return jsonify({
        "service_id": service.service_id,
        "service_name": service.service_name,
        "description": service.description,
        "price": service.price
    }), 200

@app.route("/api/create_service", methods=["POST"])
def create_service():
    if not request.is_json:
        return jsonify({"message": "Unsupported Media Type, please use application/json"}), 415

    data = request.get_json()
    service_name = data.get("service_name")
    description = data.get("description")
    price = data.get("price")

    if not service_name or not description or not price:
        return jsonify({"message": "Please provide all the details"}), 400

    if Service.query.filter_by(service_name=service_name).first():
        return jsonify({"message": "Service already exists"}), 409

    new_service = Service(service_name=service_name, description=description, price=price)
    db.session.add(new_service)
    db.session.commit()

    return jsonify({"message": "Service created successfully", "service_id": new_service.service_id}), 201

@app.route("/api/get_all_professionals", methods=["GET"])
@cache.cached(timeout=5)
def get_all_professionals():
    professionals = Professional.query.all()

    if not professionals:
        return jsonify({"message": "No professionals found"}), 404
    

    professionals_list = []
    for professional in professionals:
        service = Service.query.filter_by(service_name=professional.service_type).first()
        professionals_list.append({
            "professional_id": professional.professional_id,
            "user_id": professional.user_id,
            "description": professional.description,
            "service_type": professional.service_type,
            "date_created": professional.date_created.strftime("%Y-%m-%d %H:%M:%S"),
            "username": Users.query.filter_by(user_id=professional.user_id).first().username,
            "price": service.price,
            "blocked": Users.query.filter_by(user_id=professional.user_id).first().blocked
        })

    return jsonify({"professionals": professionals_list}), 200

@app.route("/api/get_service_professionals/<int:service_id>", methods=["GET"])
def get_service_professionals(service_id):
    service = Service.query.filter_by(service_id=service_id).first()

    if not service:
        return jsonify({"message": "Service not found"}), 404

    professionals = (
        db.session.query(Professional, Users.username)
        .join(Users, Professional.user_id == Users.user_id)  # Joining User table
        .filter(Professional.service_type == service.service_name)
        .all()
    )


    print("Professionals for the service:", service.service_name, list(professionals))


    if not professionals:
        return jsonify({"message": "No professionals found"}), 404

    professionals_list = []
    for professional, username in professionals:
        reviews = Review.query.filter_by(professional_id=professional.professional_id).all()
        rating = 0
        if reviews:
            rating = round(sum([review.rating for review in reviews]) / len(reviews),2)
        professionals_list.append({
            "professional_id": professional.professional_id,
            "user_id": professional.user_id,
            "username": username,  # Add username here
            "description": professional.description,
            "service_type": professional.service_type,
            "date_created": professional.date_created.strftime("%Y-%m-%d %H:%M:%S"),
            "rating": rating
        })
    
    for i in professionals_list:
        print(i.get("username"), i.get("rating"))    

    return jsonify({"professionals": professionals_list}), 200


@app.route("/api/get_professional/<int:professional_id>", methods=["GET"])
def get_professional(professional_id):
    professional = Professional.query.filter_by(professional_id=professional_id).first()

    if not professional:
        return jsonify({"message": "Professional not found"}), 404

    return jsonify({
        "professional_id": professional.professional_id,
        "user_id": professional.user_id,
        "description": professional.description,
        "service_type": professional.service_type,
        "date_created": professional.date_created.strftime("%Y-%m-%d %H:%M:%S")
    }), 200


@app.route("/api/get_user/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = Users.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "id": user.user_id,
        "name": user.username,
        "email": user.email,
        "phone": user.phone,
        "address": user.address
    })

@app.route('/api/add_service', methods=['POST'])
def add_service():
    data = request.json
    new_service = Service(
        service_name=data.get('service_name'),
        description=data.get('description'),
        price=data.get('price')
    )
    db.session.add(new_service)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Service added successfully', 'service_id': new_service.service_id})



@app.route('/api/get_all_service_requests', methods=['GET'])
@cache.cached(timeout=5)
def get_all_service_requests():
    try:
        requests = Request.query.all()
        request_list = [
            {
                "id": req.request_id,
                "user_id": req.user_id,
                "professional_id": req.professional_id,
                "service_type": req.service_type,
                "status": req.status,
                "date_created": req.date_created.strftime("%Y-%m-%d %H:%M:%S"),
                "date_completed": req.date_completed.strftime("%Y-%m-%d %H:%M:%S") if req.date_completed else None,
                "additional_details": req.additional_details
            }
            for req in requests
        ]
        return jsonify(request_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route("/api/user_professional_id/<int:user_id>", methods=["GET"])
def get_user_professional_id(user_id):
    professional = Professional.query.filter_by(user_id=user_id).first()
    print(professional)

    if not professional:
        return jsonify({"message": "Professional not found"}), 404

    return jsonify({"professional_id": professional.professional_id}), 200


@app.route("/api/get_service_request/<int:request_id>", methods=["GET"])
@jwt_required()
def get_service_request(request_id):
    request = Request.query.filter_by(request_id=request_id).first()

    if not request:
        return jsonify({"message": "Request not found"}), 404

    return jsonify({
        "request_id": request.request_id,
        "service_id": request.service_id,
        "user_id": request.user_id,
        "professional_id": request.professional_id,
        "date_created": request.date_created.strftime("%Y-%m-%d %H:%M:%S"),
        "date_completed": request.date_completed.strftime("%Y-%m-%d %H:%M:%S") if request.date_completed else None,
        "status": request.status,
        "additional_details": request.additional_details,
        "service_type": request.service_type
    }), 200


@app.route("/api/professional_service_request/<int:professional_id>", methods=["GET"])
@jwt_required()
def get_professional_service_request(professional_id):
    requests = Request.query.filter_by(professional_id=professional_id).all()

    if not requests:
        return jsonify({"message": "No requests found"}), 404

    request_list = []
    for request in requests:
        request_list.append({
            "request_id": request.request_id,
            "service_id": request.service_id,
            "user_id": request.user_id,
            "date_created": request.date_created.strftime("%Y-%m-%d %H:%M:%S"),
            "date_completed": request.date_completed.strftime("%Y-%m-%d %H:%M:%S") if request.date_completed else None,
            "status": request.status,
            "additional_details": request.additional_details,
            "service_type": request.service_type,
            "username": Users.query.filter_by(user_id=request.user_id).first().username
        })

    return jsonify({"requests": request_list}), 200


@app.route("/api/get_user_name/<int:user_id>", methods=["GET"])
@jwt_required()
def get_user_name(user_id):
    user = Users.query.filter_by(user_id=user_id).first()

    if not user:
        return jsonify({"message": "User not found"}), 404
    print("username is",user.username)
    return jsonify({"username": user.username}), 200


@app.route('/api/service-requests/<int:request_id>/accept', methods=['POST'])
@jwt_required()
def accept_request(request_id):
    """Allows a professional to accept a service request"""
    try:
        professional_id = get_jwt_identity()  # Get logged-in user's ID

        print("User ID",professional_id)

        professional = Professional.query.filter_by(user_id=professional_id).first()
        professional_id = professional.professional_id

        service_request = Request.query.filter_by(request_id=request_id, professional_id=professional_id).first()
        if not service_request:
            return jsonify({"error": "Request not found or not assigned to you"}), 404

        if service_request.status in ["Accepted", "Rejected","Finished","Abandoned"]:
            return jsonify({"error": "Request is already processed"}), 400

        service_request.status = "Accepted"
        db.session.commit()

        return jsonify({"message": "Service request accepted successfully", "request_id": request_id}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/service-requests/<int:request_id>/reject', methods=['POST'])
@jwt_required()
def reject_request(request_id):
    """Allows a professional to reject a service request"""
    try:
        user_id = get_jwt_identity()  # Get logged-in user's ID

        professional = Professional.query.filter_by(user_id=user_id).first()
        professional_id = professional.professional_id 

        service_request = Request.query.filter_by(request_id=request_id, professional_id=professional_id).first()
        if not service_request:
            return jsonify({"error": "Request not found or not assigned to you"}), 404

        if service_request.status in ["Accepted", "Rejected","Finished","Abandoned"]:
            return jsonify({"error": "Request is already processed"}), 400

        service_request.status = "Rejected"
        db.session.commit()

        return jsonify({"message": "Service request rejected successfully", "request_id": request_id}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/conclude-request/<int:request_id>', methods=['POST'])
@jwt_required()
def conclude_request(request_id):
    user_id = get_jwt_identity()
    service_request = Request.query.filter_by(request_id=request_id, user_id=user_id).first()
    print("service request",service_request.status)
    
    if service_request.status =="Accepted":
        service_request.status = "Concluded"
        db.session.commit()
        return jsonify({"message": "Request has been concluded successfully!"})
    if not service_request:
        return jsonify({"error": "Service request not found or unauthorized"}), 404

    if service_request.status != "Pending" or service_request.status != "Accepted":
        return jsonify({"error": "Only pending requests can be concluded"}), 400

    service_request.status = "Concluded"
    db.session.commit()

    return jsonify({"message": "Request has been concluded successfully!"})

@app.route('/api/service-requests/<int:request_id>/finish', methods=['POST'])
@jwt_required()
def finish_request(request_id):
    """Allows a professional to finish a service request"""
    try:
        user_id = get_jwt_identity()  # Get logged-in user's ID
        professional = Users.query.filter_by(user_id=user_id).first()
        professional_id = Professional.query.filter_by(user_id=professional.user_id).first().professional_id
        print("professional ID",professional_id)

        service_request = Request.query.filter_by(request_id=request_id, professional_id=professional_id).first()
        if not service_request:
            return jsonify({"error": "Request not found or not assigned to you"}), 404

        if service_request.status in ["Finished", "Abandoned"]:
            return jsonify({"error": "Request is already processed"}), 400
        elif service_request.status!="Concluded":
            return jsonify({"error": "Customer hasn't concluded yet"}), 400


        service_request.status = "Finished"
        service_request.date_completed = datetime.now()
        db.session.commit()

        return jsonify({"message": "Service request finished successfully", "request_id": request_id}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/service-requests/<int:request_id>/abandon', methods=['POST'])
@jwt_required()
def abandon_request(request_id):
    """Allows a professional to finish a service request"""
    try:
        user_id = get_jwt_identity()  # Get logged-in user's ID
        professional = Users.query.filter_by(user_id=user_id).first()
        professional_id = Professional.query.filter_by(user_id=professional.user_id).first().professional_id

        service_request = Request.query.filter_by(request_id=request_id, professional_id=professional_id).first()
        if not service_request:
            return jsonify({"error": "Request not found or not assigned to you"}), 404

        if service_request.status in ["Finished","Abandoned"]:
            return jsonify({"error": "Request is already processed"}), 400

        service_request.status = "Abandoned"
        service_request.date_completed = datetime.now()
        db.session.commit()

        return jsonify({"message": "Service request abandon successfully", "request_id": request_id}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/past-service-requests-customers', methods=['GET'])
@cache.cached(timeout=5)
@jwt_required()
def get_past_service_requests_customers():
    try:
        user_id = get_jwt_identity()
        print("user_id",user_id)
        user = Users.query.filter_by(user_id=user_id).first()

        if not user or user.role != "C":
            return jsonify({"error": "Customer not found"}), 404

        requests = Request.query.filter_by(user_id=user.user_id).all()
        request_list = [
            {
                "id": req.request_id,
                "user_id": req.user_id,
                "professional_id": req.professional_id,
                "service_type": req.service_type,
                "status": req.status,
                "date_created": req.date_created.strftime("%Y-%m-%d %H:%M:%S"),
                "date_completed": req.date_completed.strftime("%Y-%m-%d %H:%M:%S") if req.date_completed else None,
                "additional_details": req.additional_details
            }
            for req in requests
        ]

        # print("\npast services\n",jsonify(requests))
        return jsonify(request_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/create_service_request', methods=['POST'])
def create_service_request():
    data = request.json
    professional_id = data.get("professional_id")
    user_id = data.get("user_id")
    service_type = data.get("service_type") 
    additional_details = data.get("additional_details", "")


    user = Users.query.filter_by(user_id=user_id).first()
    print("User",user.username)  
    if not user or user.role != "C":
        return jsonify({"error": "Customer not found"}), 404
    

    if additional_details is None:
        additional_details = ""

    service = Service.query.filter_by(service_name=service_type).first()
    if not service:
        return jsonify({"error": "Service not found"}), 404
    
    service_id = service.service_id
    print("Professional ID",professional_id)
    print("User ID",user_id)
    print("Service ID",service_id)

    if not service_id:
        return jsonify({"error": "Service ID is required"}), 400

    # Check if the professional is already handling a request
    existing_request = Request.query.filter_by(professional_id=professional_id, status="Pending").first()
    if existing_request:
        return jsonify({"error": "Professional is already handling another request!"}), 400  

    # Create new request
    new_request = Request(
        professional_id=professional_id,
        user_id=user_id,
        service_id=service_id,  # Ensure it's stored
        additional_details=additional_details,
        status="Pending",
        service_type=service_type,
    )
    db.session.add(new_request)
    db.session.commit()

    return jsonify({"message": "Service request created successfully!"}), 201


@app.route('/api/check_professional_pending/<int:professional_id>', methods=['GET'])
def check_professional_pending(professional_id):
    # Check if the professional has any pending request
    professional_has_pending = Request.query.filter_by(professional_id=professional_id, status="Pending").first()

    return jsonify({
        "professional_has_pending": bool(professional_has_pending)
    }), 200


@app.route("/api/get-reviews/<int:professional_id>", methods=["GET"])
@jwt_required()
def get_reviews(professional_id):
    try:
        reviews = Review.query.filter_by(professional_id=professional_id).all()

        if not reviews:
            return jsonify({"message": "No reviews found"}), 404

        return jsonify([
            {
                "review_id": review.review_id,
                "user_id": review.user_id,
                "rating": review.rating,
                "review": review.review
            }
            for review in reviews
        ]), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@app.route("/api/submit-review", methods=["POST"])
@jwt_required()
def submit_review():
    print("Attempting to review")
    try:
        user_id = get_jwt_identity()  # Get the logged-in user ID
        data = request.json
        professional_id = data.get("professional_id")
        rating = data.get("rating")
        review_text = data.get("review")

        if not professional_id or not rating:
            return jsonify({"message": "Missing required fields"}), 400
        
        review = Review.query.filter_by(user_id=user_id, professional_id=professional_id).first()
        if review:
            review.rating = rating
            review.review = review_text
            db.session.commit()
            return jsonify({"message": "Review updated successfully!"}), 200

        new_review = Review(
            user_id=user_id,
            professional_id=professional_id,
            rating=rating,
            review=review_text
        )

        db.session.add(new_review)
        db.session.commit()

        return jsonify({"message": "Review submitted successfully!"}), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 500




@app.route('/api/professional_rating/<int:professional_id>', methods=['GET'])
@jwt_required()
def get_professional_rating(professional_id):
    professional = Professional.query.get(professional_id)
    if not professional:
        return jsonify({"error": "Professional not found"}), 404
    
    rating = professional.rating  # Assuming the rating is stored in the database
    return jsonify({"rating": rating})

@app.route("/api/block_user/<int:user_id>", methods=["POST"])
def block_user(user_id):

    user = Users.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    user.blocked = not user.blocked  # Toggle block status
    db.session.commit()

    return jsonify({
        "success": True,
        "message": f"User {user.username} {'blocked' if user.blocked else 'unblocked'} successfully.",
        "blocked": user.blocked  # Send the updated blocked status
    })


if __name__ == "__main__":
    app.run(debug=True,ssl_context=('cert.pem', 'key.pem')) 