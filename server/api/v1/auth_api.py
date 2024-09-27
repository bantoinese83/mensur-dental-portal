from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.dependencies import get_db_session
from core.security import create_access_token, verify_password, generate_mfa_secret, verify_totp, decode_access_token, \
    get_password_hash
from crud.user_crud import get_user_by_email, update_user
from schemas.auth_schema import Token, MFAEnableRequest, MFAVerifyRequest, PasswordReset

router = APIRouter()


@router.post(
    "/login",
    response_model=Token,
    summary="User Login",
    description="Authenticate a user and return an access token. 🔑",
)
def login(email: str, password: str, db: Session = Depends(get_db_session)):
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/enable-mfa", summary="Enable MFA", description="Enable Multi-Factor Authentication for a user.")
def enable_mfa(request: MFAEnableRequest, db: Session = Depends(get_db_session)):
    user = get_user_by_email(db, email=request.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    mfa_secret = generate_mfa_secret()
    user.mfa_secret = mfa_secret
    update_user(db, user_id=user.id, user=user)
    return {"mfa_secret": mfa_secret}


@router.post("/verify-mfa", summary="Verify MFA", description="Verify Multi-Factor Authentication for a user.")
def verify_mfa(request: MFAVerifyRequest, db: Session = Depends(get_db_session)):
    user = get_user_by_email(db, email=request.email)
    if not user or not user.mfa_secret:
        raise HTTPException(status_code=404, detail="User not found or MFA not enabled")

    if not verify_totp(user.mfa_secret, request.token):
        raise HTTPException(status_code=400, detail="Invalid MFA token")

    return {"message": "MFA verified successfully"}


@router.post("/reset-password", summary="Reset Password", description="Reset the password for a user.")
def reset_password(request: PasswordReset, db: Session = Depends(get_db_session)):
    try:
        payload = decode_access_token(request.token)
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=400, detail="Invalid token")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid token")

    user = get_user_by_email(db, email=email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.hashed_password = get_password_hash(request.new_password)
    update_user(db, user_id=user.id, user=user)
    return {"message": "Password reset successful"}
