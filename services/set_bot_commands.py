from aiogram import Bot
from aiogram.types import BotCommand


async def set_default_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="🛍️ Botni ishga tushirish"),
        BotCommand(command="help", description="❓ Yordam va savollar"),
        BotCommand(command="shop", description="🏪 Do'konni ochish"),
        BotCommand(command="cart", description="🛒 Savatim"),
        BotCommand(command="profile", description="👤 Mening profilim"),
        BotCommand(command="orders", description="📋 Mening buyurtmalarim"),
        BotCommand(command="reviews", description="⭐ Mening sharhlarim"),
        BotCommand(command="admin", description="⚙️ Admin panel"),
    ]
    await bot.set_my_commands(commands)
