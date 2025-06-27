import logging

from fastapi import FastAPI
from fastapi.routing import APIRoute, Mount
from starlette.responses import HTMLResponse

from src.api.base_controller import BaseController
from src.config.config import ConfigurationManager

SETTINGS = ConfigurationManager()


class StartController(BaseController):
    def __init__(self):
        self.logger = logging.getLogger("api.start")
        self.app = None

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
                routes.append(f"{route.name or 'unnamed'}: {', '.join(methods)} {route.path}{summary}")
            elif isinstance(route, Mount):
                routes.append(f"MOUNT: {route.path} → {route.name}")
            else:
                # Fallback for any other route types
                routes.append(f"ROUTE: {str(route)}")

        # Sort routes for better readability
        routes.sort()

        html_content = f"""
            <html>
                <body>
                    <h1>Python Fast API Template</h1>
                    <h2>Available routes:</h2>
                    <pre>{chr(10).join(routes)}</pre>
                </body>
            </html>
        """

        return HTMLResponse(content=html_content)

    def register_routes(self, app: FastAPI, url_prefix: str = ""):
        """Register the welcome page route"""
        self.app = app

        app.add_api_route(
            path=f"{url_prefix}/",
            endpoint=self.show_welcome,
            methods=["GET"],
            response_class=HTMLResponse,
            summary="Welcome Page",
            description="Shows a simple welcome screen explaining what this service does",
            tags=["info"]
        )
