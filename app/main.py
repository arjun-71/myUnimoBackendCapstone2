from fastapi import FastAPI
from .routes import lookup, auth, files, api  # Import the new API routes
from .database import Base, engine
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (or specify like ["http://localhost:3000"])
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(lookup.router, prefix="/api/v1", tags=["Lookup"])
app.include_router(auth.router, prefix="/api/v1", tags=["Auth"])
app.include_router(files.router, prefix="/api/v1", tags=["Files"])
app.include_router(api.router, prefix="/api/v1", tags=["API"])  # ✅ Add the new API routes

@app.get("/")
def root():
    return {"message": "FastAPI Backend Running!"}
