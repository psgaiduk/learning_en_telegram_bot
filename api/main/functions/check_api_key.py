from fastapi import HTTPException, Request, status


def check_api_key(request: Request) -> None:
    """Check API key."""
    api_key = request.headers.get("X-API-Key")
    if api_key != "YOUR_PERSONAL_UNIQUE_API_KEY":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API Key")