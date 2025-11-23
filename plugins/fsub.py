# Nexa — Auto FSub + Auto Warn/Mute/Ban System (MongoDB Compatible)

from pyrogram import Client, filters
from pyrogram.errors import UserNotParticipant, FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import asyncio
from config import OWNER_ID
from database import db


REQUIRED_CHANNELS = ["NexaCoders", "Nexameetup"]


# ---------------- CHECK SUB ----------------

async def check_subscription(client, user_id):
    missing = []
    for ch in REQUIRED_CHANNELS:
        try:
            await client.get_chat_member(ch, user_id)
        except UserNotParticipant:
            missing.append(ch)
        except:
            pass

    return missing if missing else None


# ---------------- AUTO PUNISHMENT LOGIC ----------------

async def punish_user(client, user_id):

    user = await db.get_user(user_id)

    if not user:
        await db.update_user({"id": user_id, "status": "normal"})
        user = await db.get_user(user_id)

    status = user.get("status", "normal")

    if status == "normal":
        await db.update_user({"id": user_id, "status": "warned"})
        return "warn"

    elif status == "warned":
        await db.update_user({"id": user_id, "status": "muted"})
        return "mute"

    elif status == "muted":
        await db.update_user({"id": user_id, "status": "banned"})
        return "ban"

    return status


# ---------------- AUTO CHECK LOOP ----------------

async def force_check_loop(client):
    await asyncio.sleep(5)

    while True:
        async for dialog in client.get_dialogs():

            if dialog.chat.type != "private":
                continue

            user_id = dialog.chat.id
            missing = await check_subscription(client, user_id)

            if missing:
                action = await punish_user(client, user_id)

                buttons = [
                    [InlineKeyboardButton(f"Join {ch}", url=f"https://t.me/{ch}")]
                    for ch in missing
                ]

                msg = {
                    "warn": "⚠ **Warning!** You left required channels.\nJoin again.",
                    "mute": "🔇 You are now **Muted** until you rejoin.",
                    "ban": "🚫 You are **Banned permanently.**"
                }.get(action, "")

                try:
                    await client.send_message(
                        user_id,
                        msg,
                        reply_markup=InlineKeyboardMarkup(buttons)
                    )
                except:
                    pass

        await asyncio.sleep(25)


# ---------------- AUTO LEAVE JUNK GROUPS ----------------

async def auto_leave_chats(client):
    await asyncio.sleep(10)
    while True:
        async for dialog in client.get_dialogs():

            if dialog.chat.type == "private":
                continue

            if dialog.chat.username in REQUIRED_CHANNELS:
                continue

            try:
                await client.leave_chat(dialog.chat.id)
            except FloodWait as e:
                await asyncio.sleep(e.value)

        await asyncio.sleep(3600)


# ---------------- OWNER COMMANDS ----------------

@Client.on_message(filters.command("unban") & filters.user(OWNER_ID))
async def unban_user(_, message):
    if len(message.command) < 2:
        return await message.reply("Usage:\n`/unban user_id`")

    user_id = int(message.command[1])
    await db.update_user({"id": user_id, "status": "normal"})

    await message.reply(f"✅ User `{user_id}` **Unbanned** Successfully!")


@Client.on_message(filters.command("unmute") & filters.user(OWNER_ID))
async def unmute_user(_, message):
    if len(message.command) < 2:
        return await message.reply("Usage:\n`/unmute user_id`")

    user_id = int(message.command[1])
    await db.update_user({"id": user_id, "status": "normal"})

    await message.reply(f"🔊 User `{user_id}` **Unmuted** Successfully!")


# backward support
checkSub = check_subscription