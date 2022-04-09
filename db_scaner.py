from telegram_bot import redis_connection, db_keys

print((len(db_keys)))

for key in db_keys:
    chat_id_value = redis_connection.get(key).decode("UTF-8")
    print(key.decode("UTF-8"), ": ", chat_id_value)
