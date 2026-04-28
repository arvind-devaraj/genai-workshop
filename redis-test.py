import redis

# Connect to the Redis server
# Adjust host and port as needed
client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

# Set a key-value pair in Redis
client.set('my_key', 'Hello, Redis!')

# Get the value of the key from Redis
value = client.get('my_key')

# Print the retrieved value
print(f"The value of 'my_key' is: {value}")
