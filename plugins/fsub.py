# Nexa — Do Not Remove Credit

from pyrogram.errors import UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import DS_FSUB_CHANNELS, DS_BOT_USERNAME


async def checkSub(client, message):
    user_id = message.from_user.id
    not_joined = []

    # Check membership for ALL required channels
    for channel in DS_FSUB_CHANNELS:
        try:
            member = await client.get_chat_member(channel, user_id)

            # If not proper member
            if member.status not in ["member", "administrator", "creator"]:
                not_joined.append(channel)

        except UserNotParticipant:
            not_joined.append(channel)

        except Exception:
            # If channel lookup fails → skip but don't break bot
            continue

    # If user is missing channels
    if not_joined:
        buttons = []

        # Create one button per channel
        for ch in not_joined:
            try:
                chat = await client.get_chat(ch)
                if chat.username:
                    buttons.append(
                        [InlineKeyboardButton(f"Join {chat.title}", url=f"https://t.me/{chat.username}")]
                    )
                else:
                    # private channels without username
                    buttons.append(
                        [InlineKeyboardButton(f"Join {chat.title}", url=chat.invite_link)]
                    )
            except:
                continue

        # Retry button
        buttons.append([
            InlineKeyboardButton(
                "♻️ Try Again",
                url=f"https://t.me/{DS_BOT_USERNAME}?start=start"
            )
        ])

        await message.reply_text(
            "<b>You must join all channels below to continue:</b>",
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode="html"
        )
        return False

    return True