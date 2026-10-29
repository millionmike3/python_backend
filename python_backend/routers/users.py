# python_backend/routers/users.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from python_backend.database import get_db
from python_backend.models.users import User, UserVault, DigitalAsset
from python_backend.schemas import (
    UserOut,
    UserCreate,
    UserLogin,
    UserVaultOut,
    DigitalAssetCreate,
    DigitalAssetOut,
)
from python_backend.rbac import get_current_user, require_admin

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


# ============================================================
# LIST USERS (ADMIN ONLY)
# ============================================================
@router.get("/", response_model=List[UserOut], dependencies=[Depends(require_admin)])
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()


# ============================================================
# GET CURRENT USER PROFILE
# ============================================================
@router.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


# ============================================================
# CREATE USER (ADMIN ONLY)
# ============================================================
@router.post("/", response_model=UserOut, dependencies=[Depends(require_admin)])
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == data.username).first()
    if existing:
        raise HTTPException(400, "Username already exists")

    user = User(
        username=data.username,
        email=data.email,
        phone=data.phone,
        password_hash=data.password,  # TODO: hash properly
        role=data.role,
        domain_id=data.domain_id,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    vault = UserVault(user_id=user.id, balance=0.0)
    db.add(vault)
    db.commit()

    return user


# ============================================================
# USER VAULT
# ============================================================
@router.get("/vault/me", response_model=UserVaultOut)
def get_my_vault(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    vault = db.query(UserVault).filter(UserVault.user_id == current_user.id).first()
    if not vault:
        raise HTTPException(404, "Vault not found")
    return vault


# ============================================================
# DIGITAL ASSETS
# ============================================================
@router.post("/assets", response_model=DigitalAssetOut)
def add_asset(
    data: DigitalAssetCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    asset = DigitalAsset(
        user_id=current_user.id,
        asset_type=data.asset_type,
        uri=data.uri,
    )
    db.add(asset)
    db.commit()
    db.refresh(asset)
    return asset


@router.get("/assets", response_model=List[DigitalAssetOut])
def list_assets(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return db.query(DigitalAsset).filter(DigitalAsset.user_id == current_user.id).all()
