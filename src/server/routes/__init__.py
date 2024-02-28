def register_routes(app, api_url_prefix):
  from .users import users_bp
  from .sessions import sessions_bp
  from .chats import chats_bp

  app.register_blueprint(users_bp, url_prefix=api_url_prefix)
  app.register_blueprint(sessions_bp, url_prefix=api_url_prefix)
  app.register_blueprint(chats_bp, url_prefix=api_url_prefix)