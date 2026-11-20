import asyncio
import logging

from aiogram import Bot
from aiogram import Dispatcher
from aiogram.types import BotCommandScopeDefault
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from vpn_bot.daemon_tasks.check_expiry_date import Subscriptions
from vpn_bot.db.helpers.configs import Configs
from vpn_bot.db.helpers.services import Services
from vpn_bot.db.helpers.tickets import Tickets
from vpn_bot.db.helpers.users import Users
from vpn_bot.db.manager import DBManager
from vpn_bot.handlers.admin import admin_router
from vpn_bot.handlers.main_menu import main_router
from vpn_bot.handlers.payment import payment_router
from vpn_bot.handlers.referral import referral_router
from vpn_bot.handlers.support import support_router
from vpn_bot.handlers.vpn import service_router
from vpn_bot.keyboards.main_menu import default_commands
from vpn_bot.middlewares.admin import AdminCheckMiddleware
from vpn_bot.middlewares.db_manager import DatabaseMiddleware
from vpn_bot.middlewares.vpn_manager import VpnManagerMiddleware
from vpn_bot.settings import DBSettings
from vpn_bot.settings import TelegramSettings
from vpn_bot.settings import XUISettings
from vpn_bot.utils.storage import Storage
from vpn_bot.utils.vpn_manager import VpnManager

from hostmon.config import Config


async def start() -> None:
    bot = Bot(Config().BOT_TOKEN)
    dp = Dispatcher()
    routers = [
        service_router,
    ]
    storage = _create_storage()
    admin_router.message.middleware.register(AdminCheckMiddleware(storage))

    for router in routers:
        dp.include_router(router)

    await bot.set_my_commands(default_commands, scope=BotCommandScopeDefault())

    _add_daemon_tasks(bot, storage)
    await _add_middlewares(dp, storage)
    await dp.start_polling(bot)


def _add_daemon_tasks(bot: Bot, storage: Storage) -> None:
    scheduler = AsyncIOScheduler()
    subscription_manager = Subscriptions(bot, storage)

    scheduler.add_job(
        subscription_manager.check_subscriptions,
        trigger="interval",
        hours=24,
    )
    scheduler.start()


async def _vpn_manager() -> AsyncApi:
    vpn_api = AsyncApi.from_env()
    max_retries = 10
    vpn_managers = [
        vpn_api.client,
        vpn_api.inbound,
        vpn_api.database,
        vpn_api.server,
    ]
    for vpn in vpn_managers:
        vpn.max_retries = max_retries

    return vpn_api


async def _add_middlewares(dp: Dispatcher, storage: Storage) -> None:
    vpn_api = await _vpn_manager()
    await vpn_api.login()

    middlewares = [
        DatabaseMiddleware(storage),
        VpnManagerMiddleware(VpnManager(vpn_api, XUISettings().REMARK)),
    ]

    for middleware in middlewares:
        dp.update.middleware(middleware)


def _create_storage() -> Storage:
    db_manager = DBManager(DBSettings())
    services = Services(db_manager)
    tickets = Tickets(db_manager)
    users = Users(db_manager)
    configs = Configs(db_manager)
    return Storage(services, tickets, users, configs)

