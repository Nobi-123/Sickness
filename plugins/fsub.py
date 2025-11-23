# (c) Silent Ghost — Auto FSub + Auto Leave (No Refresh Button)

import asyncio
from pyrogram import Client, filters
from pyrogram.errors import UserNotParticipant, FloodWait
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import db  # 👈 must store users


REQUIRED_CHANNELS = ["NexaCoders", "Nexameetup"]


# ---------------- SAVE USERS ----------------
async def save_user(user_id):
    users = await db.get_all_users()
    if user_id not in users:
        await db.add_user(user_id)


# ---------------- CHECK SUB ----------------
async def checkSub(client, message):
    user_id = message.from_user.id
    await save_user(user_id)

    markup = await check_subscription(client, user_id)

    if markup:
        await message.reply(
            "**⚠ Join the required channels to use the bot!**",
            reply_markup=markup
        )
        return False

    return True



async def check_subscription(client, user_id):
    missing = []
    buttons = []

    for ch in REQUIRED_CHANNELS:
        try:
            await client.get_chat_member(ch, user_id)
        except UserNotParticipant:
            missing.append(ch)
        except:
            pass

    if not missing:
        return None

    for ch in missing:
        try:
            info = await client.get_chat(ch)
            link = info.invite_link or f"https://t.me/{info.username}"
        except:
            link = f"https://t.me/{ch}"

        buttons.append([InlineKeyboardButton(f"📢 Join {ch}", url=link)])

    return InlineKeyboardMarkup(buttons)



# ---------------- REALTIME RECHECK ----------------
async def force_check_loop(client: Client):
    print("🔄 Real-time subscription verification active...")

    while True:
        users = await db.get_all_users()

        for user_id in users:
            markup = await check_subscription(client, user_id)

            if markup:
                try:
                    await client.send_message(
                        user_id,
                        "**⚠ You left the channel! Rejoin to continue using the bot!**",
                        reply_markup=markup
                    )
                except FloodWait as e:
                    await asyncio.sleep(e.value)
                except:
                    pass

        await asyncio.sleep(30)  # repeat



# ---------------- START HANDLER ----------------
@Client.on_message(filters.private & filters.command("start"))
async def start_handler(client, message):
    await save_user(message.from_user.id)

    if not hasattr(client, "rt_start"):
        asyncio.create_task(force_check_loop(client))
        client.rt_start = True

    await checkSub(client, message)

    await message.reply("✅ You are verified! Continue using the bot.")