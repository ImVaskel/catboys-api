from catboys.app.routes import random
from fastapi import APIRouter


router = APIRouter()
router.include_router(random.router, prefix="/random")
