from flask import Blueprint, request, jsonify
from utils import get_db, write_db, crypter_encrypt, crypter_decrypt

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
      description: Bad request
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
  if request.method == "POST":
    return users_post_handler()

def users_post_handler():
  # Validate incoming data
  data = request.get_json()
  if not data:
    return jsonify({"error": "Data missing"}), 400
  req_fields = ["username", "password"]
  for f in req_fields:
    if not data.get(f):
      return jsonify({"error": f"{f} field missing"}), 400

  # Check if the username is already taken
  db = get_db()
  if data["username"] in db["users"]:
    return jsonify({"error": "Username already taken"}), 400

  # Create a new user
  new_user = {
    "password": crypter_encrypt(data["password"]),
    "theme": "dark",
    "chats": [],
    "system_msg": crypter_encrypt("TEST SYSTEM MESSAGE")
  }
  db["users"][data["username"]] = new_user
  write_db(db)

  # Remove unnecessary fields from response
  del_fields = ["password"]
  for f in del_fields:
    new_user.pop(f)
  
  return new_user, 201