from fastapi import FastAPI

from app.routes.Authentication.auth_router import router as auth_router

app = FastAPI( title="container_booking_platform", 
              description="API for the container_booking_platform",
              version="1.0.0"
              )

app.include_router(auth_router)