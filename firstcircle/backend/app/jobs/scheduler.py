import asyncio
import logging
from ..database import SessionLocal
from .proposal_expiry_job import run_proposal_expiry_job
from .expire_drops_job import run_expire_drops_job
from .feedback_request_job import run_feedback_request_job
from .reminder_job import run_reminder_job

logger = logging.getLogger("firstcircle.scheduler")

async def scheduler_loop():
    """
    Background loop running inside FastAPI server to execute periodic cleanup and matching maintenance.
    """
    logger.info("Background job scheduler started.")
    await asyncio.sleep(5)  # Wait for startup buffer

    while True:
        try:
            db = SessionLocal()
            try:
                # 1. Clear expired proposals
                run_proposal_expiry_job(db)
                
                # 2. Expire empty/unfilled drops
                run_expire_drops_job(db)
                
                # 3. Transition complete circles and schedule feedback prompts
                run_feedback_request_job(db)
                
                # 4. Trigger upcoming event alerts
                run_reminder_job(db)
            finally:
                db.close()
        except Exception as e:
            logger.error(f"Error in background scheduler cycle: {e}")
            
        await asyncio.sleep(30) # Run cycle every 30 seconds
