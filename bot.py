# (c) ՏIᒪᗴᑎT ᘜᕼOՏT ⚡️ # Dont Remove Credit

from pyrogram import Client
from config import DS_API_ID, DS_API_HASH, DS_BOT_TOKEN
from utils import start_scheduler

class Bot(Client):

    def __init__(self):
        super().__init__(
            "pom bot",
            api_id=DS_API_ID,
            api_hash=DS_API_HASH,
            bot_token=DS_BOT_TOKEN,
            plugins=dict(root="plugins"),
            workers=150,
            sleep_threshold=5
        )

      
    async def start(self):  
        await super().start()
        await start_scheduler()
        me = await self.get_me()
        self.username = '@' + me.username
        print(f'{self.username} Bot Started.')


    async def stop(self, *args):
        await super().stop()
        print('Bot Stopped Bye')

Bot().run()

# (c) ՏIᒪᗴᑎT ᘜᕼOՏT ⚡️ # Dont Remove Credit
