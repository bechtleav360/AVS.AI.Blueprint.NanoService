import logging

from fastapi import FastAPI
from fastapi.routing import APIRoute, Mount
from starlette.responses import HTMLResponse

from src.config.config import ConfigurationManager
from src.controller.blueprint import BaseController


class StartController(BaseController):

    def __init__(self, settings: ConfigurationManager):
        super().__init__(settings)
        self.logger = logging.getLogger("api.start")

    async def show_welcome(self) -> HTMLResponse:
        """
        Shows a simple welcome screen explaining what this service does
        and lists all available routes
        """
        # Get all registered routes and format them into a string
        routes = []
        # Handle different types of route objects in FastAPI
        for route in self.app.routes:
            if isinstance(route, APIRoute):
                methods = [method for method in route.methods]
                summary = f" - {route.summary}" if route.summary else ""
                routes.append(
                    f"{route.name or 'unnamed'}: {', '.join(methods)} {route.path}{summary}"
                )
            elif isinstance(route, Mount):
                routes.append(f"MOUNT: {route.path} → {route.name}")
            else:
                # Fallback for any other route types
                routes.append(f"ROUTE: {str(route)}")

        # Sort routes for better readability
        routes.sort()

        # Get app info from settings
        app_name = self.settings.get_config("app_name", "FastAPI Application")
        app_description = self.settings.get_config("app_description", "")
        app_version = self.settings.get_config("app_version", "0.1.0")

        html_content = f"""
            <html>
                <head>
                    <title>{app_name} v{app_version}</title>
                    <style>
                        body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
                        .header {{ margin-bottom: 30px; }}
                        .description {{ color: #666; margin: 10px 0 20px 0; }}
                        .routes {{ background: #f5f5f5; padding: 15px; border-radius: 5px; }}
                        pre {{ margin: 0; white-space: pre-wrap; }}
                    </style>
                </head>
                <body>
                    <div class="header">
                        <h1>{app_name} <small>v{app_version}</small></h1>
                        {f'<div class="description">{app_description}</div>' if app_description else ''}
                    </div>
                    <h2>Available Routes</h2>
                    <div class="routes">
                        <pre>{chr(10).join(routes)}</pre>
                    </div>
                </body>
            </html>
        """

        return HTMLResponse(content=html_content)

    def register_routes(self, app: FastAPI, url_prefix: str = "") -> None:
        """Register the welcome page route

        Args:
            app: The FastAPI application instance
            url_prefix: URL prefix for the routes
        """
        self.app = app

        app.add_api_route(
            path=f"{url_prefix}/",
            endpoint=self.show_welcome,
            methods=["GET"],
            response_class=HTMLResponse,
            summary="Welcome Page",
            description="Shows a simple welcome screen explaining what this service does",
            tags=["info"],
        )
