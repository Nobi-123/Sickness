# Nexa  # Dont Remove Credit

import datetime
import pytz, random, string  
from pytz import timezone
from datetime import date 
from shortzy import Shortzy
from plugins.database import db
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# ======================================================================= #

TOKENS = {}
VERIFIED = {}

# Convert time string into seconds
async def get_seconds(time_string):
    def extract_value_and_unit(ts):
        value = ""
        index = 0
        while index < len(ts) and ts[index].isdigit():
            value += ts[index]
            index += 1
        unit = ts[index:].lstrip()
        return int(value) if value else 0, unit

    value, unit = extract_value_and_unit(time_string)

    return {
        "s": value,
        "min": value * 60,
        "hour": value * 3600,
        "day": value * 86400,
        "month": value * 86400 * 30,
        "year": value * 86400 * 365
    }.get(unit, 0)

# ======================================================================= #
# LINK SHORTENER

async def get_verify_shorted_link(link):
    shortzy = Shortzy(api_key=DS_API, base_site=DS_URL)
    return await shortzy.convert(link)

# ======================================================================= #
# TOKEN HANDLER

async def check_token(bot, userid, token):
    user = await bot.get_users(userid)
    user_tokens = TOKENS.get(user.id, {})
    return token in user_tokens and user_tokens[token] is False

async def get_token(bot, userid, link):
    user = await bot.get_users(userid)
    token = ''.join(random.choices(string.ascii_letters + string.digits, k=7))
    TOKENS[user.id] = {token: False}
    verify_url = f"{link}verify-{user.id}-{token}"
    return await get_verify_shorted_link(verify_url)

async def verify_user(bot, userid, token):
    user = await bot.get_users(userid)
    TOKENS[user.id] = {token: True}
    today = date.today()
    VERIFIED[user.id] = str(today)

async def check_verification(bot, userid):
    user = await bot.get_users(userid)
    today = date.today()

    if user.id not in VERIFIED:
        return False

    saved = VERIFIED[user.id]  # yyyy-mm-dd
    y, m, d = saved.split('-')
    old = date(int(y), int(m), int(d))

    return old >= today

# ======================================================================= #
# ( PREMIUM REMOVED ) DAILY LIMIT HANDLER
# ======================================================================= #

async def check_and_increment(user_id, tag):
    # Fetch user
    user = await db.get_user(user_id)
    if not user:
        await db.add_user(user_id, f"User{user_id}")
        user = await db.get_user(user_id)

    # Reset per-day data if new day
    today = str(datetime.datetime.now(pytz.timezone("Asia/Kolkata")).date())
    last_used_date = user.get("date")

    if last_used_date != today:
        await db.set_date(user_id, today)
        await db.set_free_used(user_id, {"desi": 0, "videsi": 0})

    used = user.get("free_used", {"desi": 0, "videsi": 0})

    # PREMIUM REMOVED → always use free limits
    if tag == "desi":
        limit = FREE_LIMIT_DESI
    else:
        limit = FREE_LIMIT_VIDESI

    # Check limit
    if used.get(tag, 0) >= limit:
        return False

    # Increment usage
    used[tag] = used.get(tag, 0) + 1
    await db.set_free_used(user_id, used)
    return True

# ======================================================================= #
# RESET LIMITS FOR ALL USERS DAILY
# ======================================================================= #

async def reset_limits():
    print("Resetting daily usage limits...")
    async for user in db.get_all_users():
        await db.set_free_used(user['id'], {"desi": 0, "videsi": 0})
        ist = timezone("Asia/Kolkata")
        today = str(datetime.datetime.now(ist).date())
        await db.set_date(user['id'], today)
    print("Limits reset.")

# ======================================================================= #
# SCHEDULER → RESET AT MIDNIGHT
# ======================================================================= #

async def start_scheduler():
    scheduler = AsyncIOScheduler(timezone="Asia/Kolkata")
    scheduler.add_job(reset_limits, "cron", hour=0, minute=0)
    scheduler.start()
    print("[Scheduler] Daily reset job scheduled at 00:00 IST.")

# Nexa # Dont Remove Credit