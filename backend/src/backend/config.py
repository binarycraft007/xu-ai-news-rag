import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'super-secret'
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LLAMA_SERVER_LLM_URL = os.environ.get('LLAMA_SERVER_LLM_URL')
    LLAMA_SERVER_EMBEDDING_URL = os.environ.get('LLAMA_SERVER_EMBEDDING_URL')
    LLAMA_SERVER_RERANKING_URL = os.environ.get('LLAMA_SERVER_RERANKING_URL')
    BING_API_KEY = os.environ.get('BING_API_KEY')
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
