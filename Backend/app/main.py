from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.database import create_tables

from app.models.user_model import users
from app.models.container_model import container

from app.routes.Authentication.auth_router import router as auth_router
from app.routes.Provider.provider_router import router as provider_router
from app.routes.Container.container_router import router as container_router


app = FastAPI()


# Create database tables
create_tables()


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Routers
app.include_router(auth_router)
app.include_router(provider_router)
app.include_router(container_router)