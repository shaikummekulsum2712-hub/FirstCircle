from pydantic import BaseModel


class ProfileCreate(BaseModel):
    user_id: int
    year: str
    branch: str
    student_type: str
    bio: str = ""
    interests: list[str] = []
    comfort_preferences: list[str] = []
    skills: list[str] = []


class ProfileUpdate(BaseModel):
    year: str | None = None
    branch: str | None = None
    student_type: str | None = None
    bio: str | None = None
    interests: list[str] | None = None
    comfort_preferences: list[str] | None = None
    skills: list[str] | None = None


class ProfileRead(BaseModel):
    id: int
    user_id: int
    year: str
    branch: str
    student_type: str
    bio: str
    interests: list[str]
    comfort_preferences: list[str]
    skills: list[str]

    class Config:
        from_attributes = True