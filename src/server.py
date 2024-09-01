from sanic import Sanic
from sanic.response import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sanic_openapi import openapi
from config import DATABASE_URL, DEFAULT_API_KEY
from routes.proxy_blueprint import proxy_blueprint
from routes.api_key_blueprint import api_key_blueprint
from utils.error_handler import setup_error_handlers
from models.api_key import ApiKey

app = Sanic("NginxProxyAPI")
openapi.blueprint.url_prefix = "/api/docs"
app.blueprint(openapi.blueprint)

# Database setup
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
app.ctx.db_session = Session

# Register blueprints
app.blueprint(proxy_blueprint)
app.blueprint(api_key_blueprint)

# Setup error handlers
setup_error_handlers(app)

@app.middleware('request')
async def authenticate(request):
    """
    Middleware to authenticate API requests using API keys.
    
    Excludes /api/status and /api/keys routes from authentication.
    """
    if request.path == '/api/status' or request.path.startswith('/api/keys') or request.path.startswith('/api/docs'):
        return
    api_key = request.headers.get('X-API-Key')
    if not api_key:
        return json({"error": "API key is required"}, status=401)
    if api_key == DEFAULT_API_KEY:
        return
    session = Session()
    try:
        key = session.query(ApiKey).filter_by(key=api_key, is_active=True).first()
        if not key:
            return json({"error": "Invalid API key"}, status=401)
    finally:
        session.close()

@app.get("/api/status")
@openapi.summary("Get API status")
@openapi.response(200, {"status": str}, "API status")
async def status(request):
    """
    Get the current status of the API.
    """
    return json({"status": "OK"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)