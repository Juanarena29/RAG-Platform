from fastapi import Depends, FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.deps import get_current_user
from app.api.middleware import limiter, setup_middleware
from app.api.routes import health as health_router
from app.core.config import get_settings
from app.core.exceptions import (
    http_exception_handler,
    unhandled_exception_handler,
    validation_exception_handler,
)
from app.core.logging import setup_logging
from app.db.models import User

settings = get_settings()
setup_logging()

app = FastAPI(title=settings.app_name, version=settings.app_version)

setup_middleware(app)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)

app.include_router(health_router.router)


@app.get("/me")
@limiter.limit(settings.default_rate_limit)
def me(request: Request, current_user: User = Depends(get_current_user)) -> dict[str, str | int]:
    return {
        "id": current_user.id,
        "email": current_user.email,
    }
