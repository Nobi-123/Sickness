# Nexa — Advanced Verification System | Permanent Storage | Owner Control

import datetime
import random, string
from shortzy import Shortzy
from database import db
from config import DS_API, DS_URL

TOKENS = {}

# ================== TOKEN GENERATOR ================== #

async def generate_token():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=7))


async def create_verify_link(user_id):
    token = await generate_token()
    TOKENS[user_id] = token

    raw_url = f"https://t.me/{DS_URL}?start=verify-{user_id}-{token}"
    short_link = await Shortzy(api_key=DS_API, base_site=DS_URL).convert(raw_url)

    return short_link


# ================== VERIFY CHECK ================== #

async def verify_user(user_id, token):

    # Check token match
    if TOKENS.get(user_id) != token:
        return False

    # Store verification in DB
    expiry = (datetime.datetime.utcnow() + datetime.timedelta(days=1)).timestamp()
    await db.update_user({"id": user_id, "verified_until": expiry})

    del TOKENS[user_id]
    return True


async def is_verified(user_id):
    user = await db.get_user(user_id)

    if not user:
        return False

    expiry = user.get("verified_until")

    if not expiry:
        return False

    if expiry < datetime.datetime.utcnow().timestamp():
        # Expired → remove verification
        await db.update_user({"id": user_id, "verified_until": None})
        return False

    return True


# ================== OWNER COMMANDS ================== #

async def admin_set_verify(user_id, days):
    expiry = (datetime.datetime.utcnow() + datetime.timedelta(days=days)).timestamp()
    await db.update_user({"id": user_id, "verified_until": expiry})
    return True


async def admin_remove_verify(user_id):
    await db.update_user({"id": user_id, "verified_until": None})
    return True