# python_backend/routers/__init__.py

from .auth import router as auth_router
from .domains import router as domains_router
from .owners import router as owners_router
from .investors import router as investors_router
from .borrowers import router as borrowers_router
from .mortgage import router as mortgage_router
from .property_sanitizer import router as property_router
from .bulk_tape import router as bulk_tape_router
from .credit import router as credit_router
from .underwriting import router as underwriting_router
from .panels import router as panels_router
from .users import router as users_router
from .leaderboard import router as leaderboard_router

__all__ = [
    "auth_router",
    "domains_router",
    "owners_router",
    "investors_router",
    "borrowers_router",
    "mortgage_router",
    "property_router",
    "bulk_tape_router",
    "credit_router",
    "underwriting_router",
    "panels_router",
    "users_router",
    "leaderboard_router",
]
