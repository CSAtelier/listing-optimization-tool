import redis
from redis.cache import CacheConfig

r = redis.Redis(host='localhost', 
                    port=6379, 
                    decode_responses=True,
                    protocol=3,
                    )


r.set("city", "New York")
cityNameAttempt1 = r.get("city")    # Retrieved from Redis server and cached
cityNameAttempt2 = r.get("city")    # Retrieved from cache