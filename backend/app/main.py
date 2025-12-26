from datetime import datetime, timedelta
from typing import Annotated

import structlog
from fastapi import FastAPI, Header, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRouter
from pydantic import BaseModel, Field

from .config import Settings, get_settings

logger = structlog.get_logger()


class RegisterRequest(BaseModel):
    email: str
    device_name: str
    identity_key: str = Field(..., description="Client-generated public identity key")
    signed_prekey: str = Field(..., description="Client-generated signed prekey")
    one_time_prekeys: list[str] = Field(default_factory=list)


class RegisterResponse(BaseModel):
    user_id: str
    device_id: str
    access_token: str


class LoginRequest(BaseModel):
    email: str
    code: str


class KeyBundleResponse(BaseModel):
    identity_key: str
    signed_prekey: str
    one_time_prekeys: list[str]


class SignalPayload(BaseModel):
    from_device: str
    to_device: str
    message: dict


class PresignRequest(BaseModel):
    file_name: str
    content_type: str
    expires_in: int = 900


class PresignResponse(BaseModel):
    url: str
    expires_at: datetime


def build_api_router(settings: Settings) -> APIRouter:
    router = APIRouter()

    @router.post("/register", response_model=RegisterResponse)
    async def register(payload: RegisterRequest) -> RegisterResponse:
        logger.info("register", email=payload.email, device=payload.device_name)
        # TODO: persist user/device/keys in Postgres, send magic link/OTP
        return RegisterResponse(user_id="u_1", device_id="d_1", access_token="mock-token")

    @router.post("/login", response_model=RegisterResponse)
    async def login(payload: LoginRequest) -> RegisterResponse:
        logger.info("login", email=payload.email)
        return RegisterResponse(user_id="u_1", device_id="d_1", access_token="mock-token")

    @router.get("/keys/{device_id}", response_model=KeyBundleResponse)
    async def fetch_keys(device_id: str) -> KeyBundleResponse:
        logger.info("fetch_keys", device_id=device_id)
        return KeyBundleResponse(
            identity_key="identity", signed_prekey="signed", one_time_prekeys=["otk1"]
        )

    @router.get("/prekeys/{user_id}", response_model=list[KeyBundleResponse])
    async def fetch_prekeys(user_id: str) -> list[KeyBundleResponse]:
        logger.info("fetch_prekeys", user_id=user_id)
        return [
            KeyBundleResponse(
                identity_key="identity", signed_prekey="signed", one_time_prekeys=["otk1"]
            )
        ]

    @router.post("/signal")
    async def signal(payload: SignalPayload) -> dict:
        logger.info("signal", from_device=payload.from_device, to_device=payload.to_device)
        # TODO: push over websocket to recipient
        return {"status": "queued"}

    @router.post("/attachments/presign", response_model=PresignResponse)
    async def presign(req: PresignRequest) -> PresignResponse:
        logger.info("presign", file=req.file_name, size_hint=req.expires_in)
        expires_at = datetime.utcnow() + timedelta(seconds=req.expires_in)
        # TODO: integrate with S3/MinIO presign
        return PresignResponse(url="https://example.com/presigned", expires_at=expires_at)

    @router.get("/stun-turn-cred")
    async def stun_turn_cred() -> dict:
        # TODO: issue time-bound TURN credentials using TURN_SECRET
        return {"username": "demo", "credential": "demo"}

    return router


def create_app(settings: Settings) -> FastAPI:
    app = FastAPI(title=settings.app_name)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    api_router = build_api_router(settings)
    app.include_router(api_router, prefix="/api")

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.websocket("/ws")
    async def ws_endpoint(
        websocket: WebSocket, authorization: Annotated[str | None, Header()] = None
    ) -> None:
        await websocket.accept()
        try:
            await websocket.send_json({"hello": "world", "auth": bool(authorization)})
            await websocket.close()
        except WebSocketDisconnect:
            logger.info("websocket disconnect")

    return app


def get_app() -> FastAPI:
    settings = get_settings()
    return create_app(settings)


app = get_app()
