from telegram import ReplyKeyboardMarkup, Update, User, Message
from telegram.ext import filters
from sqlalchemy.ext.asyncio import AsyncSession

from application.base import APPHandlers
from application.context import CustomContext
from configurations import logger
from content import CONTENT
from database import crud
from database.models import UserModel
from exceptions import NoPhotosException
from utils import get_func_name

handler = APPHandlers()


@handler.command()
async def start(user: UserModel, message: Message) -> None:
    logger.info(f'Call: {get_func_name()}')

    await message.reply_text(
        text=CONTENT.messages.start.format(username=user.tg.username or ''),
        reply_markup=ReplyKeyboardMarkup(CONTENT.keyboard, resize_keyboard=True),
    )


@handler.message()
async def photo(user: UserModel, message: Message, session: AsyncSession) -> None:
    if (await crud.get_media_count(session, user.storage)) > 1:
        await message.reply_text(text=CONTENT.messages.receive_photo.basic.get())
    else:
        await message.reply_text(text=CONTENT.messages.receive_photo.initial.get())


@handler.message(filters.Regex(r'|'.join(CONTENT.buttons)))
async def emoji_food(user: UserModel, message: Message, session: AsyncSession) -> None:
    try:
        photo = await crud.get_media_id(session, user.storage)
    except NoPhotosException:
        await message.reply_text(CONTENT.messages.exceptions.no_photos)
    else:
        await message.reply_photo(photo, CONTENT.messages.send_photo.any.get())


@handler.message()
async def all(message: Message) -> None:
    await message.reply_text(text=CONTENT.messages.regular.get())
