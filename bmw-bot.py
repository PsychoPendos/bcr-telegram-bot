import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import ContentType

TOKEN = '8125139471:AAEvu0HTA-HL_dzo0u8FRJiBZbGiYVpTzRQ'
ALLOWED_CHAT_ID = '-1002164509372'

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


async def is_user_in_chat(user_id: int, chat_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except Exception as e:
        logging.error(f"Error checking user in chat: {e}")
        return False


@dp.message(Command('start'))
async def start_handler(message: types.Message):
    chat_id = message.chat.id
    if chat_id == int(ALLOWED_CHAT_ID) or message.chat.type == 'private':
        if message.chat.type == 'private' and not await is_user_in_chat(
                message.from_user.id, int(ALLOWED_CHAT_ID)):
            await message.answer("У вас нет доступа к этому боту.")
        else:
            await message.answer("Привет! Я твой бот.")
    else:
        await message.answer("У вас нет доступа к этому боту.")


@dp.message(Command('order'))
async def order_handler(message: types.Message):
    if message.chat.id == int(ALLOWED_CHAT_ID) or await is_user_in_chat(
            message.from_user.id, int(ALLOWED_CHAT_ID)):
        await message.answer("Заказать расходники и запчасти из Европы ✈️")


@dp.message(Command('3dparts'))
async def parts_3d_handler(message: types.Message):
    if message.chat.id == int(ALLOWED_CHAT_ID) or await is_user_in_chat(
            message.from_user.id, int(ALLOWED_CHAT_ID)):
        await message.answer("Универсальные 3D решения для вашей машины 🔬")


@dp.message(Command('service'))
async def service_handler(message: types.Message):
    if message.chat.id == int(ALLOWED_CHAT_ID) or await is_user_in_chat(
            message.from_user.id, int(ALLOWED_CHAT_ID)):
        await message.answer("Проверенный автосервис в Москве 🔧")


@dp.message(Command('detailing'))
async def detailing_handler(message: types.Message):
    if message.chat.id == int(ALLOWED_CHAT_ID) or await is_user_in_chat(
            message.from_user.id, int(ALLOWED_CHAT_ID)):
        await message.answer("Детейлинг в Москве 💎")


@dp.message(
        lambda message: message.content_type == ContentType.NEW_CHAT_MEMBERS)
async def welcome_handler(message: types.Message):
    if message.chat.id == int(ALLOWED_CHAT_ID):
        for member in message.new_chat_members:
            await message.answer(f"Добро пожаловать, {member.full_name}!")


async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
