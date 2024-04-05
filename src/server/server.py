from utils import init_app

app = init_app()

if __name__ == "__main__":
  app.run(port=app.config["API_PORT"])