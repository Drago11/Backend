import logging
import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.params import Depends
from scalar_fastapi import get_scalar_api_reference
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request

from app.auth.api_key_checker import check_api_key
from app.core import settings
from app.routers import auth_router, user_router, waitlist_router

app = FastAPI(
    title="Knot9ja Backend API",
    description="A new and improved way to find job services in Nigeria!",
)
logger = logging.getLogger("uvicorn")

origins = [
    "http://localhost:3000",
    "https://knot9ja.vercel.app",
]

app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def measure_response_time(request: Request, call_next):
    start_time = time.perf_counter()  # Start timer
    response = await call_next(request)  # Process request
    end_time = time.perf_counter()  # End timer
    duration = (end_time - start_time) * 1000  # Convert to milliseconds
    logger.info(f"Request: {request.method} {request.url} ~ {duration:.2f} ms")
    return response


@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
    )


app.include_router(auth_router, )
app.include_router(user_router, dependencies=[Depends(check_api_key)], )
app.include_router(waitlist_router, dependencies=[Depends(check_api_key)], )
