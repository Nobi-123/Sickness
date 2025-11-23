# (c) Silent Ghost — Force-Sub System V2 + Auto Protection

import asyncio
from pyrogram import Client
from pyrogram.errors import UserNotParticipant, FloodWait
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import db

# REQUIRED CHANNELS (edit usernames only)
REQUIRED_CHANNELS = ["NexaCoders", "Nexameetup"]

# AUTO BAN AFTER LEAVE?
AUTO_BAN = False  # True = Auto Ban | False = Only warns user


# -------- SAVE USER --------
async def save_user(user_id):
    if not await db.is_user_exist(user_id):
        await db.add_user(user_id)


# -------- GENERATE JOIN BUTTONS --------
async def generate_buttons(client, missing):
    btn = []
    for ch in missing:
        try:
            info = await client.get_chat(ch)
            link = info.invite_link or f"https://t.me/{info.username}"
            title = info.title
        except:
            link = f"https://t.me/{ch}"
            title = ch

        btn.append([InlineKeyboardButton(f"📢 Join {title}", url=link)])

    return InlineKeyboardMarkup(btn)


# -------- CHECK SUB --------
async def check_subscription(client, user_id):
    missing = []

    for ch in REQUIRED_CHANNELS:
        try:
            await client.get_chat_member(ch, user_id)
        except UserNotParticipant:
            missing.append(ch)
        except:
            pass

    if not missing:
        return None

    markup = await generate_buttons(client, missing)
    return markup


# -------- MAIN ENTRY CHECK (Start + Messages + Callbacks) --------
async def checkSub(client, message):
    user_id = message.from_user.id
    await save_user(user_id)

    markup = await check_subscription(client, user_id)

    if markup:
        await message.reply(
            "**⚠ You must join required channel(s) to continue.**",
            reply_markup=markup
        )
        return False
    return True


# -------- AUTO REAL-TIME MONITOR --------
async def auto_monitor(client: Client):

    print("🛡 Real-Time Protection Running...")

    notified = set()  # avoid repeating same warning

    while True:
        users = await db.get_all_users()

        for u in users:
            user_id = u["user_id"]

            markup = await check_subscription(client, user_id)

            if markup:  # user left channel
                if AUTO_BAN:
                    try:
                        await client.send_message(
                            user_id, "**❌ You left the channel — You are banned.**"
                        )
                        notified.discard(user_id)
                        await db.delete_user(user_id)
                        continue
                    except:
                        continue

                if user_id not in notified:
                    try:
                        await client.send_message(
                            user_id,
                            "**⚠ You left required channel(s)! Rejoin or bot will stop.**",
                            reply_markup=markup
                        )
                        notified.add(user_id)
                    except FloodWait as e:
                        await asyncio.sleep(e.value)
                    except:
                        pass

            else:
                if user_id in notified:
                    notified.remove(user_id)

        await asyncio.sleep(25)