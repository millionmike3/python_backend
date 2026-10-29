from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from python_backend.database import SessionLocal
from python_backend.models.brand_profile import BrandProfile
from python_backend.schemas import BrandProfileCreate, BrandProfileOut
from python_backend.rbac import require_admin

router = APIRouter(prefix="/brand", tags=["Brand"])


# ============================================================
# DB DEPENDENCY
# ============================================================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ============================================================
# CREATE BRAND PROFILE (ADMIN ONLY)
# ============================================================
@router.post("/create", response_model=BrandProfileOut)
def create_brand_profile(
    data: BrandProfileCreate,
    admin=Depends(require_admin),
    db: Session = Depends(get_db),
):
    existing = db.query(BrandProfile).filter(BrandProfile.domain == data.domain).first()
    if existing:
        raise HTTPException(400, "Brand profile for this domain already exists")

    brand = BrandProfile(
        domain=data.domain,
        logo_url=data.logo_url,
        primary_color=data.primary_color,
        secondary_color=data.secondary_color,
        created_at=datetime.utcnow(),
    )

    db.add(brand)
    db.commit()
    db.refresh(brand)

    return brand


# ============================================================
# GET BRAND BY ID
# ============================================================
@router.get("/{brand_id}", response_model=BrandProfileOut)
def get_brand_by_id(
    brand_id: int,
    db: Session = Depends(get_db),
):
    brand = db.query(BrandProfile).filter(BrandProfile.id == brand_id).first()
    if not brand:
        raise HTTPException(404, "Brand not found")
    return brand


# ============================================================
# GET BRAND BY DOMAIN
# ============================================================
@router.get("/by-domain/{domain}", response_model=BrandProfileOut)
def get_brand_by_domain(
    domain: str,
    db: Session = Depends(get_db),
):
    brand = db.query(BrandProfile).filter(BrandProfile.domain == domain).first()
    if not brand:
        raise HTTPException(404, "Brand not found")
    return brand
