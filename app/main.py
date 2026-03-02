import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app import models
from app.crud import DuplicateEmailError, UserNotFoundError
from app.database import engine
from app.routers import employee

# Keep logging simple and useful for development.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="User Management API", version="1.0.0")
app.include_router(employee.router)


@app.exception_handler(DuplicateEmailError)
async def duplicate_email_exception_handler(request: Request, exc: DuplicateEmailError):
    logger.warning("Duplicate email error at %s", request.url.path)
    return JSONResponse(status_code=409, content={"detail": str(exc)})


@app.exception_handler(UserNotFoundError)
async def user_not_found_exception_handler(request: Request, exc: UserNotFoundError):
    logger.info("User not found at %s", request.url.path)
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(
    request: Request, exc: RequestValidationError
):
    logger.warning("Validation error at %s", request.url.path)
    return JSONResponse(
        status_code=422,
        content={"detail": "Validation error", "errors": exc.errors()},
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.exception("Unexpected error at %s", request.url.path)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )
