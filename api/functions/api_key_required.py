from fastapi import HTTPException, status, Request

from settings import settings


def api_key_required(request: Request) -> str:
    """
    Check API Key.

    :param request: Request object.
    :return: api key.
    """
    api_key = request.headers.get("X-API-Key")
    if api_key != settings.api_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API Key")
    return api_key
