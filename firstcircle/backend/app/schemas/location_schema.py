from pydantic import BaseModel


class LocationCreate(BaseModel):
    name: str
    location_type: str
    is_safe: bool = True
    allowed_circle_types: str = "friend,study,build,random"


class LocationRead(BaseModel):
    id: int
    name: str
    location_type: str
    is_safe: bool
    allowed_circle_types: str

    class Config:
        from_attributes = True