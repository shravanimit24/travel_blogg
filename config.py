import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///travel_blog.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TEMPLATES_AUTO_RELOAD = True
    JINJA_AUTO_RELOAD = True

    # Google Maps API Key - set in environment variables
    GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY') or 'YOUR_GOOGLE_MAPS_API_KEY'

    # Payment link
    PAYMENT_LINK = os.environ.get('PAYMENT_LINK') or 'https://buy.stripe.com/your_link'

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    # In production, ensure these are set via environment variables
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}