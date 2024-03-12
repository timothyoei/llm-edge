from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required
from utils import get_db, crypter_encrypt, crypter_decrypt, crypter_decrypt_user

sessions_bp = Blueprint("sessions", __name__)

@sessions_bp.route("/sessions", methods=["POST"])
def sessions():
  """
  Endpoint for sessions
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
    200:
      description: Session creation successful
      schema:
        type: object
        properties:
          user:
            type: object
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
          token:
            type: string
            description: The user's authentication token
    400:
      description: Missing required data
      schema:
        properties:
          error:
            type: string
            description: Error message
    401:
      description: Password mismatch
      schema:
        properties:
          error:
            type: string
            description: Error message
    404:
      description: User does not exist
      schema:
        properties:
          error:
            type: string
            description: Error message
  """
  if request.method == "POST":
    return sessions_post_handler()

def sessions_post_handler():
  # Validate incoming data
  data = request.get_json()
  if not data:
    return jsonify({"error": "Data missing"}), 400
  req_fields = ["username", "password"]
  for f in req_fields:
    if not data.get(f):
      return jsonify({"error": f"{f} field missing"}), 400

  # Check if the user exists
  db = get_db()
  username = data["username"]
  if username not in db["users"]:
    return jsonify({"error": "User does not exist"}), 404

  # Check if the password matches
  user = db["users"][username]
  if not data["password"] == crypter_decrypt(user["password"]):
    return jsonify({"error": "Password does not match"}), 401

  # Create jwt
  access_token = create_access_token(identity=username)

  # Delete unnecessary fields before sending response
  del_fields = ["password"]
  for f in del_fields:
    user.pop(f)

  return jsonify({"user": crypter_decrypt_user(user), "token": access_token}), 200