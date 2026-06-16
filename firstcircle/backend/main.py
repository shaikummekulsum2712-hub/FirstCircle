import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .app.database import engine, Base
from .app.routes import (
    auth_routes,
    profile_routes,
    drop_routes,
    proposal_routes,
    circle_routes,
    feedback_routes,
    report_routes,
    location_routes,
    auto_place_routes,
)
from .app.jobs.scheduler import scheduler_loop

# Initialize database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FirstCircle API",
    description="Backend services for matching users into peer connection groups.",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all origins for dev simplicity
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(auth_routes.router, prefix="/api")
app.include_router(profile_routes.router, prefix="/api")
app.include_router(drop_routes.router, prefix="/api")
app.include_router(proposal_routes.router, prefix="/api")
app.include_router(circle_routes.router, prefix="/api")
app.include_router(feedback_routes.router, prefix="/api")
app.include_router(report_routes.router, prefix="/api")
app.include_router(location_routes.router, prefix="/api")
app.include_router(auto_place_routes.router, prefix="/api")

@app.get("/")
def index():
    return {"name": "FirstCircle API", "status": "active"}

@app.on_event("startup")
async def startup_event():
    # Run the background job scheduler loop
    asyncio.create_task(scheduler_loop())
