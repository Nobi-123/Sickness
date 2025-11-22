# Nexa  # Don't Remove Credit

import re
from os import environ

# ─────────────────────────────────────────────
# BASIC SETTINGS
# ─────────────────────────────────────────────

id_pattern = re.compile(r'^-?\d+$')

DS_API_ID = int(environ.get("DS_API_ID", "21134445"))
DS_API_HASH = environ.get("DS_API_HASH", "231c18ea7273824491d6bf05425ab74e")

DS_BOT_TOKEN = environ.get("DS_BOT_TOKEN", "")
DS_BOT_USERNAME = environ.get("DS_BOT_USERNAME", "SicknessRoBot")  # bot username without @

DS_LOG_CHANNEL = int(environ.get("DS_LOG_CHANNEL", "-1003496332303"))
DS_STICKER = environ.get("DS_STICKER", "")
DS_PIC = environ.get("DS_PIC", "https://files.catbox.moe/6oh471.jpg")

# ─────────────────────────────────────────────
# DATABASE CHANNELS (STORE FILES)
# ─────────────────────────────────────────────

DS_DESI_FILE_CHANNEL = int(environ.get("DS_DESI_FILE_CHANNEL", "0"))
DS_VIDESI_FILE_CHANNEL = int(environ.get("DS_VIDESI_FILE_CHANNEL", "0"))

# ─────────────────────────────────────────────
# ADMINS
# ─────────────────────────────────────────────
try:
    DS_ADMINS = [int(x) for x in environ.get("DS_ADMINS", "8315954262").split()]
except ValueError:
    raise Exception("Admin list must contain only integers.")

# ─────────────────────────────────────────────
# DATABASE CONFIG
# ─────────────────────────────────────────────

DS_DB_URI = environ.get(
    "DS_DB_URI",
    "mongodb+srv://SickNessRoBot:Sickness@sickness.qxwkdjl.mongodb.net/?appName=Sickness"
)

DS_DB_NAME = environ.get("DS_DB_NAME", "SickNess")

# ─────────────────────────────────────────────
# FORCE SUBSCRIBE
# ─────────────────────────────────────────────

DS_AUTH_CHANNEL = int(environ.get("DS_AUTH_CHANNEL", "-1002890076223"))

# ─────────────────────────────────────────────
# VERIFICATION SYSTEM
# ─────────────────────────────────────────────

DS_API = environ.get("DS_API", "f454aa0a0473907a126cdc6763f5dc53361c1c7a")
DS_URL = environ.get("DS_URL", "shortxlinks.com")



# Nexa # Don't Remove Credit