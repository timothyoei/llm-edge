from flask import Flask, current_app, g
from flasgger import Swagger
import os
from dotenv import load_dotenv
from routes import register_routes
import json
from flask_jwt_extended import JWTManager
from datetime import timedelta
from cryptography.fernet import Fernet

# ============================================
# AUTHORIZATION HELPERS
# ============================================

def config_auth(app, key):
  app.config["JWT_SECRET_KEY"] = key
  app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
  jwt = JWTManager(app)

# ============================================
# CRYPTOGRAPHY HELPERS
# ============================================
def init_crypter(app, key):
  app.config["API_CRYPT_KEY"] = key
  with app.app_context():
    crypter = get_crypter()

def get_crypter():
  if "crypter" not in g:
    g.crypter = Fernet(current_app.config["API_CRYPT_KEY"])
  return g.crypter

def crypter_encrypt(data):
  return get_crypter().encrypt(data.encode()).decode()

def crypter_decrypt(data):
  return get_crypter().decrypt(data).decode()

# ============================================
# DATABASE HELPERS
# ============================================
def init_db(app, db_path):
  app.config["API_DB_PATH"] = db_path
  with app.app_context():
    db = get_db()

def get_db():
  if "db" not in g:
    with open(current_app.config["API_DB_PATH"], "r") as f:
      g.db = json.load(f)
      if g.db == None:
        print("Error loading database")
  return g.db

def write_db(new_db):
  for key, value in new_db.items():
    if isinstance(value, bytes):
        data[key] = value.decode('utf-8')
  with open(current_app.config["API_DB_PATH"], "w") as f:
    json.dump(new_db, f, indent=4)

# ============================================
# MODEL HELPERS
# ============================================

def init_model(app):
  return

def get_model():
  return

def gen_response(system_msg, prompt):
  # GENERATE RESPONSE HERE
  return "TEST RESPONSE"

# ============================================
# INITIALIZATION HELPER
# ============================================

def init_app():
  load_dotenv()

  app = Flask(os.getenv("API_NAME"))
  app.config["API_PORT"] = os.getenv("API_PORT")
  init_db(app, "data/data.json" if os.getenv("API_ENV", "DEV") == "PROD" else "src/server/data/data.json")
  config_auth(app, os.getenv("API_JWT_KEY"))
  init_crypter(app, os.getenv("API_CRYPT_KEY"))
  init_model(app)
  swagger = Swagger(app)
  register_routes(app, os.getenv("API_URL_PREFIX"))

  return app