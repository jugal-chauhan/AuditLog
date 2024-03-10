import app_database
from datetime import datetime

# Dummy data
dummy_events = [
    {
        'user_id': 1,
        'event_type': 'account_created',
        'timestamp': datetime.utcnow().isoformat(),
        'src_service': 'user_service',
        'invariant_data': {'message': 'User account created', 'priority': 1, 'trace': 'trace_id_1'},
        'app_data': {'username': 'john_doe', 'email': 'john@example.com'}
    },
    {
        'user_id': 2,
        'event_type': 'payment_processed',
        'timestamp': datetime.utcnow().isoformat(),
        'src_service': 'payment_service',
        'invariant_data': {'message': 'Payment processed', 'priority': 2, 'trace': 'trace_id_2'},
        'app_data': {'amount': 100.0, 'currency': 'USD'}
    },
    {
        'user_id': 3,
        'event_type': 'customer_deactivated',
        'timestamp': datetime.utcnow().isoformat(),
        'src_service': 'user_service',
        'invariant_data': {'message': 'User account deleted', 'priority': 4, 'trace': 'trace_id_1'},
        'app_data': {'method': 'POST', 'authentication': 1.0}
    }
    # Add more dummy events as needed
]

# Insert dummy data into the database
for event in dummy_events:
    id, success = app_database.create_log(
        event_type=event['event_type'],
        timestamp=event['timestamp'],
        src_service=event['src_service'],
        invariant_data=event.get('invariant_data', {}),
        app_data=event.get('app_data', {}),
        **{k: v for k, v in event.items() if k not in ['event_type', 'timestamp', 'src_service', 'invariant_data', 'app_data']}
    )
    if success:
        print(f"Inserted event with ID: {id}")
    else:
        print("Failed to insert event")

