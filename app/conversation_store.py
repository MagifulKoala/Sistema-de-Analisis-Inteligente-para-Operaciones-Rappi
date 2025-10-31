import redis
import json
from typing import List

redis_client = redis.Redis(host='redis', port=6379, db=2, decode_responses=True)

def get_conversation_history(user_id: str, max_messages: int = 20) -> List[str]:
    """Retrieve conversation history for a user"""
    key = f"conversation:{user_id}"
    history = redis_client.lrange(key, 0, max_messages - 1)
    return [json.loads(msg) for msg in history]

def add_to_conversation(user_id: str, message: str, response: str, ttl: int = 86400):
    """Add a message and response to conversation history"""
    key = f"conversation:{user_id}"
    
    conversation_entry = json.dumps({
        "message": message,
        "response": response
    })
    
    redis_client.lpush(key, conversation_entry)
    
    redis_client.ltrim(key, 0, 49)
    
    redis_client.expire(key, ttl)

def clear_conversation(user_id: str):
    key = f"conversation:{user_id}"
    redis_client.delete(key)