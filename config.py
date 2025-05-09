import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev_key_123')
    SQLALCHEMY_DATABASE_URI = "postgresql://neondb_owner:npg_Ehia6WBT7eIf@ep-young-field-a4p3qt3t-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key-123')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)