from fastapi import FastAPI

from app.routers.waitlist_router import waitlist_router

app = FastAPI()

app.include_router(waitlist_router)
