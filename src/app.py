"""This file serves the web app"""

from fastapi import FastAPI

from src.config import logs
from src.config.config import ConfigurationManager
from src.api import configure_routes

SETTINGS = ConfigurationManager()

app: FastAPI = FastAPI(title="Template APP", description="An app template for python REST-API's", version="0.0.1")

logs.configure()

configure_routes(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.app:app", host="0.0.0.0", port=SETTINGS.get_config("api_port"), reload=True)
