from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import create_db_and_tables
from app.routes.auto_place_routes import router as auto_place_router
from app.routes.circle_routes import router as circle_router
from app.routes.drop_member_routes import router as drop_member_router
from app.routes.drop_routes import router as drop_router
from app.routes.feedback_routes import router as feedback_router
from app.routes.free_slots_routes import router as free_slot_router
from app.routes.health_routes import router as health_router
from app.routes.location_routes import router as location_router
from app.routes.profile_routes import router as profile_router
from app.routes.proposal_routes import router as proposal_router
from app.routes.report_routes import router as report_router
from app.routes.user_routes import router as user_router
from app.routes.vibe_vote_routes import router as vibe_vote_router

app = FastAPI(
    title=settings.APP_NAME,
    version="0.2.0",
    description="Backend API for FirstCircle campus circle matching platform",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


app.include_router(health_router, prefix="/api")
app.include_router(location_router, prefix="/api")
app.include_router(user_router, prefix="/api")
app.include_router(profile_router, prefix="/api")
app.include_router(free_slot_router, prefix="/api")
app.include_router(drop_router, prefix="/api")
app.include_router(drop_member_router, prefix="/api")
app.include_router(vibe_vote_router, prefix="/api")
app.include_router(auto_place_router, prefix="/api")
app.include_router(proposal_router)
app.include_router(circle_router)
app.include_router(feedback_router)
app.include_router(report_router)