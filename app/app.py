from flask import got_request_exception
from app_factory import create_app
import os

app = create_app()

from routes import default_blueprint
app.register_blueprint(default_blueprint, url_prefix="/<string:namespace>")

if __name__ == '__main__':
  app.run(debug=True, host="0.0.0.0")
