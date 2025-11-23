# (c) Silent Ghost — Force Sub System V3 (Next Level)

import asyncio
from pyrogram import Client
from pyrogram.errors import UserNotParticipant, FloodWait
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import db

# REQUIRED CHANNELS
REQUIRED_CHANNELS = ["NexaCoders", "NexaMeetup"]

# SYSTEM CONFIG (Dynamic - Can be changed via Admin Panel)
SYSTEM_STATE = {
    "auto_ban": False,
    "auto_mute": True,
    "auto_warnings": True,
    "monitor": True
}

# TRACK WARNINGS + STATUS
warned_users = set()
muted_users = set()


# ---------------- JOIN BUTTONS ----------------
async def join_buttons(client, missing):
    btn = []
    for channel in missing:
        try:
            info = await client.get_chat(channel)
            url = info.invite_link or f"https://t.me/{info.username}"
            name = info.title
        except:
            url = f"https://t.me/{channel}"
            name = channel

        btn.append([InlineKeyboardButton(f"📢 Join {name}", url=url)])
    return InlineKeyboardMarkup(btn)


# ---------------- SUBSCRIPTION CHECK ----------------
async def check_subscription(client, user_id):
    missing = []

    for ch in REQUIRED_CHANNELS:
        try:
            await client.get_chat_member(ch, user_id)
        except UserNotParticipant:
            missing.append(ch)

    if not missing:
        return None

    return await join_buttons(client, missing)


# ---------------- ENTRY CHECK FOR ALL MESSAGES ----------------
async def checkSub(client, message):
    user = message.from_user.id
    name = message.from_user.first_name or "Unknown"

    # FIXED 👇 (name included)
    await db.add_user(user, name) if not await db.is_user_exist(user) else None

    markup = await check_subscription(client, user)

    if markup:
        if SYSTEM_STATE["auto_mute"]:
            muted_users.add(user)

        if SYSTEM_STATE["auto_warnings"] and user not in warned_users:
            warned_users.add(user)

            await message.reply(
                "**⚠ You must join required channel(s) to use this bot.**",
                reply_markup=markup
            )
        return False

    # user verified -> remove from warning/mute system
    warned_users.discard(user)
    muted_users.discard(user)
    return True


# ---------------- AUTO MONITOR SYSTEM ----------------
async def auto_monitor(client: Client):

    if not SYSTEM_STATE["monitor"]:
        print("⏸ Monitor Disabled")
        return

    print("🛡 Real Time Monitor V3 Activated...")

    while True:
        users = await db.get_all_users()

        for u in users:
            user_id = u["user_id"]
            markup = await check_subscription(client, user_id)

            if markup:  # left channel
                # Auto Ban
                if SYSTEM_STATE["auto_ban"]:
                    try:
                        await client.send_message(user_id, "❌ You left required channel — banned.")
                        await db.delete_user(user_id)
                        continue
                    except:
                        pass

                # Auto Warning
                if SYSTEM_STATE["auto_warnings"] and user_id not in warned_users:
                    warned_users.add(user_id)
                    try:
                        await client.send_message(
                            user_id,
                            "⚠ You left channel!\nJoin back to continue.",
                            reply_markup=markup
                        )
                    except:
                        pass

                muted_users.add(user_id)

            else:
                if user_id in muted_users or user_id in warned_users:
                    try:
                        await client.send_message(user_id, "✅ Thanks for rejoining! Access restored.")
                    except:
                        pass
                muted_users.discard(user_id)
                warned_users.discard(user_id)

        await asyncio.sleep(25)