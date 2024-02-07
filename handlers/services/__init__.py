from aiogram import Router

from .create_services import dialog, ServiceDialog

router = Router(name='services')
router.include_routers(dialog)
