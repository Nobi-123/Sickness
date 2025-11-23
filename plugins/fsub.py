# Nexa — Advanced Auto System

from pyrogram import Client, filters
from pyrogram.errors import UserNotParticipant, FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import asyncio

# REQUIRED CHANNELS
REQUIRED_CHANNELS = ["NexaCoders", "Nexameetup"]


# ---------------- AUTO LEAVE SYSTEM ----------------
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

        await asyncio.sleep(3600)   # 1 hour repeat



# ---------------- FORCE SUB CHECK ----------------
async def force_check_loop(client: Client):
    print("🔄 Real-Time Forced Subscription Monitoring Started...")

    while True:
        async for dialog in client.get_dialogs():

            if dialog.chat.type != "private":
                continue

            user_id = dialog.chat.id

            # Check if user left required channels
            missing = await check_subscription(client, user_id)

            if missing:
                try:
                    await client.delete_messages(user_id, dialog.top_message_id)
                except:
                    pass

                await client.send_message(
                    user_id,
                    "**⚠ Alert! You left the required channels. Join again!**",
                    reply_markup=missing
                )

        await asyncio.sleep(25)   # CHECK EVERY 25 SECONDS



async def check_subscription(client: Client, user_id):

    missing_channels = []
    buttons = []

    for channel in REQUIRED_CHANNELS:
        try:
            await client.get_chat_member(channel, user_id)

        except UserNotParticipant:
            missing_channels.append(channel)

        except:
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

        buttons.append([InlineKeyboardButton(title, url=link)])

    buttons.append([InlineKeyboardButton("♻ Refresh", callback_data="refresh_fsub")])
    return InlineKeyboardMarkup(buttons)



# ---------------- BOT START HO GA TAB RUN ----------------
@Client.on_message(filters.private & filters.command("start"))
async def start_bot(client, message):
    asyncio.create_task(auto_leave_chats(client))
    asyncio.create_task(force_check_loop(client))

    await message.reply("🔥 Bot fully activated\n✔ Auto leave ON\n✔ Auto FSub Security Enabled\n✔ Real-time Check: 25s")