# Nexa — Do Not Remove Credit

import asyncio
from pyrogram import Client, filters, enums
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup
)

from config import *
from plugins.database import db          # Updated import
from fsub import checkSub                # fsub.py is in root, so import directly
from script import LOG_TEXT, ABOUT_TXT, DS_TEXT, DST_TEXT
from utils import check_and_increment


# =====================================================
# USER MAIN KEYBOARD
# =====================================================

keyboard = ReplyKeyboardMarkup(
    [
        [KeyboardButton("Corn Video")],
        [KeyboardButton("Bot & Repo Details")],
    ],
    resize_keyboard=True
)


# =====================================================
# ADMIN COMMAND: USER COUNT
# =====================================================

@Client.on_message(filters.private & filters.command("users") & filters.user(DS_ADMINS))
async def admin_users(client, message):
    total_users = await db.total_users_count()
    await message.reply_text(f"Total Users: {total_users}")


# =====================================================
# START COMMAND
# =====================================================

@Client.on_message(filters.command("start") & filters.private)
async def start(client, message):

    # Force Subscription Check
    if not await checkSub(client, message):
        return

    user = message.from_user
    user_id = user.id

    # Save user to DB
    if not await db.is_user_exist(user_id):
        await db.add_user(user_id, user.first_name or "User")

        try:
            await client.send_message(
                DS_LOG_CHANNEL,
                LOG_TEXT.format(user_id, user.mention)
            )
        except:
            pass

    # --------------------------------------
    # PAYLOAD HANDLING
    # --------------------------------------

    payload = message.command[1] if len(message.command) > 1 else None

    if payload == "disclaimer":
        msg = await message.reply_text(DS_TEXT, parse_mode="html")
        await asyncio.sleep(180)
        return await msg.delete()

    if payload == "terms":
        msg = await message.reply_text(DST_TEXT, parse_mode="html")
        await asyncio.sleep(180)
        return await msg.delete()

    # --------------------------------------
    # SEND START MENU
    # --------------------------------------

    try:
        await message.reply_photo(
            photo=DS_PIC,
            caption=(
                "<b><blockquote>⚠️ This bot contains 18+ Content.\n"
                "Use at your own risk.</blockquote>\n\n"
                f"📌 Read our <a href='https://t.me/{DS_BOT_USERNAME}?start=disclaimer'>Disclaimer</a> and "
                f"<a href='https://t.me/{DS_BOT_USERNAME}?start=terms'>Terms</a></b>"
            ),
            reply_markup=keyboard,
            has_spoiler=True,
            parse_mode="html"
        )
    except:
        await message.reply_text(
            "⚠️ This bot contains 18+ content.\n"
            f"Disclaimer: https://t.me/{DS_BOT_USERNAME}?start=disclaimer\n"
            f"Terms: https://t.me/{DS_BOT_USERNAME}?start=terms"
        )

    await message.reply_text("Select your category 👇🏻", reply_markup=keyboard)


# =====================================================
# USER TEXT HANDLER
# =====================================================

@Client.on_message(filters.private & filters.text & ~filters.command("start"))
async def handle_user(client, message):

    text = message.text.lower().strip()
    user_id = message.from_user.id

    # --------------------------------------------------
    # DESI / CORN VIDEO
    # --------------------------------------------------

    if "corn video" in text or "desi video" in text:

        # FSUB Check
        if not await checkSub(client, message):
            return

        tag = "corn"
        channel = DS_DESI_FILE_CHANNEL

        # Daily Limit
        ok = await check_and_increment(user_id, tag)
        if not ok:
            return await message.reply("⚠️ Daily limit reached.\nTry again tomorrow!")

        # Fetch Random File
        file = await db.random_file(tag)
        if not file:
            return await message.reply("❌ No Corn videos found.")

        try:
            sent = await client.copy_message(
                chat_id=message.chat.id,
                from_chat_id=channel,
                message_id=file["msg_id"],
                caption=(
                    "<b>Powered by <a href='https://t.me/NexaCoders'>Nexa Network</a></b>\n\n"
                    "<blockquote>This file will auto-delete in 1 minute.</blockquote>"
                ),
                parse_mode="html"
            )

            # Auto-delete after 60 seconds
            await asyncio.sleep(60)
            try:
                await sent.delete()
            except:
                pass

        except:
            # If file deleted from channel → remove from DB
            try:
                await db.delete_file(file["msg_id"])
            except:
                pass

            await message.reply("⚠️ Failed to send video.\nFile may have been deleted.")

    # --------------------------------------------------
    # BOT DETAILS / REPO
    # --------------------------------------------------

    elif "bot & repo" in text or "bot details" in text:

        buttons = [
            [InlineKeyboardButton("Buy Repo", url="https://t.me/Falcoxr")]
        ]

        try:
            msg = await message.reply_text(
                ABOUT_TXT,
                reply_markup=InlineKeyboardMarkup(buttons),
                parse_mode="html",
                disable_web_page_preview=True
            )

            await asyncio.sleep(300)
            try:
                await msg.delete()
            except:
                pass

        except:
            await message.reply_text(ABOUT_TXT, parse_mode="html")

    # --------------------------------------------------
    # FALLBACK TEXT
    # --------------------------------------------------

    else:
        await message.reply_text(
            "I didn't understand that.\nUse the menu below 👇🏻",
            reply_markup=keyboard
        )