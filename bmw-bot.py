import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F, Router, types
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import (FSInputFile, KeyboardButton, Message,
                           ReplyKeyboardMarkup)
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')
ALLOWED_CHAT_ID = os.getenv('ALLOWED_CHAT_ID')

router = Router()

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
dp.include_router(router)

order_button = KeyboardButton(text='Запчасти')
service_button = KeyboardButton(text='Сервис')
printparts_button = KeyboardButton(text='3D печать')
detailing_button = KeyboardButton(text='Детейлинг')

reply_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [order_button, service_button],
        [printparts_button, detailing_button]
    ],
    resize_keyboard=True
)


@router.message(F.text == 'Запчасти')
async def handle_order(message: types.Message):
    await process_order(message)


@router.message(F.text == 'Сервис')
async def handle_service(message: types.Message):
    await process_service(message)


@router.message(F.text == '3D печать')
async def handle_3dparts(message: types.Message):
    await process_3dparts(message)


@router.message(F.text == 'Детейлинг')
async def handle_detailing(message: types.Message):
    await process_detailing(message)


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
            with open(
                'answers/hello_message.txt', 'r', encoding='utf-8'
            ) as file:
                hello_message = file.read()
                personalized_message = hello_message.replace(
                        "{username}", message.from_user.full_name)
                await message.answer(
                        personalized_message, reply_markup=reply_keyboard)
    else:
        await message.answer("У вас нет доступа к этому боту.")


async def process_order(message: types.Message):
    try:
        user_id = message.from_user.id
        chat_id = message.chat.id
        logging.info(f"Checking user {user_id} in chat {chat_id}")
        is_user_allowed = await is_user_in_chat(user_id, int(ALLOWED_CHAT_ID))
        logging.info(f"User allowed: {is_user_allowed}")
        if is_user_allowed:
            with open(
                'answers/order_message.txt', 'r', encoding='utf-8'
            ) as file:
                order_message = file.read()
            logging.info("Order message read successfully")
            await bot.send_message(
                    chat_id, order_message, reply_markup=reply_keyboard)
        else:
            await bot.send_message(chat_id, "У вас нет доступа к этому боту.")
    except Exception as e:
        logging.error(f"Error in process_order: {e}")
        await bot.send_message(chat_id, f"Произошла ошибка: {e}")


async def process_service(message: types.Message):
    try:
        user_id = message.from_user.id
        chat_id = message.chat.id
        logging.info(f"Checking user {user_id} in chat {chat_id}")

        is_user_allowed = await is_user_in_chat(user_id, chat_id)
        logging.info(f"User allowed: {is_user_allowed}")

        if is_user_allowed:
            with open(
                'answers/service_message.txt', 'r', encoding='utf-8'
            ) as file:
                service_message = file.read()
            logging.info("Service message read successfully")
            await bot.send_message(
                chat_id,
                service_message,
                reply_markup=reply_keyboard
            )
        else:
            await bot.send_message(
                    message.from_user.id, "У вас нет доступа к этому боту.")
    except Exception as e:
        logging.error(f"Error in process_service: {e}")
        await bot.send_message(chat_id, f"Произошла ошибка: {e}")


async def process_3dparts(message: types.Message):
    try:
        user_id = message.from_user.id
        chat_id = message.chat.id
        logging.info(f"Checking user {user_id} in chat {chat_id}")
        is_user_allowed = await is_user_in_chat(user_id, chat_id)
        logging.info(f"User allowed: {is_user_allowed}")
        if is_user_allowed:
            with open(
                'answers/3dparts_message.txt', 'r', encoding='utf-8'
            ) as file:
                printparts_message = file.read()
            logging.info("3D parts message read successfully")
            photo = FSInputFile('files/photos/photo_2024-09-24_08-47-18.jpg')
            await bot.send_photo(
                chat_id,
                photo,
                caption=printparts_message,
                reply_markup=reply_keyboard
            )
        else:
            await bot.send_message(
                    message.from_user.id, "У вас нет доступа к этому боту.")
    except Exception as e:
        logging.error(f"Error in process_service: {e}")
        await bot.send_message(chat_id, f"Произошла ошибка: {e}")


async def process_detailing(message: types.Message):
    try:
        user_id = message.from_user.id
        chat_id = message.chat.id
        logging.info(f"Checking user {user_id} in chat {chat_id}")
        is_user_allowed = await is_user_in_chat(user_id, chat_id)
        logging.info(f"User allowed: {is_user_allowed}")
        if is_user_allowed:
            with open(
                'answers/detailing_message.txt', 'r', encoding='utf-8'
            ) as file:
                detailing_message = file.read()
            logging.info("Detailing message read successfully")
            video = FSInputFile('files/videos/IMG_5497.MP4')
            await bot.send_video(
                chat_id,
                video,
                caption=detailing_message,
                reply_markup=reply_keyboard
            )
        else:
            await bot.send_message(
                    message.from_user.id, "У вас нет доступа к этому боту.")
    except Exception as e:
        logging.error(f"Error in process_service: {e}")
        await bot.send_message(chat_id, f"Произошла ошибка: {e}")


@dp.message(F.content_type == types.ContentType.NEW_CHAT_MEMBERS)
async def welcome_handler(message: Message):
    if message.chat.id == int(ALLOWED_CHAT_ID):
        with open(
                'answers/welcome_message.txt', 'r', encoding='utf-8') as file:
            welcome_message = file.read()
        for member in message.new_chat_members:
            personalized_message = welcome_message.replace(
                    "{username}", member.full_name)
            await message.answer(
                    personalized_message, reply_markup=reply_keyboard)


async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
