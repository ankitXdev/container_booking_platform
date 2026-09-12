from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.database import create_tables

from app.models.user_model import users
from app.models.container_model import container
from app.models.booking_model import booking
from app.models.payment_model import payment

from app.routes.Authentication.auth_router import router as auth_router
from app.routes.Provider.provider_router import router as provider_router
from app.routes.Container.container_router import router as container_router
from app.routes.Booking.booking_router import router as booking_router
from app.routes.Admin.admin_router import router as admin_router
from app.routes.Payment.payment_router import router as payment_router
from app.routes.Document.document_router import router as document_router
from fastapi.staticfiles import StaticFiles
import os


app = FastAPI()


# Create database tables
create_tables()

# Ensure uploads directory exists and mount static files
UPLOAD_DIR = os.path.join(os.getcwd(), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")


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
app.include_router(booking_router)
app.include_router(admin_router)
app.include_router(payment_router)
app.include_router(document_router)