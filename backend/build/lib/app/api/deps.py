from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session

from app.auth.api_key import get_active_api_key
from app.db.database import get_db
from app.db.models import User

authorization_header = APIKeyHeader(name="Authorization", auto_error=False)


def get_current_user(
    authorization: str | None = Depends(authorization_header),
    db: Session = Depends(get_db),
) -> User:
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Authorization header",
        )

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Authorization scheme",
        )

    raw_api_key = authorization.removeprefix("Bearer ").strip()
    if not raw_api_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing API key")

    api_key = get_active_api_key(db=db, raw_key=raw_api_key)
    if not api_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")

    user = db.get(User, api_key.user_id)
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user")

    return user
