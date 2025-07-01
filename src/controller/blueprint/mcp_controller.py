import logging

from fastapi import FastAPI

from fastapi_mcp import FastApiMCP

from src.config.config import ConfigurationManager
from src.config.params import ConfigParameter
from src.controller.blueprint import BaseController


class MCPController(BaseController):
    """Controller for Model Context Protocol (MCP) integration
    
    This controller integrates the FastAPI MCP library to enable AI assistants
    to interact with the API.
    """
    # Class variable to store the MCP instance
    _mcp_instance = None

    def __init__(self, settings: ConfigurationManager):
        super().__init__(settings)
        self.logger = logging.getLogger("api.mcp")

    def register_routes(self, app: FastAPI, url_prefix: str = "") -> None:
        """Register MCP routes and initialize the MCP instance

        Args:
            app: The FastAPI application instance
            url_prefix: URL prefix for the routes
        """
        # Check if MCP is enabled in configuration
        mcp_enabled = self.settings.get_config(ConfigParameter.APP_MCP, False)
        
        if not mcp_enabled:
            self.logger.info("MCP is disabled in configuration, skipping registration")
            return
            
        self.logger.info("Registering MCP routes")
        
        # Create MCP instance and store it as a class variable
        MCPController._mcp_instance = FastApiMCP(
            app, 
            url_prefix, 
            exclude_tags=["actuators", "info"]
        )
        
        # Mount the MCP routes
        MCPController._mcp_instance.mount()

    @classmethod
    def setup_server(cls):
        """Set up the MCP server after all routes have been registered"""
        if cls._mcp_instance:
            cls._mcp_instance.setup_server()