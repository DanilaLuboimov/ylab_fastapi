import json

from .redis_connection import redis


async def create_new_cache(dictionary: dict | None, name: str | None = None) -> None:
    if not dictionary:
        return
    if not name:
        name = str(dictionary["id"])
    dictionary["id"] = str(dictionary["id"])
    data = json.dumps(dictionary)
    await redis.set(name, data)


async def get_cache_response(name: str) -> dict | None:
    data = await redis.get(name)
    if data:
        print("Данные из кэша")
        return json.loads(data)
    print("НЕ из кэша данные")
    return None


async def delete_cache(name: str) -> None:
    await redis.delete(name)
