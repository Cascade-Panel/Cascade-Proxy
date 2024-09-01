import os

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///nginx_proxy.db")

# Nginx configuration
NGINX_CONF_PATH = "/etc/nginx/nginx.conf"
SITES_AVAILABLE_PATH = "/etc/nginx/sites-available"
SITES_ENABLED_PATH = "/etc/nginx/sites-enabled"

# Certbot configuration
CERTBOT_PATH = "/usr/bin/certbot"

# Logging configuration
LOG_FILE_PATH = "/var/log/nginx_proxy_api.log"

# API Key configuration
DEFAULT_API_KEY = os.getenv("DEFAULT_API_KEY", "your-default-api-key-here")