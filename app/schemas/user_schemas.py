from builtins import ValueError, any, bool, str
from pydantic import BaseModel, EmailStr, Field, validator, root_validator
from typing import Optional, List
from datetime import datetime
from enum import Enum
import uuid
import re
from app.models.user_model import UserRole
from app.utils.nickname_gen import generate_nickname


def validate_url(url: Optional[str]) -> Optional[str]:
    if url is None:
        return url
    url_regex = r'^https?:\/\/[^\s/$.?#].[^\s]*$'
    if not re.match(url_regex, url):
        raise ValueError('Invalid URL format')
    return url

class UserBase(BaseModel):
    email: EmailStr = Field(..., example="john.doe@example.com")
    nickname: Optional[str] = Field(None, min_length=3, pattern=r'^[\w-]+$', example=generate_nickname())
    first_name: Optional[str] = Field(None, example="John")
    last_name: Optional[str] = Field(None, example="Doe")
    bio: Optional[str] = Field(None, example="Experienced software developer specializing in web applications.")
    profile_picture_url: Optional[str] = Field(None, example="https://example.com/profiles/john.jpg")
    linkedin_profile_url: Optional[str] =Field(None, example="https://linkedin.com/in/johndoe")
    github_profile_url: Optional[str] = Field(None, example="https://github.com/johndoe")
    role: UserRole

    _validate_urls = validator('profile_picture_url', 'linkedin_profile_url', 'github_profile_url', pre=True, allow_reuse=True)(validate_url)
 
    class Config:
        from_attributes = True

class UserCreate(UserBase):
    email: EmailStr = Field(..., example="john.doe@example.com")
    password: str = Field(..., example="Secure*1234")

    @validator("password")
    def validate_password_strength(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must include at least one uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must include at least one lowercase letter")
        if not re.search(r"\d", v):
            raise ValueError("Password must include at least one number")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError("Password must include at least one special character")
        return v


class UserUpdate(UserBase):
    email: Optional[EmailStr] = Field(None, example="john.doe@example.com")
    nickname: Optional[str] = Field(None, min_length=3, pattern=r'^[\w-]+$', example="john_doe123")
    first_name: Optional[str] = Field(None, example="John")
    last_name: Optional[str] = Field(None, example="Doe")
    bio: Optional[str] = Field(None, example="Experienced software developer specializing in web applications.")
    profile_picture_url: Optional[str] = Field(None, example="https://example.com/profiles/john.jpg")
    linkedin_profile_url: Optional[str] =Field(None, example="https://linkedin.com/in/johndoe")
    github_profile_url: Optional[str] = Field(None, example="https://github.com/johndoe")
    role: Optional[UserRole] = Field(None, example="AUTHENTICATED")

    @root_validator(pre=True)
    def check_at_least_one_value(cls, values):
        if not any(values.values()):
            raise ValueError("At least one field must be provided for update")
        return values

class UserResponse(UserBase):
    id: uuid.UUID = Field(..., example=uuid.uuid4())
    email: EmailStr = Field(..., example="john.doe@example.com")
    nickname: Optional[str] = Field(None, min_length=3, pattern=r'^[\w-]+$', example=generate_nickname())    
    is_professional: Optional[bool] = Field(default=False, example=True)
    role: UserRole

    created_at: datetime = Field(..., example=str(datetime.utcnow()))
    updated_at: datetime = Field(..., example=str(datetime.utcnow()))
    last_login_at: Optional[datetime] = Field(None, example=str(datetime.utcnow()))
    links: Optional[dict] = Field(None, example={"self": "/users/1234", "edit": "/users/1234/edit"})
    profile_picture_url: Optional[str] = None

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": "9dc3ba46-395a-437b-946c-4c5d49ef5aa2",
                "email": "john.doe@example.com",
                "nickname": "jolly_lion_403",
                "is_professional": True,
                "role": "authenticated",
                "created_at": "2025-05-05T12:00:00Z",
                "updated_at": "2025-05-05T12:05:00Z",
                "last_login_at": "2025-05-05T12:03:00Z",
                "links": {
                    "self": "/users/9dc3ba46-395a-437b-946c-4c5d49ef5aa2",
                    "edit": "/users/9dc3ba46-395a-437b-946c-4c5d49ef5aa2/edit"
                },
                "profile_picture_url": "https://cdn.minio.myapp.com/profile-pictures/john_doe.jpg"
            }
        }



class LoginRequest(BaseModel):
    email: str = Field(..., example="john.doe@example.com")
    password: str = Field(..., example="Secure*1234")

class ErrorResponse(BaseModel):
    error: str = Field(..., example="Not Found")
    details: Optional[str] = Field(None, example="The requested resource was not found.")

class UserListResponse(BaseModel):
    items: List[UserResponse] = Field(
        ...,
        example=[
            {
                "id": "123e4567-e89b-12d3-a456-426614174000",  # Just a static UUID string
                "nickname": "cooldev123",
                "email": "john.doe@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "bio": "Experienced developer",
                "role": "AUTHENTICATED",
                "profile_picture_url": "https://example.com/profiles/john.jpg",
                "linkedin_profile_url": "https://linkedin.com/in/johndoe",
                "github_profile_url": "https://github.com/johndoe",
                "is_professional": True
            }
        ]
    )

    total: int = Field(..., example=100)
    page: int = Field(..., example=1)
    size: int = Field(..., example=10)
