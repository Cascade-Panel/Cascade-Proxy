from sanic import Blueprint
from sanic.response import json
from sqlalchemy.orm import Session
from models.proxy import Proxy
from services.nginx_service import NginxService
from services.certbot_service import CertbotService
from sanic_ext import openapi

proxy_blueprint = Blueprint('proxy_blueprint', url_prefix='/api/proxies')

@proxy_blueprint.post('/')
@openapi.summary("Create a new proxy")
@openapi.description("Create a new proxy configuration")
@openapi.parameter("X-API-Key", str, "header", required=True)
@openapi.body({"old_ip": str, "old_port": int, "new_domain": str, "https_enabled": bool})
@openapi.response(201, {"message": str, "proxy": Proxy.to_dict()}, "Proxy created successfully")
@openapi.response(400, {"error": str}, "Bad request")
async def create_proxy(request):
    """
    Create a new proxy configuration.
    """
    data = request.json
    session: Session = request.app.ctx.db_session()

    try:
        new_proxy = Proxy(
            old_ip=data['old_ip'],
            old_port=data['old_port'],
            new_domain=data['new_domain'],
            https_enabled=data.get('https_enabled', False)
        )
        session.add(new_proxy)
        session.commit()

        nginx_service = NginxService()
        nginx_service.create_proxy(new_proxy)

        if new_proxy.https_enabled:
            certbot_service = CertbotService()
            certbot_service.obtain_certificate(new_proxy.new_domain)

        return json({"message": "Proxy created successfully", "proxy": new_proxy.to_dict()}, status=201)
    except Exception as e:
        session.rollback()
        return json({"error": str(e)}, status=400)
    finally:
        session.close()

@proxy_blueprint.get('/')
@openapi.summary("Get all proxies")
@openapi.description("Retrieve all proxy configurations")
@openapi.parameter("X-API-Key", str, "header", required=True)
@openapi.response(200, [Proxy.to_dict()], "List of all proxies")
async def get_all_proxies(request):
    """
    Retrieve all proxy configurations.
    """
    session: Session = request.app.ctx.db_session()
    try:
        proxies = session.query(Proxy).all()
        return json([proxy.to_dict() for proxy in proxies])
    finally:
        session.close()

@proxy_blueprint.get('/<proxy_id:int>')
@openapi.summary("Get a specific proxy")
@openapi.description("Retrieve a specific proxy configuration by ID")
@openapi.parameter("X-API-Key", str, "header", required=True)
@openapi.parameter("proxy_id", int, "path", required=True)
@openapi.response(200, Proxy.to_dict(), "Proxy details")
@openapi.response(404, {"error": str}, "Proxy not found")
async def get_proxy(request, proxy_id):
    """
    Retrieve a specific proxy configuration by ID.
    """
    session: Session = request.app.ctx.db_session()
    try:
        proxy = session.query(Proxy).get(proxy_id)
        if proxy:
            return json(proxy.to_dict())
        return json({"error": "Proxy not found"}, status=404)
    finally:
        session.close()

@proxy_blueprint.put('/<proxy_id:int>')
@openapi.summary("Update a proxy")
@openapi.description("Update an existing proxy configuration")
@openapi.parameter("X-API-Key", str, "header", required=True)
@openapi.parameter("proxy_id", int, "path", required=True)
@openapi.body({"old_ip": str, "old_port": int, "new_domain": str, "https_enabled": bool})
@openapi.response(200, {"message": str, "proxy": Proxy.to_dict()}, "Proxy updated successfully")
@openapi.response(404, {"error": str}, "Proxy not found")
@openapi.response(400, {"error": str}, "Bad request")
async def update_proxy(request, proxy_id):
    """
    Update an existing proxy configuration.
    """
    data = request.json
    session: Session = request.app.ctx.db_session()
    try:
        proxy = session.query(Proxy).get(proxy_id)
        if not proxy:
            return json({"error": "Proxy not found"}, status=404)

        proxy.old_ip = data.get('old_ip', proxy.old_ip)
        proxy.old_port = data.get('old_port', proxy.old_port)
        proxy.new_domain = data.get('new_domain', proxy.new_domain)
        proxy.https_enabled = data.get('https_enabled', proxy.https_enabled)

        session.commit()

        nginx_service = NginxService()
        nginx_service.update_proxy(proxy)

        if proxy.https_enabled and not data.get('https_enabled', True):
            certbot_service = CertbotService()
            certbot_service.revoke_certificate(proxy.new_domain)
        elif not proxy.https_enabled and data.get('https_enabled', False):
            certbot_service = CertbotService()
            certbot_service.obtain_certificate(proxy.new_domain)

        return json({"message": "Proxy updated successfully", "proxy": proxy.to_dict()})
    except Exception as e:
        session.rollback()
        return json({"error": str(e)}, status=400)
    finally:
        session.close()

@proxy_blueprint.delete('/<proxy_id:int>')
@openapi.summary("Delete a proxy")
@openapi.description("Delete an existing proxy configuration")
@openapi.parameter("X-API-Key", str, "header", required=True)
@openapi.parameter("proxy_id", int, "path", required=True)
@openapi.response(200, {"message": str}, "Proxy deleted successfully")
@openapi.response(404, {"error": str}, "Proxy not found")
@openapi.response(400, {"error": str}, "Bad request")
async def delete_proxy(request, proxy_id):
    """
    Delete an existing proxy configuration.
    """
    session: Session = request.app.ctx.db_session()
    try:
        proxy = session.query(Proxy).get(proxy_id)
        if not proxy:
            return json({"error": "Proxy not found"}, status=404)

        nginx_service = NginxService()
        nginx_service.delete_proxy(proxy)

        if proxy.https_enabled:
            certbot_service = CertbotService()
            certbot_service.revoke_certificate(proxy.new_domain)

        session.delete(proxy)
        session.commit()

        return json({"message": "Proxy deleted successfully"})
    except Exception as e:
        session.rollback()
        return json({"error": str(e)}, status=400)
    finally:
        session.close()