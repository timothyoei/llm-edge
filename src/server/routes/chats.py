from flask import Blueprint, request, jsonify
from utils import get_db, write_db, gen_response, crypter_encrypt, crypter_decrypt
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from

chats_bp = Blueprint("chats", __name__)

@chats_bp.route("/chats", methods=["GET", "POST"])
@jwt_required()
@swag_from("../docs/chats_get.yml")
@swag_from("../docs/chats_post.yml")
def chats():
  db = get_db()
  if request.method == "GET":
    return chats_get_handler(db)
  elif request.method == "POST":
    return chats_post_handler(db)

def chats_get_handler(db):
  username = get_jwt_identity()
  if username not in db["users"]:
    return jsonify({"error": "User not found"}), 400
  return jsonify({"chats": db["users"][username]["chats"]}), 200

def chats_post_handler(db):
  # Validate incoming data
  username = get_jwt_identity()
  if username not in db["users"]:
    return jsonify({"error": "User not found"}), 400

  # Insert new chat
  new_chat = {
    "title": "TEST TITLE",
    "history": []
  }
  db["users"][username]["chats"].append(new_chat)
  write_db(db)

  return jsonify(new_chat), 201

@chats_bp.route("/chats/<int:chat_idx>", methods=["GET", "POST", "DELETE"])
@jwt_required()
def chat(chat_idx):
  """
  Endpoint for a single chat
  ---
  parameters:
    - in: path
      name: chat_id
      required: true
      description: The ID of the chat to retrieve
      type: string
    - in: header
      name: Authorization
      required: true
      description: The JWT token for the user that this chat belongs to
      type: string
      default: Bearer JWT_TOKEN
  responses:
    200:
      description: Chat details
      schema:
        properties:
          _id:
            type: string
            description: The chat's unique ID
          title:
            type: string
            description: The title of the chat
          email:
            type: string
            description: The email that this chat belongs to
          history:
            type: array
            items:
              type: object
              properties:
                query:
                  type: string
                  description: The input to the model
                response:
                  type: string
                  description: The output of the model
    204:
      description: Chat details
      schema:
        type: object
        properties:
          message:
            type: string
            description: Deletion result
  """
  db = get_db()
  if request.method == "GET":
    return chat_get_handler(chat_idx, db)
  elif request.method == "POST":
    return chat_post_handler(chat_idx, db)
  elif request.method == "DELETE":
    return chat_delete_handler(chat_idx, db)

def chat_get_handler(chat_idx, db):
  # Verify identity
  username = get_jwt_identity()
  if username not in db["users"]:
    return jsonify({"error": "User not found"}), 400

  # Check if chat exists
  if chat_idx >= len(db["users"][username]["chats"]):
    return jsonify({"error": "Chat not found"}), 400

  return db["users"][username]["chats"][chat_idx], 200

def chat_post_handler(chat_idx, db):
  # Validate incoming data
  data = request.get_json()
  if not data:
    return jsonify({"error": "Data missing"}), 400
  req_fields = ["query"]
  for f in req_fields:
    if not data.get(f):
      return jsonify({"error": f"{f} field missing"}), 400  

  # Verify identity
  username = get_jwt_identity()
  if username not in db["users"]:
    return jsonify({"error": "User not found"}), 400

  # Check if chat exists
  chats = db["users"][username]["chats"]
  if chat_idx >= len(chats):
    return jsonify({"error": "Chat not found"}), 400

  # Add new chat to history
  res = gen_response(crypter_decrypt(db["users"][username]["system_msg"]), data["query"])
  new_chat = {
    "query": crypter_encrypt(data["query"]),
    "response": crypter_encrypt(res)
  }
  chats[chat_idx]["history"].append(new_chat)
  write_db(db)
  return jsonify({"response": res}), 200

def chat_delete_handler(chat_idx, db):
  # Verify identity
  username = get_jwt_identity()
  if username not in db["users"]:
    return jsonify({"error": "User not found"}), 400

  # Check if chat exists
  if chat_idx >= len(db["users"][username]["chats"]):
    return jsonify({"error": "Chat not found"}), 400

  # Delete chat
  db["users"][username]["chats"].pop(chat_idx)
  write_db(db)
  return jsonify({"message": "Successfully deleted chat"}), 200