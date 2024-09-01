from sanic import Blueprint
from sanic.response import json
from sqlalchemy.orm import Session
from models.api_key import ApiKey
from sanic_ext import openapi
import secrets

api_key_blueprint = Blueprint('api_key_blueprint', url_prefix='/api/keys')

@api_key_blueprint.post('/')
@openapi.summary("Create a new API key")
@openapi.description("Create a new API key")
@openapi.body({"description": str})
@openapi.response(201, {"message": str, "api_key": ApiKey.to_dict()}, "API key created successfully")
@openapi.response(400, {"error": str}, "Bad request")
async def create_api_key(request):
    """
    Create a new API key.
    """
    session: Session = request.app.ctx.db_session()
    try:
        data = request.json
        new_key = secrets.token_urlsafe(32)
        api_key = ApiKey(key=new_key, description=data.get('description', ''))
        session.add(api_key)
        session.commit()
        return json({"message": "API key created successfully", "api_key": api_key.to_dict()}, status=201)
    except Exception as e:
        session.rollback()
        return json({"error": str(e)}, status=400)
    finally:
        session.close()

@api_key_blueprint.get('/')
@openapi.summary("Get all API keys")
@openapi.description("Retrieve all API keys")
@openapi.response(200, [ApiKey.to_dict()], "List of all API keys")
async def get_all_api_keys(request):
    """
    Retrieve all API keys.
    """
    session: Session = request.app.ctx.db_session()
    try:
        api_keys = session.query(ApiKey).all()
        return json([key.to_dict() for key in api_keys])
    finally:
        session.close()

@api_key_blueprint.delete('/<key_id:int>')
@openapi.summary("Delete an API key")
@openapi.description("Delete an existing API key")
@openapi.parameter("key_id", int, "path", required=True)
@openapi.response(200, {"message": str}, "API key deleted successfully")
@openapi.response(404, {"error": str}, "API key not found")
@openapi.response(400, {"error": str}, "Bad request")
async def delete_api_key(request, key_id):
    """
    Delete an existing API key.
    """
    session: Session = request.app.ctx.db_session()
    try:
        api_key = session.query(ApiKey).get(key_id)
        if not api_key:
            return json({"error": "API key not found"}, status=404)
        session.delete(api_key)
        session.commit()
        return json({"message": "API key deleted successfully"})
    except Exception as e:
        session.rollback()
        return json({"error": str(e)}, status=400)
    finally:
        session.close()