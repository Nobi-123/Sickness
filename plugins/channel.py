# (c) ՏIᒪᗴᑎT ᘜᕼOՏT ⚡️ # Dont Remove Credit

from pyrogram import Client, filters
from config import DS_DESI_FILE_CHANNEL, DS_VIDESI_FILE_CHANNEL
from plugins.database import db

@Client.on_message(filters.video & filters.chat(DS_DESI_FILE_CHANNEL))
async def save_desi(_, message):
    if message.video:
        await db.save_file(
            caption=message.caption or "",
            file_id=message.video.file_id,
            msg_id=message.id,
            file_size=message.video.file_size,
            tag="desi"
        )

@Client.on_message(filters.video & filters.chat(DS_VIDESI_FILE_CHANNEL))
async def save_videsi(_, message):
    if message.video:
        await db.save_file(
            caption=message.caption or "",
            file_id=message.video.file_id,
            msg_id=message.id,
            file_size=message.video.file_size,
            tag="videsi"
        )

# (c) ՏIᒪᗴᑎT ᘜᕼOՏT ⚡️ # Dont Remove Credit
