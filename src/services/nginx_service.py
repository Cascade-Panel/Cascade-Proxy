import os
from config import NGINX_CONF_PATH, SITES_AVAILABLE_PATH, SITES_ENABLED_PATH
from models.proxy import Proxy

class NginxService:
    """
    Service class for managing Nginx configurations.
    """

    def __init__(self):
        """
        Initialize the NginxService with configuration paths.
        """
        self.nginx_conf_path = NGINX_CONF_PATH
        self.sites_available_path = SITES_AVAILABLE_PATH
        self.sites_enabled_path = SITES_ENABLED_PATH

    def create_proxy(self, proxy: Proxy):
        """
        Create a new Nginx proxy configuration.

        Args:
            proxy (Proxy): The proxy configuration to create.
        """
        config = self._generate_proxy_config(proxy)
        site_config_path = os.path.join(self.sites_available_path, f"{proxy.new_domain}.conf")
        
        with open(site_config_path, 'w') as f:
            f.write(config)

        # Create symlink in sites-enabled
        os.symlink(site_config_path, os.path.join(self.sites_enabled_path, f"{proxy.new_domain}.conf"))

        self._reload_nginx()

    def update_proxy(self, proxy: Proxy):
        """
        Update an existing Nginx proxy configuration.

        Args:
            proxy (Proxy): The updated proxy configuration.
        """
        self.delete_proxy(proxy)
        self.create_proxy(proxy)

    def delete_proxy(self, proxy: Proxy):
        """
        Delete an existing Nginx proxy configuration.

        Args:
            proxy (Proxy): The proxy configuration to delete.
        """
        site_config_path = os.path.join(self.sites_available_path, f"{proxy.new_domain}.conf")
        site_enabled_path = os.path.join(self.sites_enabled_path, f"{proxy.new_domain}.conf")

        if os.path.exists(site_config_path):
            os.remove(site_config_path)

        if os.path.exists(site_enabled_path):
            os.remove(site_enabled_path)

        self._reload_nginx()

    def _generate_proxy_config(self, proxy: Proxy):
        """
        Generate Nginx configuration for a proxy.

        Args:
            proxy (Proxy): The proxy configuration.

        Returns:
            str: The generated Nginx configuration.
        """
        config = f"""
server {{
    listen 80;
    server_name {proxy.new_domain};

    location / {{
        proxy_pass http://{proxy.old_ip}:{proxy.old_port};
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }}
}}
"""
        return config

    def _reload_nginx(self):
        """
        Reload the Nginx service.
        """
        os.system('nginx -s reload')