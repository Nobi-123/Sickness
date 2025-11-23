from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import DS_ADMINS
from plugins.fsub import SYSTEM_STATE

def panel_buttons():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(f"🛡 Auto Monitor: {'ON' if SYSTEM_STATE['monitor'] else 'OFF'}", callback_data="toggle_monitor")],
        [InlineKeyboardButton(f"🤐 Auto Mute: {'ON' if SYSTEM_STATE['auto_mute'] else 'OFF'}", callback_data="toggle_mute")],
        [InlineKeyboardButton(f"⚠ Auto Warning: {'ON' if SYSTEM_STATE['auto_warnings'] else 'OFF'}", callback_data="toggle_warning")],
        [InlineKeyboardButton(f"🚫 Auto Ban: {'ON' if SYSTEM_STATE['auto_ban'] else 'OFF'}", callback_data="toggle_ban")],
    ])


@Client.on_message(filters.command("panel") & filters.user(DS_ADMINS))
async def admin_panel(client, message):
    await message.reply("⚙ **Admin Control Panel**", reply_markup=panel_buttons())


@Client.on_callback_query(filters.user(DS_ADMINS))
async def panel_callback(client, callback):

    key = callback.data.replace("toggle_", "")
    SYSTEM_STATE[key] = not SYSTEM_STATE[key]

    await callback.message.edit("⚙ **Updated Settings**", reply_markup=panel_buttons())
    await callback.answer("Updated ✔")