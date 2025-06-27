from abc import ABC, abstractmethod
from fastapi import FastAPI


class BaseController(ABC):
    """Base controller class that all controllers should inherit from"""

    @abstractmethod
    def register_routes(self, app: FastAPI, url_prefix: str=""):
        pass
