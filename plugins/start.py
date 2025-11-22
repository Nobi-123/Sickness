# Nexa  — Do Not Remove Credit

import asyncio
import datetime
import pytz

from config import *
from .database import db
from .fsub import checkSub
from .script import (
    LOG_TEXT,
    ABOUT_TXT,
    DS_TEXT,
    DST_TEXT,
)
from utils import check_and_increment  # kept for compatibility (currently unlimited if you removed limits)
from pyrogram import Client, filters, enums
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    KeyboardButton,
    ReplyKeyboardMarkup
)

# -------------------------------------------------------
# UI TEXT (from your provided strings)
# -------------------------------------------------------
# LOG_TEXT, ABOUT_TXT, DS_TEXT, DST_TEXT are imported from .script
# (If you prefer to keep them here instead, move the definitions into this file)

# -------------------------------------------------------
# MAIN USER KEYBOARD (My Plan + Premium removed)
# -------------------------------------------------------
keyboard = ReplyKeyboardMarkup(
    [
        [KeyboardButton("Desi Video"), KeyboardButton("Videsi Video")],
        [KeyboardButton("Bot & Repo Details")],
    ],
    resize_keyboard=True,
    one_time_keyboard=False
)


# -------------------------------------------------------
# ADMIN: Total Users Count
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

    # Ensure user joined required channel (FSub)
    if not await checkSub(client, message):
        return

    user_id = message.from_user.id

    # Add user to DB if new and log
    if not await db.is_user_exist(user_id):
        await db.add_user(user_id, message.from_user.first_name or "Unknown")
        try:
            await client.send_message(
                DS_LOG_CHANNEL,
                LOG_TEXT.format(user_id, message.from_user.mention)
            )
        except Exception:
            # silently ignore logging errors (e.g., channel missing)
            pass

    # Payload handling (disclaimer/terms)
    payload = message.command[1] if len(message.command) > 1 else None

    if payload == "disclaimer":
        msg = await message.reply_text(DS_TEXT, parse_mode=enums.ParseMode.HTML)
        await asyncio.sleep(180)
        return await msg.delete()

    if payload == "terms":
        msg = await message.reply_text(DST_TEXT, parse_mode=enums.ParseMode.HTML)
        await asyncio.sleep(180)
        return await msg.delete()

    # Send start banner/photo
    try:
        await message.reply_photo(
            photo=DS_PIC,
            caption=(
                f"<b><blockquote>⚠️ Contains 18+ Content\nUse At Your Own Risk.</blockquote>\n\n"
                f"Read our <a href=\"https://t.me/{DS_BOT_USERNAME}?start=disclaimer\">Disclaimer</a> & "
                f"<a href=\"https://t.me/{DS_BOT_USERNAME}?start=terms\">Terms</a></b>"
            ),
            reply_markup=keyboard,
            has_spoiler=True,
            parse_mode=enums.ParseMode.HTML
        )
    except Exception:
        # fallback to text if sending photo fails
        await message.reply_text(
            (
                "⚠️ Contains 18+ Content — Use At Your Own Risk.\n\n"
                f"Read our Disclaimer: https://t.me/{DS_BOT_USERNAME}?start=disclaimer\n"
                f"Read our Terms: https://t.me/{DS_BOT_USERNAME}?start=terms"
            )
        )

    await message.reply_text("Select your category 👇🏻")


# -------------------------------------------------------
# USER TEXT HANDLER
# -------------------------------------------------------
@Client.on_message(filters.private & filters.text & ~filters.command("start"))
async def handle_request(bot, message):

    text = message.text.lower().strip()
    user_id = message.from_user.id

    # ------------------------------
    # VIDESI VIDEO
    # ------------------------------
    if "videsi video" in text:

        # F-Sub check
        if not await checkSub(bot, message):
            return

        tag = "videsi"
        channel = DS_VIDESI_FILE_CHANNEL

        # check_and_increment kept for compatibility (if you removed limits it should return True)
        ok = await check_and_increment(user_id, tag)
        if not ok:
            return await message.reply("You reached today's limit. Try again tomorrow.")

        file = await db.random_file(tag)
        if not file:
            return await message.reply("No video found.")

        try:
            sent = await bot.copy_message(
                chat_id=message.chat.id,
                from_chat_id=channel,
                message_id=file["msg_id"],
                caption=(
                    "<b>Powered by <a href='https://t.me/NexaCoders'>Nexa Network</a></b>\n\n"
                    "<blockquote>This file auto-deletes in 1 minute.</blockquote>"
                ),
                parse_mode=enums.ParseMode.HTML
            )
            await asyncio.sleep(60)
            try:
                await sent.delete()
            except Exception:
                pass
        except Exception:
            # remove stale DB entry if message can't be copied
            try:
                await db.delete_file(file["msg_id"])
            except Exception:
                pass
            await message.reply("⚠️ Failed to send video. It may have been deleted.")

    # ------------------------------
    # DESI VIDEO
    # ------------------------------
    elif "desi video" in text:

        # F-Sub check
        if not await checkSub(bot, message):
            return

        tag = "desi"
        channel = DS_DESI_FILE_CHANNEL

        ok = await check_and_increment(user_id, tag)
        if not ok:
            return await message.reply("You reached today's limit. Try again tomorrow.")

        file = await db.random_file(tag)
        if not file:
            return await message.reply("No video found.")

        try:
            sent = await bot.copy_message(
                chat_id=message.chat.id,
                from_chat_id=channel,
                message_id=file["msg_id"],
                caption=(
                    "<b>Powered by <a href='https://t.me/NexaCoders'>Nexa Network</a></b>\n\n"
                    "<blockquote>This file auto-deletes in 1 minute.</blockquote>"
                ),
                parse_mode=enums.ParseMode.HTML
            )
            await asyncio.sleep(60)
            try:
                await sent.delete()
            except Exception:
                pass
        except Exception:
            try:
                await db.delete_file(file["msg_id"])
            except Exception:
                pass
            await message.reply("⚠️ Failed to send video. It may have been deleted.")

    # ------------------------------
    # BOT & REPO DETAILS
    # ------------------------------
    elif "bot & repo details" in text or "bot & repo" in text or "bot details" in text:
        buttons = [[InlineKeyboardButton("Buy Repo", url="https://t.me/Falcoxr")]]
        try:
            info_msg = await message.reply_text(
                text=ABOUT_TXT,
                reply_markup=InlineKeyboardMarkup(buttons),
                disable_web_page_preview=True,
                parse_mode=enums.ParseMode.HTML
            )
            await asyncio.sleep(300)
            try:
                await info_msg.delete()
            except Exception:
                pass
        except Exception:
            await message.reply_text(ABOUT_TXT, parse_mode=enums.ParseMode.HTML)

    # ------------------------------
    # FALLBACK (unknown text)
    # ------------------------------
    else:
        # Friendly hint
        await message.reply_text(
            "I didn't understand that. Use the keyboard below or send one of:\n"
            "- Desi Video\n- Videsi Video\n- Bot & Repo Details",
            reply_markup=keyboard
        )


# Nexa  — Do Not Remove Credit