import subprocess
from config import CERTBOT_PATH

class CertbotService:
    """
    Service class for managing SSL certificates using Certbot.
    """

    def __init__(self):
        """
        Initialize the CertbotService with the Certbot path.
        """
        self.certbot_path = CERTBOT_PATH

    def obtain_certificate(self, domain):
        """
        Obtain an SSL certificate for a domain using Certbot.

        Args:
            domain (str): The domain to obtain the certificate for.

        Raises:
            Exception: If certificate obtaining fails.
        """
        try:
            subprocess.run([
                self.certbot_path, 'certonly',
                '--nginx',
                '-d', domain,
                '--non-interactive',
                '--agree-tos',
                '--email', 'admin@example.com'  # Replace with your email
            ], check=True)
        except subprocess.CalledProcessError as e:
            raise Exception(f"Failed to obtain certificate for {domain}: {str(e)}")

    def revoke_certificate(self, domain):
        """
        Revoke an SSL certificate for a domain using Certbot.

        Args:
            domain (str): The domain to revoke the certificate for.

        Raises:
            Exception: If certificate revocation fails.
        """
        try:
            subprocess.run([
                self.certbot_path, 'revoke',
                '--cert-name', domain,
                '--non-interactive'
            ], check=True)
        except subprocess.CalledProcessError as e:
            raise Exception(f"Failed to revoke certificate for {domain}: {str(e)}")