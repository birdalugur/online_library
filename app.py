import json
from typing import Union, List

import aioredis
from fastapi import FastAPI, Query
from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient

from config import mdb_connection_string, redis_url
from bson.objectid import ObjectId
from models import Book, User

app = FastAPI()
redis = aioredis.from_url(redis_url, decode_responses=True)
client = MongoClient(mdb_connection_string)
client = AsyncIOMotorClient(mdb_connection_string)

library = client.library
book_docs = library.book_docs
user_docs = library.users


async def get_cache(_id: str):
    """
    Get data from redis cache."""

    data = await redis.get("book:" + _id)
    if data:
        return json.loads(data)


async def set_cache(_id, data):
    """
    Set data to redis cache."""

    await redis.set("book:" + _id, json.dumps(data.dict()), ex=60 + 60)


async def get_book_by_id(_id: str):
    isCached = True
    data = await get_cache(_id)

    if not data:
        isCached = False
        data = await book_docs.find_one(ObjectId(_id))
        data = Book(**data)

        await set_cache(_id, data)

    return {"isCached": isCached, "data": data}


async def mset_cache(data: List[dict]):
    key_value_data = {}
    for doc in data:
        key_value_data.update({'cache:' + doc['id']: json.dumps(doc)})
    await redis.mset(key_value_data)


async def mget_cache():
    """
    Returns all the books in the cache."""

    _keys = await redis.keys('cache:*')
    # TODO: Use redis.mget()
    data = []
    for key in _keys:
        doc = await redis.get(key)
        data.append(json.loads(doc))

    return data


async def get_all_books():
    # TODO: Bad code. Edit the code!
    isCached = True

    if await redis.get("cachecontrol"):
        data = await mget_cache()
        return {"isCached": isCached, "data": data}
    data = None
    if not data:
        isCached = False
        length = await book_docs.count_documents(filter={})
        all_books = await book_docs.find().to_list(length)
        book_tables = [Book(**doc).dict() for doc in all_books]

        await redis.flushall()
        await mset_cache(book_tables)
        await redis.set("cachecontrol", 1, ex=20)

    return {"isCached": isCached, "data": book_tables}


@app.get("/books/")
async def get_books(_id: Union[str, None] = Query(default=None, alias="id")):
    if _id:
        res = await get_book_by_id(_id)
    else:
        res = await get_all_books()
    return res


@app.post('/user/')
async def create_user(user: User):
    result = await user_docs.insert_one(user.dict())
    return str(result.inserted_id)
