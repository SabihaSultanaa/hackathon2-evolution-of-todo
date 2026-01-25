"""Authentication endpoints."""

import logging
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import select
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from app.database import get_db
from app.models.user import User
from app.auth.security import hash_password, verify_password, create_access_token
from app.schemas.user import UserCreate, UserLogin
from app.schemas.token import Token
from app.config import get_settings

router = APIRouter(prefix="/auth", tags=["Authentication"])
logger = logging.getLogger(__name__)
settings = get_settings()

# Define where the frontend should look for the token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Find the user in the database
    user = db.get(User, int(user_id))
    if user is None:
        raise credentials_exception
        
    return user

@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    logger.info(f"Register attempt for email: {user_data.email}")

    # Check if email already exists
    existing_user = db.execute(
        select(User).where(User.email == user_data.email)
    ).scalars().first()
    if existing_user:
        logger.warning(f"Registration failed - email already exists: {user_data.email}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Validate password length
    if len(user_data.password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters"
        )

    # Create new user
    user = User(
        email=user_data.email,
        hashed_password=hash_password(user_data.password)
    )
    db.add(user)
    try:
        db.commit()
        logger.info(f"User created successfully with ID: {user.id}")
    except Exception as e:
        db.rollback()
        logger.error(f"Database error during user creation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
    db.refresh(user)

    # Generate JWT token
    token = create_access_token(data={"sub": str(user.id)})

    return Token(access_token=token, token_type="bearer")


@router.post("/login", response_model=Token)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """Login with email and password."""
    # Find user by email
    user = db.execute(
        select(User).where(User.email == credentials.email)
    ).scalars().first()

    if user is None or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Generate JWT token 
    token = create_access_token(data={"sub": str(user.id)})

    return Token(access_token=token, token_type="bearer")