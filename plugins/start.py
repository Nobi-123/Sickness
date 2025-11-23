# Nexa — Do Not Remove Credit

import asyncio
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import *
from database import db
from plugins.fsub import checkSub  # force join
from plugins.script import LOG_TEXT, ABOUT_TXT


# ---------------- Admin Only: Stats ----------------
@Client.on_message(filters.private & filters.command("stats") & filters.user(DS_ADMINS))
async def stats_handler(client, message):
    total_users = await db.total_users_count()
    await message.reply_text(f"📊 <b>Total Users:</b> <code>{total_users}</code>", parse_mode=enums.ParseMode.HTML)


# ---------------- Admin Only: Broadcast ----------------
@Client.on_message(filters.private & filters.command("broadcast") & filters.user(DS_ADMINS))
async def broadcast_handler(client, message):

    if not message.reply_to_message:
        return await message.reply("⚠️ <b>Reply to a message to broadcast.</b>", parse_mode=enums.ParseMode.HTML)

    sent = 0
    failed = 0
    users = await db.get_all_users()

    status = await message.reply(f"📢 Broadcasting started...\nTotal users: {len(users)}")

    for user in users:
        try:
            await message.reply_to_message.copy(int(user["id"]))
            sent += 1
        except:
            failed += 1

        await asyncio.sleep(0.2)

        if (sent + failed) % 50 == 0:
            try:
                await status.edit_text(f"📢 Sending...\n✔️ Sent: {sent}\n❌ Failed: {failed}")
            except:
                pass

    await status.edit_text(f"📢 <b>Broadcast Completed</b>\n\n✔️ Sent: {sent}\n❌ Failed: {failed}", parse_mode=enums.ParseMode.HTML)



# ---------------- Start Command ----------------
@Client.on_message(filters.private & filters.command("start"))
async def start(client, message):

    if not await checkSub(client, message):
        return

    user_id = message.from_user.id

    if not await db.is_user_exist(user_id):
        await db.add_user(user_id, message.from_user.first_name or "User")
        try:
            await client.send_message(
                DS_LOG_CHANNEL, LOG_TEXT.format(user_id, message.from_user.mention)
            )
        except:
            pass

    buttons = [
        [InlineKeyboardButton("🎬 Get Random Video", callback_data="video")],
        [InlineKeyboardButton("🤖 Bot & Repo Info", callback_data="bot_info")]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)

    try:
        await message.reply_photo(
            photo=DS_PIC,
            caption="<b>🔞 Random Adult Video Bot\n\nClick Below 👇</b>",
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    except:
        await message.reply_text(
            "<b>🔞 Random Adult Video Bot\n\nClick Below 👇</b>",
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )


# ---------------- Send Random Video ----------------
async def send_random_video(client, chat_id, callback_message=None):

    file = await db.random_file("Video")
    if not file:
        if callback_message:
            return await callback_message.edit_text("❌ No videos available.")
        return

    try:
        sent = await client.copy_message(
            chat_id=chat_id,
            from_chat_id=DS_PORN_FILE_CHANNEL,
            message_id=file["msg_id"],
            caption="<b>🔥 Auto-deletes in 60 seconds.</b>",
            parse_mode=enums.ParseMode.HTML
        )

        # Buttons under video
        buttons = [
            [InlineKeyboardButton("➡ Next Video", callback_data="next")],
            [InlineKeyboardButton("🗑 Delete Now", callback_data=f"delete_{sent.id}")]
        ]

        await client.send_message(
            chat_id, "👇 Need another?", reply_markup=InlineKeyboardMarkup(buttons)
        )

        await asyncio.sleep(60)
        try:
            await sent.delete()
        except:
            pass

    except:
        if callback_message:
            await callback_message.edit_text("⚠ Failed to send video.")


# ---------------- Callback Handler ----------------
@Client.on_callback_query()
async def button_handler(client, callback_query):
    chat_id = callback_query.message.chat.id

    if not await checkSub(client, callback_query.message):
        return

    data = callback_query.data

    # Send video logic
    if data == "video" or data == "next":
        await callback_query.message.edit_text("🎬 Fetching...")
        await send_random_video(client, chat_id, callback_query.message)

    # Delete message logic
    elif data.startswith("delete_"):
        msg_id = int(data.split("_")[1])
        try:
            await client.delete_messages(chat_id, msg_id)
            await callback_query.answer("🗑 Deleted", show_alert=False)
        except:
            await callback_query.answer("⚠ Already deleted", show_alert=False)

    # Bot info section
    elif data == "bot_info":
        buttons = [[InlineKeyboardButton("📦 Buy Repo", url="https://t.me/Falcoxr")]]
        await callback_query.message.edit_text(
            ABOUT_TXT,
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=enums.ParseMode.HTML,
            disable_web_page_preview=True
        )


# ---------------- User Text Handler ----------------
@Client.on_message(filters.private & filters.text & ~filters.command("start"))
async def handle_text(client, message):

    if not await checkSub(client, message):
        return

    buttons = [
        [InlineKeyboardButton("🎬 Get Random Video", callback_data="video")],
        [InlineKeyboardButton("🤖 Bot & Repo Info", callback_data="bot_info")]
    ]

    await message.reply_text(
        "Use the buttons below 👇",
        reply_markup=InlineKeyboardMarkup(buttons)
    )