from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    email: str
    roll_number: str


class UserRead(BaseModel):
    id: int
    name: str
    email: str
    roll_number: str
    college_domain: str
    email_verified: bool
    verification_status: str

    class Config:
        from_attributes = True