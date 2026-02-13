from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
from dotenv import load_dotenv

from app.routes import auth, cases, sightings, admin
from app.models.database import engine, Base, SessionLocal
from app.models.models import User
from app.utils.auth import get_password_hash

# Load environment variables
load_dotenv()

# Create database tables
Base.metadata.create_all(bind=engine)

# Create default admin user
def create_default_admin():
    db = SessionLocal()
    try:
        # Check if admin already exists
        admin_user = db.query(User).filter(User.email == "admin@admin.com").first()
        if not admin_user:
            # Use simple password to avoid bcrypt length issues
            admin_user = User(
                email="admin@admin.com",
                phone="+1234567890",
                hashed_password=get_password_hash("admin"),  # Shorter password
                is_admin=True
            )
            db.add(admin_user)
            db.commit()
            print("\n" + "="*50)
            print("🔑 DEFAULT ADMIN ACCOUNT CREATED:")
            print("📧 Email: admin@admin.com")
            print("🔒 Password: admin")
            print("🌐 Login at: http://localhost:3000")
            print("👨💼 Admin Dashboard will be visible after login")
            print("="*50 + "\n")
        else:
            print("\n✅ Admin account already exists: admin@admin.com\n")
    except Exception as e:
        print(f"Error creating admin user: {e}")
        # Try with even simpler hash
        try:
            import hashlib
            simple_hash = hashlib.sha256("admin".encode()).hexdigest()
            admin_user = User(
                email="admin@admin.com",
                phone="+1234567890",
                hashed_password=simple_hash,
                is_admin=True
            )
            db.add(admin_user)
            db.commit()
            print("\n✅ Admin created with simple hash\n")
        except Exception as e2:
            print(f"Simple hash also failed: {e2}")
    finally:
        db.close()

# Create admin user on startup
create_default_admin()

app = FastAPI(
    title="Missing Person Detection System",
    description="API for missing person detection using facial recognition",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React app
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(cases.router, prefix="/cases", tags=["Cases"])
app.include_router(sightings.router, prefix="/sightings", tags=["Sightings"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])

@app.get("/")
async def root():
    return {"message": "Missing Person Detection System API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )