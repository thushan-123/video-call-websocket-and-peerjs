import redis
from Loggers.log import err_log, app_log

# Connect to the redis database
redis_otp_client = redis.Redis(host="localhost", port=6379, db=0)
redis_call_client = redis.Redis(host="localhost", port=6379, db=1)

try:
    redis_otp_client.ping()
    redis_call_client.ping()
    app_log.info("redis database is connected successfully")
except Exception as e:
    err_log.error(f"redis connection -> {e}")
