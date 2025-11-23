from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import DS_ADMINS
from plugins.fsub import SYSTEM_STATE


def panel_buttons():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(f"🛡 Auto Monitor: {'ON' if SYSTEM_STATE.get('monitor', False) else 'OFF'}", callback_data="toggle_monitor")],
        [InlineKeyboardButton(f"🤐 Auto Mute: {'ON' if SYSTEM_STATE.get('auto_mute', False) else 'OFF'}", callback_data="toggle_mute")],
        [InlineKeyboardButton(f"⚠ Auto Warning: {'ON' if SYSTEM_STATE.get('auto_warnings', False) else 'OFF'}", callback_data="toggle_warning")],
        [InlineKeyboardButton(f"🚫 Auto Ban: {'ON' if SYSTEM_STATE.get('auto_ban', False) else 'OFF'}", callback_data="toggle_ban")],
    ])


@Client.on_message(filters.command("panel") & filters.user(DS_ADMINS))
async def admin_panel(client, message):
    await message.reply("⚙ **Admin Control Panel**", reply_markup=panel_buttons())


@Client.on_callback_query(filters.user(DS_ADMINS))
async def panel_callback(client, callback):

    key = callback.data.replace("toggle_", "")

    # 🛠 SAFE UPDATE (no crash even if key not exists)
    SYSTEM_STATE[key] = not SYSTEM_STATE.get(key, False)

    await callback.message.edit("⚙ **Updated Settings**", reply_markup=panel_buttons())
    await callback.answer("Updated ✔")