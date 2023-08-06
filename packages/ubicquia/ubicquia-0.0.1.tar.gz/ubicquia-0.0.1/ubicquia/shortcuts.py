"""Shortuct for common tools."""

from decouple import config
from .base import UbicquiaSession
from .client import Ubicquia


def ubicquia_instance() -> Ubicquia:
    """Create an instance of Ubicquia using ENV variables.

    Prefix env with `UBICQUIA_` all names in upper case. Use Ubicquia default
    names. Example:

    - UBICQUIA_CLIENT_ID
    - UBICQUIA_SECRET_KEY
    - UBICQUIA_USERNAME
    - UBICQUIA_PASSWORD
    """
    CLIENT_ID = config('UBICQUIA_CLIENT_ID')
    SECRET_KEY = config('UBICQUIA_SECRET_KEY')
    USERNAME = config('UBICQUIA_USERNAME')
    PASSWORD = config('UBICQUIA_PASSWORD')
    session = UbicquiaSession(
        client_id=CLIENT_ID,
        client_secret=SECRET_KEY,
        username=USERNAME,
        password=PASSWORD
    )
    return Ubicquia(session)
