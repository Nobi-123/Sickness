# Nexa — Do Not Remove Credit

import asyncio
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import *
from database import db
from plugins.fsub import checkSub
from plugins.script import LOG_TEXT, ABOUT_TXT, DS_TEXT, DST_TEXT
from utils import check_and_increment


# =====================================================
# ADMIN: USER COUNT
# =====================================================
@Client.on_message(filters.private & filters.command("users") & filters.user(DS_ADMINS))
async def admin_users(client, message):
    total_users = await db.total_users_count()
    await message.reply_text(f"Total Users: {total_users}")


# =====================================================
# START COMMAND
# =====================================================
@Client.on_message(filters.private & filters.command("start"))
async def start(client, message):
    """Send start message with optional payload handling."""
    
    if not await checkSub(client, message):
        return

    user = message.from_user
    user_id = user.id

    # Save user in DB
    if not await db.is_user_exist(user_id):
        await db.add_user(user_id, user.first_name or "User")
        try:
            await client.send_message(
                DS_LOG_CHANNEL,
                LOG_TEXT.format(user_id, user.mention)
            )
        except Exception:
            pass

    # Handle payloads
    payload = message.command[1] if len(message.command) > 1 else None
    if payload == "disclaimer":
        msg = await message.reply_text(DS_TEXT, parse_mode=enums.ParseMode.HTML)
        await asyncio.sleep(180)
        return await msg.delete()
    if payload == "terms":
        msg = await message.reply_text(DST_TEXT, parse_mode=enums.ParseMode.HTML)
        await asyncio.sleep(180)
        return await msg.delete()

    # Main start message
    try:
        await message.reply_photo(
            photo=DS_PIC,
            caption=(
                "<b><blockquote>⚠️ This bot contains 18+ Content.\nUse at your own risk.</blockquote>\n\n"
                f"📌 Read our <a href='https://t.me/{DS_BOT_USERNAME}?start=disclaimer'>Disclaimer</a> and "
                f"<a href='https://t.me/{DS_BOT_USERNAME}?start=terms'>Terms</a></b>"
            ),
            parse_mode=enums.ParseMode.HTML
        )
    except Exception:
        await message.reply_text(
            "⚠️ This bot contains 18+ content.\n"
            f"Disclaimer: https://t.me/{DS_BOT_USERNAME}?start=disclaimer\n"
            f"Terms: https://t.me/{DS_BOT_USERNAME}?start=terms"
        )


# =====================================================
# USER TEXT HANDLER
# =====================================================
@Client.on_message(filters.private & filters.text & ~filters.command("start"))
async def handle_user(bot, message):
    text = message.text.lower().strip()
    user_id = message.from_user.id

    # -----------------------------
    # Video Section
    # -----------------------------
    if "video" in text:
        if not await checkSub(bot, message):
            return

        tag = "Video"
        channel = DS_PORN_FILE_CHANNEL

        # Daily limit
        ok = await check_and_increment(user_id, tag)
        if not ok:
            return await message.reply("⚠️ You reached today's limit.\nTry again tomorrow!")

        # Fetch random video
        file = await db.random_file(tag)
        if not file:
            return await message.reply("❌ No videos found.")

        try:
            sent = await bot.copy_message(
                chat_id=message.chat.id,
                from_chat_id=channel,
                message_id=file["msg_id"],
                caption=(
                    "<b>Powered by <a href='https://t.me/NexaCoders'>Nexa Network</a></b>\n\n"
                    "<blockquote>This file will auto-delete in 1 minute.</blockquote>"
                ),
                parse_mode=enums.ParseMode.HTML
            )
            await asyncio.sleep(60)
            try:
                await sent.delete()
            except Exception:
                pass
        except Exception:
            # Remove from DB if missing
            try:
                await db.delete_file(file["msg_id"])
            except Exception:
                pass
            await message.reply("⚠️ Failed to send video. It may have been deleted.")

    # -----------------------------
    # Bot Details
    # -----------------------------
    elif "bot & repo" in text or "bot details" in text:
        buttons = [[InlineKeyboardButton("Buy Repo", url="https://t.me/Falcoxr")]]
        try:
            msg = await message.reply_text(
                ABOUT_TXT,
                reply_markup=InlineKeyboardMarkup(buttons),
                parse_mode=enums.ParseMode.HTML,
                disable_web_page_preview=True
            )
            await asyncio.sleep(300)
            try:
                await msg.delete()
            except Exception:
                pass
        except Exception:
            await message.reply_text(ABOUT_TXT, parse_mode=enums.ParseMode.HTML)

    # -----------------------------
    # Fallback
    # -----------------------------
    else:
        await message.reply_text(
            "I didn't understand that. Please type 'Video' or 'Bot & Repo Details'."
        )