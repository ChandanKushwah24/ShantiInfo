from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from database import engine, Base
from routes import guest_router, room_router, staff_router, reservation_router

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI application
app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.api_version,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(guest_router, prefix="/api")
app.include_router(room_router, prefix="/api")
app.include_router(staff_router, prefix="/api")
app.include_router(reservation_router, prefix="/api")

@app.get("/", tags=["Root"])
def read_root():
    return {
        "message": "Welcome to Hotel Management API",
        "version": settings.api_version,
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
