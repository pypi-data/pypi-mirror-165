from requests import Session
from typing import Dict
from logging import raiseExceptions

from .Config import Config

class Requests:
    """Class for the request"""
    def __init__(self):
        self.url = Config.BASE_URL
        try:
            self.session = Session()
        except Exception as e:
            raiseExceptions(f"Could not create Session Object: {e}")

    def get_ip(self) -> Dict[str, object]:
        """Get your current public IP-Adresse"""
        response = self.session.get(self.url)
        return response.json()