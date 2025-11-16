# (C) ՏIᒪᗴᑎT ᘜᕼOՏT ⚡️ # Dont Remove Credit

from datetime import timedelta, datetime
import pytz, traceback, string, random 
from config import DS_ADMINS, DS_LOG_CHANNEL, DS_BOT_USERNAME
from plugins.database import db 
from pyrogram import Client, filters 
from utils import get_seconds
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

VALID_REDEEM_CODES = {}

def generate_code(length=8):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for _ in range(length))

@Client.on_message(filters.command("add_redeem") & filters.user(DS_ADMINS))
async def add_redeem_code(client, message):
    user_id = message.from_user.id
    if len(message.command) == 3:
        try:
            time = message.command[1]
            num_codes = int(message.command[2])
        except ValueError:
            await message.reply_text("Please provide a valid number of codes to generate.")
            return

        codes = []
        for _ in range(num_codes):
            code = generate_code()
            VALID_REDEEM_CODES[code] = time
            codes.append(code)

        codes_text = '\n'.join(f"➔ <code>/redeem {code}</code>" for code in codes)
        response_text = f"""
<b>Gɪғᴛᴄᴏᴅᴇ Gᴇɴᴇʀᴀᴛᴇᴅ ✅
Aᴍᴏᴜɴᴛ:</b> {num_codes}

{codes_text}
<b>Duration:</b> {time}

🔰<u>𝗥𝗲𝗱𝗲𝗲𝗺 𝗜𝗻𝘀𝘁𝗿𝘂𝗰𝘁𝗶𝗼𝗻</u>🔰
<b>𝙹𝚞𝚜𝚝 𝚌𝚕𝚒𝚌𝚔 𝚝𝚑𝚎 𝚊𝚋𝚘𝚟𝚎 𝚌𝚘𝚍𝚎 𝚝𝚘 𝚌𝚘𝚙𝚢 𝚊𝚗𝚍 𝚝𝚑𝚎𝚗 𝚜𝚎𝚗𝚍 𝚝𝚑𝚊𝚝 𝚌𝚘𝚍𝚎 𝚝𝚘 𝚝𝚑𝚎 𝙱𝚘𝚝, 𝚝𝚑𝚊𝚝'𝚜 𝚒𝚝 🔥</b>"""

        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Rᴇᴅᴇᴇᴍ Hᴇʀᴇ ✅️", url=f"http://t.me/{DS_BOT_USERNAME}")],
                [InlineKeyboardButton("Aɴʏ Qᴜᴇʀʏ ❔", url="https://t.me/xAkairo")]
            ]
        )

        await message.reply_text(response_text, reply_markup=keyboard)
    else:
        await message.reply_text("<b>♻ Usage:\n\n➩ <code>/add_redeem 1min 1</code>,\n➩ <code>/add_redeem 1hour 10</code>,\n➩ <code>/add_redeem 1day 5</code></b>")

# (C) ՏIᒪᗴᑎT ᘜᕼOՏT ⚡️ # Dont Remove Credit

@Client.on_message(filters.command("redeem"))
async def redeem_code(client, message):
    user_id = message.from_user.id
    if len(message.command) == 2:
        redeem_code = message.command[1]

        if redeem_code in VALID_REDEEM_CODES:
            try:
                time = VALID_REDEEM_CODES.pop(redeem_code)
                user = message.from_user.mention

                try:
                    seconds = await get_seconds(time)
                except Exception as e:
                    await message.reply_text("Invalid time format in redeem code.")
                    return

                if seconds > 0:
                    data = await db.get_user(user_id)
                    current_expiry = data.get("expiry_time") if data else None

                    now_aware = datetime.now(pytz.utc)

                    if current_expiry:
                        current_expiry = current_expiry.replace(tzinfo=pytz.utc)

                    if current_expiry and current_expiry > now_aware:
                        expiry_str_in_ist = current_expiry.astimezone(pytz.timezone("Asia/Kolkata")).strftime("%d-%m-%Y\n⏱️ Expiry Time: %I:%M:%S %p")
                        await message.reply_text(
                            f"🚫 You already have premium access, which expires on {expiry_str_in_ist}.\nYou cannot redeem another code until your current premium expires.",
                            disable_web_page_preview=True
                        )
                        return

                    expiry_time = now_aware + timedelta(seconds=seconds)
                    user_data = {"id": user_id, "expiry_time": expiry_time}
                    await db.update_user(user_data)

                    expiry_str_in_ist = expiry_time.astimezone(pytz.timezone("Asia/Kolkata")).strftime("%d-%m-%Y\n⏱️ Expiry Time: %I:%M:%S %p")

                    await message.reply_text(
                        f"Premium activated successfully!\n\nUser: {user}\nUser ID: {user_id}\nPremium Access: <code>{time}</code>\n\nExpiry Date: {expiry_str_in_ist}",
                        disable_web_page_preview=True
                    )

                    await client.send_message(
                        DS_LOG_CHANNEL,
                        text=f"#Redeem_Premium\n\n👤 User: {user}\n⚡ User ID: <code>{user_id}</code>\n⏰ Premium Access: <code>{time}</code>\n⌛️ Expiry Date: {expiry_str_in_ist}\n\n🔑 Redeem Code: <code>{redeem_code}</code>",
                        disable_web_page_preview=True
                    )
                else:
                    await message.reply_text("Invalid time format in redeem code.")
            except Exception as e:
                await message.reply_text(f"An error occurred while redeeming the code: {e}")
        else:
            await message.reply_text("Invalid Redeem Code or Expired.")
    else:
        await message.reply_text("Usage: /redeem <code>")

