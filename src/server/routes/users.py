from flask import Blueprint, request, jsonify
from utils import get_db, write_db, crypter_encrypt, crypter_decrypt
from flask_jwt_extended import jwt_required, get_jwt_identity

users_bp = Blueprint("users", __name__)

@users_bp.route("/users", methods=["POST"])
def users():
  """
  Endpoint for users
  ---
  consumes:
    - application/json
  parameters:
    - in: body
      name: body
      required: true
      schema:
        required:
          - username
          - password
        properties:
          username:
            type: string
            description: The user's username
          password:
            type: string
            description: The user's password
  responses:
    201:
      description: User successfully created
      schema:
        properties:
          theme:
            type: string
            description: The user's theme preference
          system_msg:
            type: string
            description: The user's system message
          chats:
            type: array
            description: The user's chats
    400:
      description: Missing required data
      schema:
        properties:
          error:
            type: string
            description: Error message
    409:
      description: Username already taken
      schema:
        properties:
          error:
            type: string
            description: Error message
    500:
      description: Internal server error
      schema:
        properties:
          error:
            type: string
            description: Error message
  """
  data = request.get_json()
  if not data:
    return jsonify({"error": "Data missing"}), 400
  db = get_db()
  if request.method == "POST":
    return users_post_handler(data, db)

def users_post_handler(data, db):
  # Validate incoming data
  req_fields = ["username", "password"]
  for f in req_fields:
    if not data.get(f):
      return jsonify({"error": f"{f} field missing"}), 400

  # Check if the username is already taken
  if data["username"] in db["users"]:
    return jsonify({"error": "Username already taken"}), 409

  # Create a new user
  new_user = {
    "password": crypter_encrypt(data["password"]),
    "theme": crypter_encrypt("dark"),
    "system_msg": crypter_encrypt("TEST SYSTEM MESSAGE"),
    "chats": [],
  }
  db["users"][data["username"]] = new_user
  write_db(db)

  # Remove unnecessary fields from response
  del_fields = ["password"]
  for f in del_fields:
    new_user.pop(f)
  
  return new_user, 201

@users_bp.route("/users/user", methods=["PATCH", "DELETE"])
@jwt_required()
def user():
  # Verify identity
  username = get_jwt_identity()
  db = get_db()
  if username not in db["users"]:
    return jsonify({"error": "User not found"}), 404

  # Dispatch to request method handlers
  if request.method == "PATCH":
    return user_patch_handler(username, db)
  elif request.method == "DELETE":
    return user_delete_handler(username, db)

def user_patch_handler(username, db):
  # Validate incoming data
  data = request.get_json()
  if not data:
    return jsonify({"error": "Data missing"}), 400

  for f in data:
    if not data.get(f):
      return jsonify({"error": f"{f} field is not valid"}), 400
    else:
      db["users"][username][f] = crypter_encrypt(data[f])
  write_db(db)
  return jsonify({"message": "Successfully updated user"}), 200

def user_delete_handler(username, db):
  db["users"].pop(username, None)
  write_db(db)
  return jsonify({"message": "Successfully deleted user"}), 200