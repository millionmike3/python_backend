# Make python_backend a proper Python package

# Expose key modules for easier imports
from .database import Base, engine, SessionLocal
from .models import *
from .schemas import *
from .services import *
