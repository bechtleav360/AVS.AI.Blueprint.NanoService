import importlib
import pkgutil
from typing import List, Type

from fastapi import FastAPI

from src.config import ConfigParameter, ConfigurationManager
from src.controller.blueprint import BaseController

# READ BEVOR CHANGING
# This file automatically imports all subclasses of BaseController and executes the "register_routes" method.
# Any class derived from BaseController, located in src.api, will automatically be imported and configured!


def _import_submodules(package_name: str):
    """Import all submodules of a module, recursively"""

    package = importlib.import_module(package_name)

    for _, name, is_pkg in pkgutil.iter_modules(
        package.__path__, package.__name__ + "."
    ):
        importlib.import_module(name)
        if is_pkg:
            _import_submodules(name)


def _get_all_subclasses(base_class: Type) -> List[Type]:
    """Get all subclasses of a base class"""

    all_subclasses = []
    for subclass in base_class.__subclasses__():
        all_subclasses.append(subclass)
        all_subclasses.extend(_get_all_subclasses(subclass))
    return all_subclasses


def configure_routes(app: FastAPI, settings: ConfigurationManager) -> FastAPI:
    """Add all endpoints, defined in the controller classes, to the fast api app"""

    url_prefix: str = str(settings.get_config(ConfigParameter.APP_URL_PREFIX, ""))
    while url_prefix.endswith("/"):
        # we do not want it to end with a slash
        url_prefix = url_prefix[:-1]
    if not url_prefix.startswith("/") and url_prefix:
        # url path has to start with a slash
        url_prefix = "/" + url_prefix

    # Import all modules in the api package to ensure all controller classes are loaded
    _import_submodules("src.controller")

    # Get all controller classes
    controller_classes = _get_all_subclasses(BaseController)

    # Initialize and register each controller
    for controller_class in controller_classes:
        controller = controller_class(settings=settings)
        controller.register_routes(app, url_prefix=url_prefix)

    return app
