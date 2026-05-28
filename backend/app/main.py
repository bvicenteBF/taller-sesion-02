from datetime import timedelta

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError

from app.auth import authenticate_user, create_access_token, decode_token
from app.config import settings
from app.schemas import TokenRequest, TokenResponse

app = FastAPI(title="JWT Auth API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

bearer_scheme = HTTPBearer()


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/auth/token", response_model=TokenResponse)
def login(request: TokenRequest):
    """
    Authenticate with username and password.
    Returns a JWT access token valid for 300 seconds.
    """
    user = authenticate_user(request.username, request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token(
        data={"sub": user["username"]},
        expires_delta=timedelta(seconds=settings.access_token_expire_seconds),
    )
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        expires_in=settings.access_token_expire_seconds,
    )


@app.post("/auth/refresh", response_model=TokenResponse)
def refresh_token(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    """
    Refresh an existing valid JWT token.
    Returns a new JWT access token valid for 300 seconds.
    """
    token = credentials.credentials
    try:
        payload = decode_token(token)
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    new_token = create_access_token(
        data={"sub": username},
        expires_delta=timedelta(seconds=settings.access_token_expire_seconds),
    )
    return TokenResponse(
        access_token=new_token,
        token_type="bearer",
        expires_in=settings.access_token_expire_seconds,
    )
