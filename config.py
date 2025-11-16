# (c) ՏIᒪᗴᑎT ᘜᕼOՏT ⚡️ # Dont Remove Credit

import re
from os import environ

id_pattern = re.compile(r'^.\d+$')

DS_API_ID = int(environ.get("DS_API_ID", "21134445"))
DS_API_HASH = environ.get("DS_API_HASH", "231c18ea7273824491d6bf05425ab74e")
DS_BOT_TOKEN = environ.get("DS_BOT_TOKEN", "7868730175:AAEfxMIVLDyDrs7liOjLLf72TMEOMb96Rck")
DS_BOT_USERNAME = environ.get("DS_BOT_USERNAME", "AdultxPornBot") # bot username without @
DS_LOG_CHANNEL = int(environ.get("DS_LOG_CHANNEL", "-1002287964531"))
DS_STICKER = environ.get("DS_STICKER", "")
DS_PIC = environ.get('DS_PIC', 'https://envs.sh/k-.jpg/HGBOTZ.jpg')

# Database Channel For Text Or Caption Store 
DS_DESI_FILE_CHANNEL = int(environ.get("DS_DESI_FILE_CHANNEL", "-1002812150081"))
DS_VIDESI_FILE_CHANNEL = int(environ.get("DS_VIDESI_FILE_CHANNEL", "-1002855994773"))
FREE_LIMIT_DESI = 5
FREE_LIMIT_VIDESI = 3
PREMIUM_LIMIT_DESI = 40
PREMIUM_LIMIT_VIDESI = 15

# Bot Admins
try:
    DS_ADMINS=[]
    for x in (environ.get("DS_ADMINS", "8156708830").split()):
        DS_ADMINS.append(int(x))
except ValueError:
      raise Exception("Your Admins list does not contain valid integers.")
    
# Mongodb Database 
DS_DB_URI = environ.get("DS_DB_URI", "mongodb+srv://dragonbytexmikey:vkFfYQyByjm4zCqS@cluster0.akw3kyd.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
DS_DB_NAME = environ.get("DS_DB_NAME", "susant-botz")

# Force subscribe channel 
DS_AUTH_CHANNEL = int(environ.get('DS_AUTH_CHANNEL', '-1002777869483')) # give your force subscribe channel id here else leave it blank

# Verification Variables
DS_API = environ.get("DS_API", "f454aa0a0473907a126cdc6763f5dc53361c1c7a") # shortlink api
DS_URL = environ.get("DS_URL", "shortxlinks.com") # shortlink domain without https://
DS_VERIFY_TUTORIAL = environ.get("DS_VERIFY_TUTORIAL", "https://t.me/howtoopenCineZonelinks/5") # how to open link 
DS_VERIFICATION = bool(environ.get("DS_VERIFICATION", False)) # set True Or False and make sure spelling is correct and first letter capital.

# (c) ՏIᒪᗴᑎT ᘜᕼOՏT ⚡️ # Dont Remove Credit
