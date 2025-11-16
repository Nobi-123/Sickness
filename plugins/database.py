# (c) ՏIᒪᗴᑎT ᘜᕼOՏT ⚡️ # Dont Remove Credit

import datetime
import motor.motor_asyncio
from pymongo import MongoClient
from config import DS_DB_URI, DS_DB_NAME

client = MongoClient(DS_DB_URI)
mongo = motor.motor_asyncio.AsyncIOMotorClient(DS_DB_URI)
db_async = mongo[DS_DB_NAME]
db_sync = client[DS_DB_NAME]

# (c) ՏIᒪᗴᑎT ᘜᕼOՏT ⚡️ # Dont Remove Credit

class Database:

    def __init__(self):
        self.users = db_async["users"]
        self.files = db_async["files"]

    async def add_user(self, user_id, name):
        await self.users.insert_one({
            "id": user_id,
            "name": name,
            "plan": False,
            "date": None,
            "free_used": {"desi": 0, "videsi": 0},
            "expiry_time": None
        })

    async def is_user_exist(self, id):
        user = await self.users.find_one({'id':int(id)})
        return bool(user)
    
    async def get_user(self, user_id):
        return await self.users.find_one({"id": user_id})

    async def set_date(self, user_id, date):
        await self.users.update_one({"id": user_id}, {"$set": {"date": date}})

    async def set_free_used(self, user_id, used):
        await self.users.update_one({"id": user_id}, {"$set": {"free_used": used}})

    async def has_premium_access(self, user_id):
        user = await self.get_user(user_id)
        if not user:
            return False
        expiry = user.get("expiry_time")
        if expiry and datetime.datetime.utcnow() < expiry:
            return True
        await self.users.update_one({"id": user_id}, {"$set": {"plan": False, "expiry_time": None}})
        return False

    async def get_all_users(self):
        return self.users.find({})

    async def delete_user(self, user_id):
        await self.users.delete_many({'id': int(user_id)})

    async def delete_file(self, file_id):
        await self.files.delete_one({'_id': file_id})
    
    async def total_users_count(self):
        count = await self.users.count_documents({})
        return count

    async def save_file(self, caption, file_id, msg_id, file_size, tag):
        await self.files.insert_one({
            "caption": caption,
            "file_id": file_id,
            "msg_id": msg_id,
            "file_size": file_size,
            "tag": tag
        })

    async def random_file(self, tag):
        cursor = self.files.aggregate([
            {"$match": {"tag": tag}},
            {"$sample": {"size": 1}}
        ])
        try:
            return await cursor.next()
        except StopAsyncIteration:
            return None
    
    async def set_plan(self, id, plan):
        await self.users.update_one({'id': int(id)}, {'$set': {'plan': plan}})

    async def update_user(self, user_data):
        await self.users.update_one({"id": user_data["id"]}, {"$set": user_data}, upsert=True)

    async def remove_premium_access(self, user_id):
        return await self.users.update_one(
            {"id": user_id}, {"$set": {"expiry_time": None}}
        )

    async def set_pre_used(self, id, pre_used):
        await self.users.update_one({'id': int(id)}, {'$set': {'pre_used': pre_used}})

    async def get_plan(self, id):
        user = await self.users.find_one({'id': int(id)})
        return user.get('plan', False) if user else False
    
    async def get_date(self, id):
        user = await self.users.find_one({'id': int(id)})
        return user.get('date') if user else None
    
    async def get_free_used(self, id):
        user = await self.users.find_one({'id': int(id)})
        return user.get('free_used', {"desi": 0, "videsi": 0}) if user else {"desi": 0, "videsi": 0}

    async def get_pre_used(self, id):
        user = await self.users.find_one({'id': int(id)})
        return user.get('pre_used', 0) if user else 0
    
db = Database()

# (c) ՏIᒪᗴᑎT ᘜᕼOՏT ⚡️ # Dont Remove Credit
