"""Report service for safety reporting."""

from fastapi import HTTPException
from sqlmodel import Session, select

from app.models.circle import Circle
from app.models.report import Report
from app.models.user import User


def submit_report(report_data: dict, session: Session) -> Report:
    """Submit a safety report for a circle."""
    circle_id = report_data["circle_id"]
    reporter_user_id = report_data["reporter_user_id"]
    reported_user_id = report_data.get("reported_user_id")
    reason = report_data["reason"]
    details = report_data.get("details", "")

    # Validate circle exists
    circle = session.get(Circle, circle_id)
    if not circle:
        raise HTTPException(status_code=404, detail="Circle not found")

    # Validate reporter exists
    reporter = session.get(User, reporter_user_id)
    if not reporter:
        raise HTTPException(status_code=404, detail="Reporter not found")

    # Validate reported user exists if provided
    if reported_user_id:
        reported = session.get(User, reported_user_id)
        if not reported:
            raise HTTPException(status_code=404, detail="Reported user not found")

    # Create report
    report = Report(
        circle_id=circle_id,
        reporter_user_id=reporter_user_id,
        reported_user_id=reported_user_id,
        reason=reason,
        details=details,
        status="open",
    )
    session.add(report)
    session.commit()
    session.refresh(report)
    return report


def get_report(report_id: int, session: Session) -> Report:
    """Get a report by ID."""
    report = session.get(Report, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report


def get_user_reports(user_id: int, session: Session) -> list[Report]:
    """Get all reports submitted by a user."""
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    reports = session.exec(
        select(Report).where(Report.reporter_user_id == user_id)
    ).all()
    return reports


def get_reports_about_user(user_id: int, session: Session) -> list[Report]:
    """Get all reports about a user."""
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    reports = session.exec(
        select(Report).where(Report.reported_user_id == user_id)
    ).all()
    return reports


def mark_report_resolved(report_id: int, session: Session) -> Report:
    """Mark a report as resolved."""
    report = get_report(report_id, session)
    report.status = "resolved"
    session.add(report)
    session.commit()
    session.refresh(report)
    return report
