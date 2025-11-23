# Nexa # Dont Remove Credit

from pyrogram import Client, filters
from config import DS_PORN_FILE_CHANNEL
from plugins.database import db

@Client.on_message(filters.video & filters.chat(DS_PORN_FILE_CHANNEL))
async def save_Video(_, message):
    if message.video:
        await db.save_file(
            caption=message.caption or "",
            file_id=message.video.file_id,
            msg_id=message.id,
            file_size=message.video.file_size,
            tag="Video"
        )


# Nexa # Dont Remove Credit
