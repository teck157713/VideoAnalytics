from __future__ import annotations
import httpx
from fastapi import APIRouter, HTTPException, Query, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from config.auth0_config import get_settings
from DetectAnalytics.routers.models import OauthException, OauthToken
settings = get_settings()
router = APIRouter()
security = HTTPBearer()

@router.get(
    "/callback",
    response_model=OauthToken,
    responses={
        400: {"description": "Oauth Error", "model": OauthException},
    },
)
async def oauth_callback(
    code: str = Query(description="Authorization Code"),
) -> OauthToken:
    """
    GitHub Oauth Integration Callback
    """
    async with httpx.AsyncClient() as client:
        token_result = await client.post(
            "https://github.com/login/oauth/access_token",
            json={
                "client_id": settings.GITHUB_AUTH0_CLIENTID,
                "client_secret": settings.GITHUB_AUTH0_CLIENT_SECRET,
                "code": code,
                "redirect_uri": "http://localhost:8080/v1/auth/callback",
            },
            headers={"Accept": "application/json"},
        )
        data = token_result.json()
        error = data.get("error")
        if error:
            raise HTTPException(
                status_code=400,
                detail=f"{data.get('error')}: {data.get('error_description')}",
            )

        access_token: str = data.get("access_token")
        user_result = await client.get(
            "https://api.github.com/user",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        user_data = user_result.json()
        user = user_data.get("login")

    return OauthToken(access_token=access_token)

async def validate_access_token(
    access_token: Depends(security)
) -> str:
    """
    Validate an access token
    Returns the username or raises a 401 HTTPException
    """
    async with httpx.AsyncClient() as client:
        user_result = await client.get(
            "https://api.github.com/user",
            headers={"Authorization": f"Bearer {access_token.credentials}"},
        )

        if user_result.status_code == 200:
            user_data = user_result.json()
            user = user_data.get("login")
            if user:
                return user

    raise HTTPException(
        status_code=401,
        detail="Unauthorized",
    )