# Cascade-Proxy

Cascade-Proxy is a powerful and flexible Nginx reverse proxy management system designed to work seamlessly with Cascade, a comprehensive docker container, system container, and VM management platform. While it's optimized for integration with Cascade, Cascade-Proxy can also be used as a standalone solution for managing Nginx reverse proxies.

## Features

- RESTful API for managing Nginx reverse proxy configurations
- Automatic SSL/TLS certificate management using Certbot
- API key authentication for secure access
- Integration with Nginx for real-time configuration updates
- Supports both HTTP and HTTPS proxying
- Designed for easy integration with Cascade platform
- Can be used as a standalone proxy management solution

## Prerequisites

- Python 3.7+
- Nginx
- Certbot
- SQLite (default) or any SQLAlchemy-supported database

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-repo/cascade-proxy.git
   cd cascade-proxy
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Update `config.py`:

4. Initialize the database:
   ```
   python init_db.py
   ```

5. Start the Cascade-Proxy service:
   ```
   python app.py
   ```

## Usage

### API Endpoints

- `GET /api/status`: Check the status of the API (no authentication required)
- `POST /api/proxies`: Create a new proxy configuration
- `GET /api/proxies`: List all proxy configurations
- `GET /api/proxies/<id>`: Get details of a specific proxy configuration
- `PUT /api/proxies/<id>`: Update a proxy configuration
- `DELETE /api/proxies/<id>`: Delete a proxy configuration
- `POST /api/keys`: Create a new API key
- `GET /api/keys`: List all API keys
- `DELETE /api/keys/<id>`: Delete an API key

### Authentication

All endpoints (except `/api/status`) require an API key to be included in the `X-API-Key` header of the request.

### OpenAPI Documentation

Access the OpenAPI documentation at `http://your-server:8000/swagger` for detailed information about the API endpoints and their usage.

## Integration with Cascade

Cascade-Proxy is designed to integrate seamlessly with the Cascade platform. When used in conjunction with Cascade, it provides automated proxy management for your containers and VMs. Refer to the Cascade documentation for specific integration instructions.

## Standalone Usage

While optimized for use with Cascade, Cascade-Proxy can be used as a standalone solution for managing Nginx reverse proxies. Simply run the service and use the API endpoints to manage your proxy configurations.

## Contributing

Contributions to Cascade-Proxy are welcome! Please refer to our [Contributing Guidelines](CONTRIBUTING.md) for more information.

## License

Cascade-Proxy is released under the [MIT License](LICENSE).

## Support

For issues, feature requests, or questions, please open an issue in the GitHub repository or contact our support team at support@cascade-platform.com.

---

Cascade-Proxy - Simplifying reverse proxy management for the Cascade platform and beyond.