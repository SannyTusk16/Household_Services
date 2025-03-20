class Config:
    SECRET_KEY = 'TANGO_DESERVED_BETTER'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CELERY_BROKER_URL = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/0"
    GOOGLE_CHAT_WEBHOOK_URL = "https://chat.googleapis.com/v1/spaces/XXXXXX/messages"
    MAIL_SENDER = "your-email@example.com"
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "your-email@example.com"
    MAIL_PASSWORD = "your-email-password"



    DEBUG = True