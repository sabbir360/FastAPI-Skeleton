from contextlib import asynccontextmanager
from datetime import timedelta
from fastapi import FastAPI, Depends, HTTPException, \
    Query, status, Body, Request
from fastapi.openapi.utils import get_openapi
from db import get_db

from service import Service
from auth import create_access_token, verify_token
from crud import CRUDExample
from schemas import RequestSchema, RequestResponse, TokenRequest, \
    TokenResponse, StatusSchema
from config import config
from models import SampleTable


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = get_db()
    db.connect()
    db.create_tables([SampleTable])
    yield
    db.close()


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    schema = get_openapi(
        title="RESTFul API (OpenAPI 3.0.3)",
        version="1.0.0",
        description="A Sample Swagger/OpenAPI 3 standard project skeleton.",
        routes=app.routes,
    )
    for methods in schema.get("paths", {}).values():
        for details in methods.values():
            for k in list(details.get("responses", {}).keys()):
                if k != "200":
                    details["responses"][k] = {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "example": {
                                    "name": "example name",
                                    "app_name": "my_app",
                                    "detail": "Error details"
                                }
                            }
                        },
                    }
    app.openapi_schema = schema
    return schema


app = FastAPI(lifespan=lifespan)
app.openapi = custom_openapi


@app.get("/record", response_model=RequestResponse)
async def get_record_by_type_propagation(
    name: str = Query(..., description="Check record propagation"),
    record_type: str = Query(..., description="Type of record"),
    app_name: str = Depends(verify_token)
):
    
    service = Service(app_name)
    
    crud = CRUDExample()
    record_history = crud.get_record_by_type(record_type)
    service_status = service.check_status(record_history)
    if service_status == "P":
        status_enum = StatusSchema.PROPAGATED
    elif service_status == "I":
        status_enum = StatusSchema.IN_PROGRESS
    else:
        status_enum = StatusSchema.NOT_AVAILABLE
    return RequestResponse(name=name, app_name=app_name, status=status_enum,
                          detail=f"{record_type} records checked.")


@app.post("/record", response_model=RequestResponse)
async def create_record(
    request: RequestSchema,
    req: Request,
    app_name: str = Depends(verify_token)
):
    crud = CRUDExample()
    crud.save()
    return RequestResponse(name=request.name, app_name=app_name, status=StatusSchema.IN_PROGRESS,
                          detail="Record created.")


@app.patch("/record", response_model=RequestResponse)
async def patch_record(
    request: RequestSchema,
    req: Request,
    app_name: str = Depends(verify_token)
):
    pass


@app.put("/record", response_model=RequestResponse)
async def put_record(
    request: RequestSchema,
    req: Request,
    app_name: str = Depends(verify_token)
):
    pass


@app.post("/token", response_model=TokenResponse)
def generate_token(request: TokenRequest = Body(...)):
    """
    Generate a token for the given app name and secret key.

    The token will be valid for 10 minutes.

    Args:

        request (TokenRequest, optional): _description_. Defaults to Body(...).

    Raises:

        HTTPException: _description_

    Returns:

        Token and Bearer token type.

        Response model: TokenResponse
    """
    if config["auth"].get(request.app_name) == request.secret_key:
        timeout = 10
        token = create_access_token(data={"sub": request.secret_key,
                                          "app": request.app_name},
                                    expires_delta=timedelta(minutes=timeout))
        return TokenResponse(token=token, token_type="bearer", timeout=timeout)
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid secret key")
