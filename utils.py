# Nexa  # Dont Remove Credit

import datetime
import pytz, random, string  
from pytz import timezone
from datetime import date 
from shortzy import Shortzy
from plugins.database import db   # Still used only for storing users if needed

# ======================================================================= #

TOKENS = {}
VERIFIED = {}

# ======================================================================= #
# TIME STRING → SECONDS
# ======================================================================= #

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
# ======================================================================= #

async def get_verify_shorted_link(link):
    shortzy = Shortzy(api_key=DS_API, base_site=DS_URL)
    return await shortzy.convert(link)

# ======================================================================= #
# TOKEN HANDLER
# ======================================================================= #

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
    VERIFIED[user.id] = str(date.today())

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
# LIMIT SYSTEM REMOVED
# ======================================================================= #
# No limit checking
# No usage tracking
# No reset job
# ======================================================================= #

async def check_and_increment(user_id, tag):
    """
    LIMIT REMOVED:
    Always return True → unlimited usage for all users
    """
    # Make sure the user exists in the DB (optional)
    user = await db.get_user(user_id)
    if not user:
        await db.add_user(user_id, f"User{user_id}")

    return True

# ======================================================================= #
# DAILY RESET REMOVED
# ======================================================================= #

async def reset_limits():
    """
    Function kept only for compatibility but does nothing now.
    """
    print("Daily limit reset skipped (limits removed).")

async def start_scheduler():
    """
    Scheduler removed. No daily reset needed.
    """
    print("[Scheduler] Disabled since limits are removed.")

# Nexa # Dont Remove Credit