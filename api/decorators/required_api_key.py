from functools import wraps
from fastapi import HTTPException, status

from settings import settings


def api_key_required(func):
    @wraps(func)
    async def decorated_function(*args, **kwargs):
        request = kwargs.get('request')
        if request:
            api_key = request.headers.get('X-API-Key')
            if api_key != settings.api_key:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid API Key')
        return await func(*args, **kwargs)
    return decorated_function