# (C) ՏIᒪᗴᑎT ᘜᕼOՏT ⚡️ # Dont Remove Credit

@Client.on_message(filters.command("premium") & filters.user(DS_ADMINS))
async def add_premium(client, message):
    try:
        _, user_id, time, *custom_message = message.text.split(" ", 3)
        custom_message = "**Tʜᴀɴᴋ ʏᴏᴜ ғᴏʀ ᴘᴜʀᴄʜᴀsɪɴɢ ᴛʜᴇ ᴘʀᴇᴍɪᴜᴍ ᴘᴀᴄᴋᴀɢᴇ. Nᴏᴡ, ʟᴇᴠᴇʀᴀɢᴇ ɪᴛs ғᴜʟʟ ᴘᴏᴛᴇɴᴛɪᴀʟ**" if not custom_message else " ".join(custom_message)
        time_zone = datetime.now(pytz.timezone("Asia/Kolkata"))
        current_time = time_zone.strftime("%d-%m-%Y : %I:%M:%S %p")
        user = await client.get_users(user_id)
        seconds = await get_seconds(time)
        if seconds > 0:
            expiry_time = datetime.now() + timedelta(seconds=seconds)
            user_data = {"id": user.id, "expiry_time": expiry_time}
            await db.update_user(user_data)
            await db.set_plan(user.id, plan=True)
            data = await db.get_user(user.id)
            expiry = data.get("expiry_time")
            expiry_str_in_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata")).strftime("%d-%m-%Y  :  %I:%M:%S %p")
            await message.reply_text(f"<b><u>Premium Access Added To The User</u>\n\n👤 User: {user.mention}\n\n🪪 User id: <code>{user_id}</code>\n\n⏰ Premium Access: {time}\n\n🎩 Joining : {current_time}\n\n⌛️ Expiry: {expiry_str_in_ist}.\n\n<code>{custom_message}</code></b>", disable_web_page_preview=True)
            await client.send_message(chat_id=user_id, text=f"<b>ʜɪɪ {user.mention},\n\n<u>ᴘʀᴇᴍɪᴜᴍ ᴀᴅᴅᴇᴅ ᴛᴏ ʏᴏᴜʀ ᴀᴄᴄᴏᴜɴᴛ</u> 😀\n\nᴘʀᴇᴍɪᴜᴍ ᴀᴄᴄᴇss - {time}\n\n⏰ ᴊᴏɪɴɪɴɢ - {current_time}\n\n⌛️ ᴇxᴘɪʀᴇ ɪɴ - {expiry_str_in_ist}\n\n<code>{custom_message}</code></b>", disable_web_page_preview=True)
            await client.send_message(DS_LOG_CHANNEL, text=f"#Added_Premium\n\n👤 User - {user.mention}\n\n🪪 User Id - <code>{user_id}</code>\n\n⏰ Premium Access - {time}\n\n🎩 Joining - {current_time}\n\n⌛️ Expiry - {expiry_str_in_ist}\n\n<code>{custom_message}</code>", disable_web_page_preview=True)
        else:
            await message.reply_text("<b>⚠️ Invalid Format, Use This Format - <code>/premium user_id 1day</code>\n\n<u>Time Format -</u>\n\n<code>1 day for day\n1 hour for hour\n1 min for minutes\n1 month for month\n1 year for year</code></b>")
    except ValueError:
        await message.reply_text("<b>⚠️ Invalid Format, Use This Format - <code>/premium user_id 1day</code>\n\n<u>Time Format -</u>\n\n<code>1 day for day\n1 hour for hour\n1 min for minutes\n1 month for month\n1 year for year</code></b>")
    except Exception as e:
        traceback.print_exc()
        await message.reply_text(f"error - {e}")

# (C) ՏIᒪᗴᑎT ᘜᕼOՏT ⚡️ # Dont Remove Credit

@Client.on_message(filters.command("remove_premium") & filters.user(DS_ADMINS))
async def remove_premium(client, message):
    if len(message.command) == 2:
        user_id = int(message.command[1])
        user = await client.get_users(user_id)
        if await db.remove_premium_access(user_id):
            await message.reply_text("<b>sᴜᴄᴄᴇssꜰᴜʟʟʏ ʀᴇᴍᴏᴠᴇᴅ ✅</b>")
            await db.set_plan(user_id, plan=False)
            await client.send_message(
                chat_id=user_id,
                text=f"<b>ʜᴇʏ {user.mention},\n\nʏᴏᴜʀ ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴄᴇss ʜᴀs ʙᴇᴇɴ ʀᴇᴍᴏᴠᴇᴅ 😕</b>"
            )
        else:
            await message.reply_text("<b>👀 ᴜɴᴀʙʟᴇ ᴛᴏ ʀᴇᴍᴏᴠᴇ, ᴀʀᴇ ʏᴏᴜ sᴜʀᴇ ɪᴛ ᴡᴀs ᴀ ᴘʀᴇᴍɪᴜᴍ ᴜsᴇʀ ɪᴅ??</b>")
    else:
        await message.reply_text("Usage: <code>/remove_premium user_id</code>")

# (C) ՏIᒪᗴᑎT ᘜᕼOՏT ⚡️ # Dont Remove Credit
