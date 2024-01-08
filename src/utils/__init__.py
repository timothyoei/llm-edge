from flask import Flask, current_app, g
import os
from dotenv import load_dotenv
from routes import register_routes

# ============================================
# INITIALIZATION HELPER
# ============================================

def init_model(app):
  # INITIALIZE MODEL HERE

def get_model():
  # RETURN MODEL HERE

def gen_response(system_msg, prompt):
  # GENERATE RESPONSE HERE

def init_app():
  load_dotenv()

  app = Flask(__name__)
  # init_model(app)
  register_routes(app, os.getenv("API_URL_PREFIX"))

  return app