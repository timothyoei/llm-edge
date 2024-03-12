from flask import Flask, current_app, g
from flasgger import Swagger
import os
from dotenv import load_dotenv
from routes import register_routes
import json
from flask_jwt_extended import JWTManager
from datetime import timedelta
from cryptography.fernet import Fernet
from flask_cors import CORS
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

# ============================================
# CORS HELPERS
# ============================================
def init_cors(app):
  CORS(app)

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

def crypter_decrypt_user(user):
  user["theme"] = crypter_decrypt(user["theme"])
  user["system_msg"] = crypter_decrypt(user["system_msg"])
  for chat in user["chats"]:
    chat["title"] = crypter_decrypt(chat["title"])
    for qa in chat["history"]:
      qa["query"] = crypter_decrypt(qa["query"])
      qa["response"] = crypter_decrypt(qa["response"])
  return user

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
  with open(current_app.config["API_DB_PATH"], "w") as f:
    json.dump(new_db, f, indent=4)

# ============================================
# MODEL HELPERS
# ============================================

def init_model(app, model_path):
  compute_dtype = getattr(torch, "float16")
  bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=False,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=compute_dtype
  )
  app.config["API_MODEL"] = AutoModelForCausalLM.from_pretrained(
    model_path,
    quantization_config=bnb_config,
    device_map="auto")
  app.config["API_MODEL_TOKENIZER"] = AutoTokenizer.from_pretrained(model_path)

def get_model():
  if "model" not in g:
    g.model = (current_app.config["API_MODEL"], current_app.config["API_MODEL_TOKENIZER"])
  return g.model

def gen_response(system_msg, prompt):
  # model, tokenizer = get_model()
  
  # input_ids = tokenizer(prompt, return_tensors="pt", truncation=True).input_ids
  # outputs = model.generate(
  #   input_ids=input_ids,
  #   max_new_tokens=200,
  #   temperature=0.1
  # )
  # result = tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]

  return "SIMULATED MODEL RESPONSE"

# ============================================
# INITIALIZATION HELPER
# ============================================

def init_app():
  load_dotenv()
  is_prod = os.getenv("API_IS_PROD", "FALSE") == "TRUE"

  app = Flask(os.getenv("API_NAME"))
  app.config["API_PORT"] = os.getenv("API_PORT")

  data_path = "data/data.json" if is_prod else "src/server/data/data.json"
  init_db(app, data_path)

  init_cors(app)

  config_auth(app, os.getenv("API_JWT_KEY"))

  init_crypter(app, os.getenv("API_CRYPT_KEY"))

  model_path = "model" if is_prod else "src/server/model"
  # init_model(app, model_path)

  swagger = Swagger(app)

  register_routes(app, os.getenv("API_URL_PREFIX"))

  return app