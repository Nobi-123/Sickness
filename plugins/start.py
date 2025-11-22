# NEXA — Do Not Remove Credit

import asyncio
import datetime
import pytz

from config import *
from .database import db
from .fsub import checkSub
from .script import (
    DS_TEXT,
    DST_TEXT,
    LOG_TEXT,
    ABOUT_TXT,
)
from utils import check_and_increment

from pyrogram import Client, filters, enums
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    KeyboardButton,
    ReplyKeyboardMarkup
)

# -------------------------------------------------------
# MAIN USER KEYBOARD (My Plan + Premium Removed)
# -------------------------------------------------------
keyboard = ReplyKeyboardMarkup(
    [
        [KeyboardButton("Desi Video"), KeyboardButton("Videsi Video")],
        [KeyboardButton("Bot & Repo Details")],
    ],
    resize_keyboard=True
)


# -------------------------------------------------------
# ADMIN TOTAL USERS CHECK
# -------------------------------------------------------
@Client.on_message(filters.private & filters.command("users") & filters.user(DS_ADMINS))
async def admin_users(client, message):
    total_users = await db.total_users_count()
    await message.reply_text(f"**Total Users:** `{total_users}`")


# -------------------------------------------------------
# START COMMAND
# -------------------------------------------------------
@Client.on_message(filters.command("start") & filters.private)
async def start(client, message):

    # F-Sub Check
    if not await checkSub(client, message):
        return

    user_id = message.from_user.id

    # Add user to DB if new
    if not await db.is_user_exist(user_id):
        await db.add_user(user_id, message.from_user.first_name)
        await client.send_message(
            DS_LOG_CHANNEL,
            LOG_TEXT.format(user_id, message.from_user.mention)
        )

    # Payload Handling
    payload = message.command[1] if len(message.command) > 1 else None

    if payload == "disclaimer":
        msg = await message.reply_text(DS_TEXT, parse_mode=enums.ParseMode.HTML)
        await asyncio.sleep(180)
        return await msg.delete()

    if payload == "terms":
        msg = await message.reply_text(DST_TEXT, parse_mode=enums.ParseMode.HTML)
        await asyncio.sleep(180)
        return await msg.delete()

    # Send Start Banner
    await message.reply_photo(
        photo=DS_PIC,
        caption=f"""
<b><blockquote>⚠️ Contains 18+ Content  
Use At Your Own Risk.</blockquote>

Read our  
<a href="https://t.me/{DS_BOT_USERNAME}?start=disclaimer">Disclaimer</a> •  
<a href="https://t.me/{DS_BOT_USERNAME}?start=terms">Terms</a></b>
""",
        reply_markup=keyboard,
        has_spoiler=True,
        parse_mode=enums.ParseMode.HTML
    )

    await message.reply_text("Select your category 👇🏻")


# -------------------------------------------------------
# USER REQUEST HANDLER
# -------------------------------------------------------
@Client.on_message(filters.private & filters.text & ~filters.command("start"))
async def handle_request(bot, message):

    text = message.text.lower().strip()
    user_id = message.from_user.id

    # ============================
    # VIDESI CONTENT
    # ============================
    if "videsi video" in text:

        if not await checkSub(bot, message):
            return

        tag = "videsi"
        channel = DS_VIDESI_FILE_CHANNEL

        # Daily limit check
        if not await check_and_increment(user_id, tag):
            return await message.reply("You reached your today’s limit. Try tomorrow.")

        file = await db.random_file(tag)
        if not file:
            return await message.reply("No video found.")

        try:
            msg = await bot.copy_message(
                chat_id=user_id,
                from_chat_id=channel,
                message_id=file["msg_id"],
                caption=(
                    "<b>Powered by <a href='https://t.me/NexaCoders'>Nexa Coders</a></b>"
                    "\n\n<blockquote>This file auto-deletes in 1 minute.</blockquote>"
                )
            )
            await asyncio.sleep(60)
            await msg.delete()

        except:
            await db.delete_file(file["msg_id"])
            await message.reply("Video not found. Removed from database.")


    # ============================
    # DESI CONTENT
    # ============================
    elif "desi video" in text:

        if not await checkSub(bot, message):
            return

        tag = "desi"
        channel = DS_DESI_FILE_CHANNEL

        if not await check_and_increment(user_id, tag):
            return await message.reply("⛔ Daily limit over. Try again tomorrow.")

        file = await db.random_file(tag)
        if not file:
            return await message.reply("No video found.")

        try:
            msg = await bot.copy_message(
                chat_id=user_id,
                from_chat_id=channel,
                message_id=file["msg_id"],
                caption=(
                    "<b>Powered by <a href='https://t.me/TncNetwork'>TNC Network</a></b>"
                    "\n\n<blockquote>This file auto-deletes in 1 minute.</blockquote>"
                )
            )
            await asyncio.sleep(60)
            await msg.delete()

        except:
            await db.delete_file(file["msg_id"])
            await message.reply("⚠️ File not accessible. Deleted from DB.")


    # ============================
    # BOT INFO
    # ============================
    elif "bot & repo details" in text:

        buttons = [[InlineKeyboardButton("Buy Repo", url="https://t.me/Falcoxr")]]

        msg = await message.reply_text(
            ABOUT_TXT,
            reply_markup=InlineKeyboardMarkup(buttons),
            disable_web_page_preview=True,
            parse_mode=enums.ParseMode.HTML
        )

        await asyncio.sleep(300)
        await msg.delete()


# NEXA  — Do Not Remove Credit