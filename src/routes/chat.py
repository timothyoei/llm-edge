from flask import Blueprint, request, jsonify
from utils import get_model

chat_bp = Blueprint("chat", __name__)
@chat_bp.route("/chat", methods=["POST"])
def chat():
  if request.method == "POST":
    return chat_post_handler()

def chat_post_handler():
  data = request.get_json()
  if not data:
    return jsonify({"error": "Data missing"}), 400
  req_fields = ["system_msg", "prompt"]
  if not validate_req_fields(req_fields, data):
    return jsonify({"error": "Required field missing"}), 400
  return jsonify({"response": gen_response(data["system_msg"], data["prompt"])}), 201
  
def validate_req_fields(req_fields, data):
  for f in req_fields:
    if not data.get(f):
      return False
  return True