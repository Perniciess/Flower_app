from aiogram import Router

from .registration import router as registration_router
from .reset_password import router as reset_password_router
from .start import router as start_router

router = Router()
router.include_router(start_router)
router.include_router(registration_router)
router.include_router(reset_password_router)
