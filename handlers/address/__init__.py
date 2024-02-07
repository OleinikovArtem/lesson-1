from aiogram import Router

from .create_address import router as create_addres_router

router = Router(name='address')
router.include_routers(create_addres_router)
