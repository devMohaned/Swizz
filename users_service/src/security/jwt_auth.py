import logging

from fastapi import Depends, status, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from config.settings import settings
from exception.app_exceptions import AppException
from exception.error_code import BAD_TOKEN

logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_token(token: str):
    try:
        logger.info(f"Verifying token: {token}")
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm],
            audience=settings.jwt_audience,
            issuer=settings.jwt_issuer,
        )
        return payload
    except JWTError as e:
        logger.warning(f"Invalid JWT: {str(e)}")
        raise AppException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message="Invalid or expired token",
            code=BAD_TOKEN,
        )
    except Exception as e:
        logger.exception(f"Failed to verify token: {str(e)}")
        raise e


async def get_current_user(request: Request, token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    role = payload.get("role")
    if not role:
        logger.warning(f"Invalid or expired token: {token}")
        raise AppException(status_code=403, message="Missing role in token claims", code=BAD_TOKEN)

    # attach user context to the request
    request.state.user = payload
    return payload
