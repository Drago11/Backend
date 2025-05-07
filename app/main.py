import logging
import time

from fastapi import FastAPI
from fastapi.params import Depends
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request

from app.auth.api_key_checker import check_api_key
from app.auth.auth import auth_router
from app.routers.user_router import user_router
from app.routers.waitlist_router import waitlist_router

app = FastAPI(
    dependencies=[Depends(check_api_key)],
    title="Knot9ja Backend API",
    description="A new and improve way to find job services in Nigeria!",
)
logger = logging.getLogger("uvicorn")

origins = [
    "http://localhost:3000",
    "https://knot9ja.vercel.app",
]
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


# app.include_router(auth_router)
app.include_router(waitlist_router)
