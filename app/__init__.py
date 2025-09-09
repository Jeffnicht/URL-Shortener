from flask import Flask
import redis
from . import extensions 
import os
from dotenv import load_dotenv

def create_app():
    app = Flask(__name__)
    app.secret_key = 'superdupersecret'
    app.config['REDIS_URL'] = os.getenv("REDIS_URL", "redis://172.16.249.2:6379")
    extensions.redis_client = redis.Redis.from_url(app.config["REDIS_URL"], decode_responses=True)
    from .routes import register_routes
    register_routes(app)
    return app
