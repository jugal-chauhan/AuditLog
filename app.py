from flask import Flask, request, jsonify
import os
import app_database

app = Flask(__name__)

@app.route('/events', methods=['POST'])
def record_event():
    try:
        event = request.json
        # Capture the source IP address and HTTP method
        source_ip = request.remote_addr
        http_method = request.method

        id, success = app_database.create_log(
            user_id=event['user_id'],
            event_type=event['event_type'],
            timestamp=event['timestamp'],
            src_service=event['src_service'],
            invariant_data=event['invariant_data'],
            app_data=event['app_data'],
            source_ip=source_ip,
            http_method=http_method
        )
        if success:
            return jsonify({"message": "Event recorded", "id": str(id)}), 201
        else:
            return jsonify({"message": "Error recording event"}), 500
    except Exception as e:
        app.logger.error(f"Failed to record event: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/events', methods=['GET'])
def get_events():
    user_id = request.args.get('user_id')
    # Default values for pagination
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))

    if user_id:
        events, total = app_database.read_logs_by_user_id(int(user_id), limit=per_page, skip=(page - 1) * per_page)
    else:
        events, total = app_database.read_logs(limit=per_page, skip=(page - 1) * per_page)

    return jsonify({
        'events': events,
        'total': total,
        'page': page,
        'per_page': per_page,
        'total_pages': (total + per_page - 1) // per_page  # Calculate total number of pages
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))  
    app.run(host='0.0.0.0', port=port, debug=True)
