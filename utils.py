# (c) ՏIᒪᗴᑎT ᘜᕼOՏT ⚡️ # Dont Remove Credit

import datetime
import pytz, random, string  
from pytz import timezone
from datetime import date 
from config import DS_API, DS_URL, FREE_LIMIT_DESI, FREE_LIMIT_VIDESI, PREMIUM_LIMIT_DESI, PREMIUM_LIMIT_VIDESI
from shortzy import Shortzy
from plugins.database import db
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# ======================================================================= #

TOKENS = {}
VERIFIED = {}

async def get_seconds(time_string):
    def extract_value_and_unit(ts):
        value = ""
        unit = ""
        index = 0
        while index < len(ts) and ts[index].isdigit():
            value += ts[index]
            index += 1
        unit = ts[index:].lstrip()
        if value:
            value = int(value)
        return value, unit
    value, unit = extract_value_and_unit(time_string)
    if unit == 's':
        return value
    elif unit == 'min':
        return value * 60
    elif unit == 'hour':
        return value * 3600
    elif unit == 'day':
        return value * 86400
    elif unit == 'month':
        return value * 86400 * 30
    elif unit == 'year':
        return value * 86400 * 365
    else:
        return 0

# (c) ՏIᒪᗴᑎT ᘜᕼOՏT ⚡️ # Dont Remove Credit

async def get_verify_shorted_link(link):
    shortzy = Shortzy(api_key=DS_API, base_site=DS_URL)
    link = await shortzy.convert(link)
    return link

async def check_token(bot, userid, token):
    user = await bot.get_users(userid)
    if user.id in TOKENS.keys():
        TKN = TOKENS[user.id]
        if token in TKN.keys():
            is_used = TKN[token]
            if is_used == True:
                return False
            else:
                return True
    else:
        return False

async def get_token(bot, userid, link):
    user = await bot.get_users(userid)
    token = ''.join(random.choices(string.ascii_letters + string.digits, k=7))
    TOKENS[user.id] = {token: False}
    link = f"{link}verify-{user.id}-{token}"
    shortened_verify_url = await get_verify_shorted_link(link)
    return str(shortened_verify_url)

async def verify_user(bot, userid, token):
    user = await bot.get_users(userid)
    TOKENS[user.id] = {token: True}
    tz = pytz.timezone('Asia/Kolkata')
    today = date.today()
    VERIFIED[user.id] = str(today)

async def check_verification(bot, userid):
    user = await bot.get_users(userid)
    tz = pytz.timezone('Asia/Kolkata')
    today = date.today()
    if user.id in VERIFIED.keys():
        EXP = VERIFIED[user.id]
        years, month, day = EXP.split('-')
        comp = date(int(years), int(month), int(day))
        if comp<today:
            return False
        else:
            return True
    else:
        return False

# ======================================================================= #
# (c) ՏIᒪᗴᑎT ᘜᕼOՏT ⚡️ # Dont Remove Credit

async def check_and_increment(user_id, tag):
    user = await db.get_user(user_id)
    if not user:
        await db.add_user(user_id, f"User{user_id}")
        user = await db.get_user(user_id)
        
    today = str(datetime.datetime.now(pytz.timezone("Asia/Kolkata")).date())
    last_used_date = user.get("date")
    is_premium = await db.has_premium_access(user_id)

    if last_used_date != today:
        await db.set_date(user_id, today)
        await db.set_free_used(user_id, {"desi": 0, "videsi": 0})

    used = user.get("free_used", {"desi": 0, "videsi": 0})

    if tag == "desi":
        limit = PREMIUM_LIMIT_DESI if is_premium else FREE_LIMIT_DESI
    else:
        limit = PREMIUM_LIMIT_VIDESI if is_premium else FREE_LIMIT_VIDESI

    if used.get(tag, 0) >= limit:
        return False

    used[tag] = used.get(tag, 0) + 1
    await db.set_free_used(user_id, used)
    return True

async def reset_limits():
    print("Resetting daily usage limits...")
    async for user in db.get_all_users():
        await db.set_free_used(user['id'], {"desi": 0, "videsi": 0})
        ist = timezone("Asia/Kolkata")
        today = str(datetime.datetime.now(ist).date())
        await db.set_date(user['id'], today)
    print("Limits reset.")

# (c) ՏIᒪᗴᑎT ᘜᕼOՏT ⚡️ # Dont Remove Credit

async def start_scheduler():
    scheduler = AsyncIOScheduler(timezone="Asia/Kolkata")  # Ensure IST timezone!
    scheduler.add_job(reset_limits, "cron", hour=0, minute=0)
    scheduler.start()
    print("[Scheduler] Daily reset job scheduled at 00:00 IST.")

# (c) ՏIᒪᗴᑎT ᘜᕼOՏT ⚡️ # Dont Remove Credit
