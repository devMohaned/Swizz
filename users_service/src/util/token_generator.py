from datetime import datetime, timedelta, timezone

from jose import jwt

from users_service.src.config.settings import settings


# Dummy Method (For testing purposes)
def get_access_token():
    expiration = datetime.now(timezone.utc) + timedelta(hours=5)
    token = jwt.encode(
        {
            "sub": "user123",
            "role": "admin",
            "aud": settings.jwt_audience,
            "iss": settings.jwt_issuer,
            "exp": expiration

        },
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm
    )
    print(f"Bearer {token}")


get_access_token()
