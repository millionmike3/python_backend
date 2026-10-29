# python_backend/models/users.py

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from python_backend.database import Base


# ============================================================
# USER MODEL
# ============================================================
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, nullable=True)

    # Stored hashed password
    password_hash = Column(String, nullable=False)

    # RBAC role (admin, investor, borrower, owner, etc.)
    role = Column(String, nullable=False)

    # Multi‑tenant domain
    domain_id = Column(Integer, nullable=True)

    created_at = Column(DateTime)

    # Relationships
    vault = relationship("UserVault", back_populates="user")
    assets = relationship("DigitalAsset", back_populates="user")


# ============================================================
# BRAND PROFILE
# ============================================================
class BrandProfile(Base):
    __tablename__ = "brand_profiles"

    id = Column(Integer, primary_key=True, index=True)
    domain = Column(String, unique=True, index=True, nullable=False)

    # Branding fields
    name = Column(String, nullable=False)
    logo_url = Column(String, nullable=True)
    primary_color = Column(String, nullable=True)


# ============================================================
# USER VAULT
# ============================================================
class UserVault(Base):
    __tablename__ = "user_vaults"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="vault")


# ============================================================
# DIGITAL ASSET (NFTs, docs, tokens, etc.)
# ============================================================
class DigitalAsset(Base):
    __tablename__ = "digital_assets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    asset_type = Column(String, nullable=False)
    uri = Column(String, nullable=False)

    user = relationship("User", back_populates="assets")
