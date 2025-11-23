# (c) ՏIᒪᗴᑎT ᘜᕼOՏT ⚡️ # Dont Remove Credit

import datetime
import motor.motor_asyncio
from pymongo import MongoClient
from config import DS_DB_URI, DS_DB_NAME

# Synchronous client (optional)
client = MongoClient(DS_DB_URI)
# Async client
mongo = motor.motor_asyncio.AsyncIOMotorClient(DS_DB_URI)
db_async = mongo[DS_DB_NAME]
db_sync = client[DS_DB_NAME]


class Database:
    def __init__(self):
        self.users = db_async["users"]
        self.files = db_async["files"]

    # ---------------- User Methods ----------------
    async def add_user(self, user_id: int, name: str):
        if not await self.is_user_exist(user_id):
            await self.users.insert_one({
                "id": user_id,
                "name": name,
                "date": None,
                "expiry_time": None
            })

    async def is_user_exist(self, user_id: int) -> bool:
        user = await self.users.find_one({'id': int(user_id)})
        return bool(user)

    async def get_user(self, user_id: int) -> dict:
        return await self.users.find_one({"id": int(user_id)})

    async def update_user(self, user_data: dict):
        await self.users.update_one({"id": user_data["id"]}, {"$set": user_data}, upsert=True)

    async def set_date(self, user_id: int, date):
        await self.users.update_one({"id": user_id}, {"$set": {"date": date}})

    async def get_date(self, user_id: int):
        user = await self.get_user(user_id)
        return user.get("date") if user else None

    async def total_users_count(self) -> int:
        return await self.users.count_documents({})

    async def get_all_users(self):
        return self.users.find({})

    async def delete_user(self, user_id: int):
        await self.users.delete_many({'id': int(user_id)})

    # ---------------- File Methods ----------------
    async def save_file(self, caption: str, file_id: str, msg_id: int, file_size: int, tag: str):
        """Save a file to the DB."""
        exists = await self.files.find_one({"msg_id": msg_id})
        if not exists:
            await self.files.insert_one({
                "caption": caption,
                "file_id": file_id,
                "msg_id": msg_id,
                "file_size": file_size,
                "tag": tag
            })

    async def delete_file(self, msg_id: int):
        """Delete a file by its message ID."""
        await self.files.delete_one({'msg_id': msg_id})

    async def random_file(self, tag: str):
        """Get a random file by tag."""
        cursor = self.files.aggregate([
            {"$match": {"tag": tag}},
            {"$sample": {"size": 1}}
        ])
        try:
            return await cursor.next()
        except StopAsyncIteration:
            return None


# Instantiate
db = Database()

# (c) ՏIᒪᗴᑎT ᘜᕼOՏT ⚡️ # Dont Remove Credit