from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.models.location import Location
from app.schemas.location_schema import LocationCreate, LocationRead

router = APIRouter(prefix="/locations", tags=["Locations"])


@router.get("/", response_model=list[LocationRead])
def get_locations(session: Session = Depends(get_session)):
    statement = select(Location)
    locations = session.exec(statement).all()
    return locations


@router.post("/", response_model=LocationRead)
def create_location(
    location_data: LocationCreate,
    session: Session = Depends(get_session),
):
    existing = session.exec(
        select(Location).where(Location.name == location_data.name)
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Location already exists")

    location = Location(**location_data.model_dump())
    session.add(location)
    session.commit()
    session.refresh(location)

    return location