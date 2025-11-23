# Nexa # Don't Remove Credit

from pyrogram import Client, filters
from config import DS_PORN_FILE_CHANNEL
from database import db


@Client.on_message(filters.video & filters.chat(DS_PORN_FILE_CHANNEL))
async def save_video(client, message):
    """Save incoming videos from the source channel to the database."""
    if not message.video:
        return

    try:
        await db.save_file(
            caption=message.caption or "",
            file_id=message.video.file_id,
            msg_id=message.id,
            file_size=message.video.file_size,
            tag="Video"
        )
        print(f"✅ Saved video {message.id} from channel {DS_PORN_FILE_CHANNEL}")
    except Exception as e:
        print(f"❌ Failed to save video {message.id}: {e}")