from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from python_backend.database import SessionLocal

# Correct model imports
from python_backend.models.domain import Domain
from python_backend.models.users import User
from python_backend.models.brand_profile import BrandProfile


# Remove BrandProfile unless you actually have it
# from python_backend.models.brand_profile import BrandProfile

from python_backend.schemas import DomainCreate, DomainOut
from python_backend.rbac import require_admin, require_owner


router = APIRouter(prefix="/domains", tags=["Domains"])


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
# CREATE DOMAIN (ADMIN ONLY)
# ============================================================
@router.post("/create", response_model=DomainOut)
def create_domain(
    data: DomainCreate,
    admin=Depends(require_admin),
    db: Session = Depends(get_db),
):
    owner = db.query(User).filter(User.id == data.owner_user_id).first()
    if not owner:
        raise HTTPException(404, "Owner user not found")

    if owner.role != "OWNER":
        raise HTTPException(400, "User must have OWNER role")

    domain = Domain(
        name=data.name,
        brand=data.brand,
        owner_user_id=data.owner_user_id,
        created_at=datetime.utcnow(),
    )

    db.add(domain)
    db.commit()
    db.refresh(domain)

    owner.domain_id = domain.id
    db.commit()

    return domain


# ============================================================
# GET DOMAIN BY ID (OWNER OR ADMIN)
# ============================================================
@router.get("/{domain_id}", response_model=DomainOut)
def get_domain(
    domain_id: int,
    user=Depends(require_owner),
    db: Session = Depends(get_db),
):
    domain = db.query(Domain).filter(Domain.id == domain_id).first()
    if not domain:
        raise HTTPException(404, "Domain not found")

    if user.role == "OWNER" and user.domain_id != domain_id:
        raise HTTPException(403, "Not authorized")

    return domain


# ============================================================
# OWNER VIEW THEIR DOMAIN
# ============================================================
@router.get("/owner/me", response_model=DomainOut)
def owner_view_domain(
    owner=Depends(require_owner),
    db: Session = Depends(get_db),
):
    domain = db.query(Domain).filter(Domain.id == owner.domain_id).first()
    if not domain:
        raise HTTPException(404, "Domain not found")

    return domain


# ============================================================
# ADMIN LIST ALL DOMAINS
# ============================================================
@router.get("/admin/all", response_model=list[DomainOut])
def admin_list_domains(
    admin=Depends(require_admin),
    db: Session = Depends(get_db),
):
    return db.query(Domain).all()


# ============================================================
# UPDATE DOMAIN (ADMIN ONLY)
# ============================================================
@router.put("/admin/{domain_id}", response_model=DomainOut)
def admin_update_domain(
    domain_id: int,
    data: DomainCreate,
    admin=Depends(require_admin),
    db: Session = Depends(get_db),
):
    domain = db.query(Domain).filter(Domain.id == domain_id).first()
    if not domain:
        raise HTTPException(404, "Domain not found")

    domain.name = data.name
    domain.brand = data.brand
    domain.owner_user_id = data.owner_user_id

    owner = db.query(User).filter(User.id == data.owner_user_id).first()
    if not owner:
        raise HTTPException(404, "Owner user not found")

    owner.domain_id = domain.id

    db.commit()
    db.refresh(domain)

    return domain
