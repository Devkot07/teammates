from decouple import config


DATABASE_URL = f"mysql+aiomysql://{config('DB_USER')}:{config('DB_PASSWORD')}@{config('DB_HOST')}:{config('DB_PORT')}/{config('DB_NAME')}"

redis_config = {
    "url": f"redis://{config('REDIS_HOST')}",
    "decode_responses": True,
    "encoding": "utf-8"
}

auth_service_url = config("AUTH_SERVICE_URL")
