def register_routes(app, api_url_prefix):
  from .chat import chat_bp

  app.register_blueprint(chat_bp, url_prefix=api_url_prefix)