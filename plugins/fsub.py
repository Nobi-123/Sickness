# (c) Silent Ghost — Auto FSub + Auto Leave (No Refresh Button)

import asyncio
from pyrogram import Client, filters
from pyrogram.errors import UserNotParticipant, FloodWait
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# REQUIRED CHANNELS
REQUIRED_CHANNELS = ["NexaCoders", "Nexameetup"]


# ---------------- FORCE-SUB CHECK FUNCTION ----------------
async def checkSub(client, message):
    user_id = message.from_user.id
    markup = await check_subscription(client, user_id)

    if markup:
        try:
            await message.reply(
                "**⚠ You must join the required channel(s) to use the bot.**",
                reply_markup=markup
            )
        except:
            pass
        return False

    return True



async def check_subscription(client, user_id):
    missing_channels = []
    buttons = []

    for channel in REQUIRED_CHANNELS:
        try:
            await client.get_chat_member(channel, user_id)

        except UserNotParticipant:
            missing_channels.append(channel)

        except Exception:
            continue

    if not missing_channels:
        return None

    for ch in missing_channels:
        try:
            info = await client.get_chat(ch)
            link = info.invite_link or f"https://t.me/{info.username}"
            title = info.title

        except:
            link = f"https://t.me/{ch}"
            title = ch

        buttons.append([InlineKeyboardButton(f"📢 Join {title}", url=link)])

    return InlineKeyboardMarkup(buttons)



# ---------------- AUTO-LEAVE SYSTEM ----------------
async def auto_leave_chats(client: Client):
    print("🚀 Auto Leave Started...")

    while True:
        async for dialog in client.get_dialogs():

            if dialog.chat.type == "private":
                continue

            if dialog.chat.username and dialog.chat.username in REQUIRED_CHANNELS:
                continue

            try:
                await client.leave_chat(dialog.chat.id)
                print(f"🚪 Left: {dialog.chat.title or dialog.chat.id}")

            except FloodWait as e:
                await asyncio.sleep(e.value)

            except Exception as err:
                print(err)

        await asyncio.sleep(3600)   # check every 1 hour



# ---------------- REAL-TIME FORCED CHECK LOOP ----------------
async def force_check_loop(client: Client):
    print("🔄 Real-Time Forced Subscription Monitoring Started...")

    while True:
        async for dialog in client.get_dialogs():

            if dialog.chat.type != "private":
                continue

            markup = await check_subscription(client, dialog.chat.id)

            if markup:
                try:
                    await client.send_message(
                        dialog.chat.id,
                        "**⚠ You left the channel! Join back to continue using the bot.**",
                        reply_markup=markup
                    )
                except:
                    pass

        await asyncio.sleep(25)   # 🔥 Real-time check every 25s



# ---------------- ACTIVATE AUTO SYSTEM ON START ----------------
@Client.on_message(filters.private & filters.command("start"))
async def run_system(client, message):
    asyncio.create_task(auto_leave_chats(client))
    asyncio.create_task(force_check_loop(client))

    await message.reply(
        "🔥 System Activated!\n\n"
        "✔ Auto Leave ON\n"
        "✔ Force Subscription ON\n"
        "✔ Real-Time Protection (Every 25s)\n"
        "🚫 No Refresh Button — Fully Automatic"
    )