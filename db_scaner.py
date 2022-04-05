import redis
import os

redis_url = os.environ["REDIS_URL"]
redis_connection = redis.from_url(redis_url)
db_keys = redis_connection.keys(pattern="*")

print((len(db_keys)))

for key in db_keys:
    chat_id_value = redis_connection.get(key).decode("UTF-8")
    print(key.decode("UTF-8"), ": ", chat_id_value)

