from pymongo import MongoClient, DESCENDING
import os
import json

client = MongoClient(os.getenv('MONGO_URI', 'mongodb://localhost:27017/'))
db = client["activity_db"]
collection = db["logger"]

def create_log(user_id, event_type, timestamp, src_service, invariant_data, app_data, **kwargs):
    event = {
        'user_id': user_id,
        'event_type': event_type,
        'timestamp': timestamp,
        'src_service': src_service,
        'invariant_data': invariant_data,
        'app_data': app_data
    }
    event.update(kwargs)
    try:
        result = collection.insert_one(event)
        return result.inserted_id, True
    except Exception as e:
        print(f"Error inserting event: {e}")
        return None, False

def read_logs(limit=100, skip=0):
    try:
        cursor = collection.find(
            filter={},
            projection={'_id': 0},
            sort=[('timestamp', DESCENDING)],
            skip=skip,
            limit=limit
        )
        total = collection.count_documents({})
        return list(cursor), total
    except Exception as e:
        print(f"Error reading logs: {e}")
        return [], 0

def read_logs_by_user_id(user_id, limit=100, skip=0):
    try:
        query = {'user_id': user_id}
        cursor = collection.find(
            filter=query,
            projection={'_id': 0},
            sort=[('timestamp', DESCENDING)],
            skip=skip,
            limit=limit
        )
        total = collection.count_documents(query)
        return list(cursor), total
    except Exception as e:
        print(f"Error reading logs by user_id: {e}")
        return [], 0
