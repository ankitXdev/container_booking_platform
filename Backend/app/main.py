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


# =============================================================================
# Production CORS Configuration
# =============================================================================
# Reads allowed origins from environment variable (e.g. CORS_ORIGINS or FRONTEND_URL)
# Supports local development and automatic Vercel preview/production domains.
default_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

env_cors = os.getenv("CORS_ORIGINS", "")
allowed_origins = [origin.strip() for origin in env_cors.split(",") if origin.strip()] or default_origins

frontend_url = os.getenv("FRONTEND_URL")
if frontend_url and frontend_url.strip() not in allowed_origins:
    allowed_origins.append(frontend_url.strip())

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_origin_regex=r"https://.*\.vercel\.app|https://.*\.onrender\.com|https://.*\.netlify\.app",
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