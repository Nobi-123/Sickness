# (c) Silent Ghost — Auto FSub + Auto Leave (No Refresh Button)

import asyncio
from pyrogram import Client, filters
from pyrogram.errors import UserNotParticipant, FloodWait
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# REQUIRED CHANNELS (EDIT HERE)
REQUIRED_CHANNELS = ["NexaCoders", "Nexameetup"]


# ---------------- CHECK SUBSCRIPTION ----------------
async def checkSub(client, message):
    user_id = message.from_user.id
    markup = await check_subscription(client, user_id)

    if markup:
        await message.reply(
            "**⚠ You must join the required channel(s) to use the bot.**",
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
            title = info.title
        except:
            link = f"https://t.me/{ch}"
            title = ch

        buttons.append([InlineKeyboardButton(f"📢 Join {title}", url=link)])

    return InlineKeyboardMarkup(buttons)



# ---------------- AUTO LEAVE NON REQUIRED GROUPS ----------------
async def auto_leave_chats(client: Client):
    print("🚀 Auto Leave Started...")

    while True:
        async for dialog in client.iter_dialogs():
            chat = dialog.chat

            if chat.type == "private":
                continue

            if chat.username and chat.username in REQUIRED_CHANNELS:
                continue

            try:
                await client.leave_chat(chat.id)
                print(f"🚪 LEFT: {chat.title or chat.id}")
            except FloodWait as e:
                await asyncio.sleep(e.value)
            except Exception as e:
                print(e)

        await asyncio.sleep(3600)  # Check every hour



# ---------------- REAL-TIME MONITORING ----------------
async def force_check_loop(client: Client):
    print("🔄 Real-time subscription monitoring running...")

    while True:
        async for dialog in client.iter_dialogs():

            if dialog.chat.type != "private":   # only DM users
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

        await asyncio.sleep(25)  # Fast check



# ---------------- RUN ON START ----------------
@Client.on_message(filters.private & filters.command("start"))
async def start_handler(client, message):

    if not hasattr(client, "system_started"):
        asyncio.create_task(auto_leave_chats(client))
        asyncio.create_task(force_check_loop(client))
        client.system_started = True

    await checkSub(client, message)