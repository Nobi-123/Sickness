# (c) Silent Ghost — Multi Channel Forced Subscription

from pyrogram import Client
from pyrogram.errors import UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# ===========================
# ADD MULTIPLE CHANNELS HERE
# ===========================
REQUIRED_CHANNELS = [
    "NexaCoders",   # Example: "GhostUpdates"
    "Nexameetup",  
]


async def checkSub(client: Client, message):
    user_id = message.from_user.id
    missing_channels = []

    # Check each required channel
    for channel in REQUIRED_CHANNELS:
        try:
            await client.get_chat_member(channel, user_id)

        except UserNotParticipant:
            # User not joined, mark as missing
            missing_channels.append(channel)

        except Exception:
            # If bot is not admin / channel invalid
            continue

    # ===========================
    # User has NOT joined all channels
    # ===========================
    if missing_channels:
        buttons = []

        # Create button for each missing channel
        for ch in missing_channels:
            try:
                info = await client.get_chat(ch)
                title = info.title
                link = info.invite_link or f"https://t.me/{ch.replace('@','')}"
            except:
                title = ch
                link = f"https://t.me/{ch.replace('@','')}"

            buttons.append([InlineKeyboardButton(title, url=link)])

        buttons.append([InlineKeyboardButton("♻ Refresh", callback_data="refresh_fsub")])

        await message.reply_text(
            "**🚫 You must join all required channels to use this bot!**\n\n"
            "👇 Join the channels below and press **Refresh**:",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
        return False

    # ===========================
    # User is fully subscribed
    # ===========================
    return True