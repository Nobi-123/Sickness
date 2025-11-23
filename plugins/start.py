# Nexa — Do Not Remove Credit

import asyncio
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import *
from database import db
from plugins.fsub import checkSub  # force join
from plugins.script import LOG_TEXT, ABOUT_TXT, DS_TEXT, DST_TEXT

# ---------------- Admin Users Count ----------------
@Client.on_message(filters.private & filters.command("users") & filters.user(DS_ADMINS))
async def admin_users(client, message):
    total_users = await db.total_users_count()
    await message.reply_text(f"Total Users: {total_users}")


# ---------------- Start Command ----------------
@Client.on_message(filters.private & filters.command("start"))
async def start(client, message):
    """Send start message and save user in DB."""

    if not await checkSub(client, message):
        return

    user = message.from_user
    user_id = user.id

    # Save user
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

    # Inline buttons
    buttons = [
        [InlineKeyboardButton("🎬 Video", callback_data="video")],
        [InlineKeyboardButton("🤖 Bot & Repo Details", callback_data="bot_details")],
        [InlineKeyboardButton("📌 Disclaimer", url=f"https://t.me/{DS_BOT_USERNAME}?start=disclaimer")],
        [InlineKeyboardButton("📄 Terms", url=f"https://t.me/{DS_BOT_USERNAME}?start=terms")]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)

    # Send start message
    try:
        await message.reply_photo(
            photo=DS_PIC,
            caption=(
                "<b><blockquote>⚠️ This bot contains 18+ Content.\nUse at your own risk.</blockquote></b>"
            ),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    except Exception:
        await message.reply_text(
            "⚠️ This bot contains 18+ content.\n"
            f"Disclaimer: https://t.me/{DS_BOT_USERNAME}?start=disclaimer\n"
            f"Terms: https://t.me/{DS_BOT_USERNAME}?start=terms"
        )


# ---------------- Callback Query Handler ----------------
@Client.on_callback_query()
async def button_handler(client, callback_query):
    data = callback_query.data
    chat_id = callback_query.message.chat.id

    if data == "video":
        if not await checkSub(client, callback_query.message):
            return
        await callback_query.message.edit_text("🎬 Fetching a random video...")

        file = await db.random_file("Video")
        if not file:
            return await callback_query.message.edit_text("❌ No videos found.")

        try:
            sent = await client.copy_message(
                chat_id=chat_id,
                from_chat_id=DS_PORN_FILE_CHANNEL,
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
            await callback_query.message.edit_text("⚠️ Failed to send video.")

    elif data == "bot_details":
        buttons = [[InlineKeyboardButton("Buy Repo", url="https://t.me/Falcoxr")]]
        await callback_query.message.edit_text(
            ABOUT_TXT,
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=enums.ParseMode.HTML,
            disable_web_page_preview=True
        )


# ---------------- User Text Handler ----------------
@Client.on_message(filters.private & filters.text & ~filters.command("start"))
async def handle_user(bot, message):
    text = message.text.lower().strip()
    user_id = message.from_user.id

    if not await checkSub(bot, message):
        return

    if "video" in text:
        # Trigger video logic
        await message.reply_text("🎬 Please click the 'Video' button above for a random video.")

    elif "bot & repo" in text or "bot details" in text:
        buttons = [[InlineKeyboardButton("Buy Repo", url="https://t.me/Falcoxr")]]
        await message.reply_text(
            ABOUT_TXT,
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=enums.ParseMode.HTML,
            disable_web_page_preview=True
        )

    else:
        buttons = [
            [InlineKeyboardButton("🎬 Video", callback_data="video")],
            [InlineKeyboardButton("🤖 Bot & Repo Details", callback_data="bot_details")]
        ]
        await message.reply_text(
            "I didn't understand that. Please use the buttons below:",
            reply_markup=InlineKeyboardMarkup(buttons)
        )