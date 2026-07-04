"""Report routes for safety reporting."""

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.database import get_session
from app.schemas.report_schema import ReportCreate, ReportResponse
from app.services.report_service import (
    submit_report,
    get_report,
    get_user_reports,
    get_reports_about_user,
    mark_report_resolved,
)

router = APIRouter(prefix="/api/reports", tags=["reports"])


@router.post("/", response_model=ReportResponse)
def submit_report_endpoint(
    report_data: ReportCreate,
    session: Session = Depends(get_session),
):
    """Submit a safety report."""
    report = submit_report(report_data.model_dump(), session)
    return report


@router.get("/{report_id}", response_model=ReportResponse)
def get_report_endpoint(report_id: int, session: Session = Depends(get_session)):
    """Get report details."""
    report = get_report(report_id, session)
    return report


@router.get("/user/{user_id}", response_model=list[ReportResponse])
def get_user_reports_endpoint(user_id: int, session: Session = Depends(get_session)):
    """Get reports submitted by a user."""
    reports = get_user_reports(user_id, session)
    return reports


@router.get("/about/{user_id}", response_model=list[ReportResponse])
def get_reports_about_endpoint(user_id: int, session: Session = Depends(get_session)):
    """Get reports about a user."""
    reports = get_reports_about_user(user_id, session)
    return reports


@router.patch("/{report_id}/resolve", response_model=ReportResponse)
def resolve_report_endpoint(
    report_id: int, session: Session = Depends(get_session)
):
    """Mark a report as resolved."""
    report = mark_report_resolved(report_id, session)
    return report
