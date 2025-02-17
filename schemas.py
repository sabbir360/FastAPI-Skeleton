from pydantic import BaseModel, Field
from enum import Enum


class StatusSchema(str, Enum):
    IN_PROGRESS = "In Progress"
    NOT_AVAILABLE = "Not Available"


class RequestSchema(BaseModel):
    name: str


class BaseResponse(BaseModel):
    detail: str


class RequestResponse(BaseResponse):
    name: str
    app_name: str
    status: StatusSchema = Field(
        None, description="Status of the item")


class TokenRequest(BaseModel):
    app_name: str = Field(..., min_length=3, max_length=50,
                          description="Name of the application requesting the token")
    secret_key: str = Field(..., min_length=10, max_length=128,
                            description="Secret key for authentication")


class TokenResponse(BaseModel):
    token: str = Field(...,
                       description="Generated token for API authentication")
    token_type: str = Field("bearer", description="Type of the token")
    timeout: int = Field(..., description="Timeout in minutes")
