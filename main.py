from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from utils.validate import validate_date, validate_time

app = Flask(__name__)
CORS(app)

# Geçici toplantı listesi
meetings = [] #herhangi bir database kullanımından bahsedilmediği için en basit şekilde tasarladım
meeting_id_counter = 1

# Toplantı oluşturma (POST)
@app.route('/api/v1/meetings', methods=['POST'])
def create_meeting():
    global meeting_id_counter

    # Zorunlu alanların kontrolü
    if not all(key in request.json for key in ('topic', 'date', 'start_time', 'end_time')):
        return jsonify({'error': 'All fields except participants are required: topic, date, start_time, end_time.'}), 400

    # Date ve time verilerinin kontrolü
    meeting_date = validate_date(request.json['date'])
    start_time = validate_time(request.json['start_time'])
    end_time = validate_time(request.json['end_time'])

    if not meeting_date or not start_time or not end_time:
        return jsonify({'error': 'Invalid date or time format. Date should be YYYY-MM-DD, and time should be HH:MM.'}), 400

    # Şu andan önceki tarih ve saatlerin kontrolü
    now = datetime.now()
    if meeting_date < now.date() or (meeting_date == now.date() and start_time < now.time()):
        return jsonify({'error': 'Date and start time cannot be in the past.'}), 400

    # End time, start time'dan önce olamaz
    if end_time <= start_time:
        return jsonify({'error': 'End time must be after start time.'}), 400

    meeting = {
        'id': meeting_id_counter,
        'topic': request.json['topic'],
        'date': meeting_date.strftime('%Y-%m-%d'),
        'start_time': start_time.strftime('%H:%M'),
        'end_time': end_time.strftime('%H:%M'),
        'participants': request.json.get('participants', [])
    }
    meetings.append(meeting)
    meeting_id_counter += 1
    return jsonify(meeting), 201

# Toplantı listeleme (GET)
@app.route('/api/v1/meetings', methods=['GET'])
def list_meetings():
    return jsonify(meetings)

# Toplantı güncelleme (PUT)
@app.route('/api/v1/meetings/<int:id>', methods=['PUT'])
def update_meeting(id):
    meeting = next((m for m in meetings if m['id'] == id), None)
    if not meeting:
        return jsonify({'error': 'Meeting not found'}), 404

    # Date ve time verilerini kontrol et
    new_date = request.json.get('date')
    new_start_time = request.json.get('start_time')
    new_end_time = request.json.get('end_time')

    if new_date:
        meeting_date = validate_date(new_date)
        if not meeting_date:
            return jsonify({'error': 'Invalid date format. Date should be YYYY-MM-DD.'}), 400
        meeting['date'] = meeting_date.strftime('%Y-%m-%d')

    if new_start_time:
        start_time = validate_time(new_start_time)
        if not start_time:
            return jsonify({'error': 'Invalid time format. Time should be HH:MM.'}), 400
        meeting['start_time'] = start_time.strftime('%H:%M')

    if new_end_time:
        end_time = validate_time(new_end_time)
        if not end_time:
            return jsonify({'error': 'Invalid time format. Time should be HH:MM.'}), 400
        meeting['end_time'] = end_time.strftime('%H:%M')

    meeting['topic'] = request.json.get('topic', meeting['topic'])
    meeting['participants'] = request.json.get('participants', meeting['participants'])

    return jsonify(meeting)

# Toplantı silme (DELETE)
@app.route('/api/v1/meetings/<int:id>', methods=['DELETE'])
def delete_meeting(id):
    global meetings
    meetings = [m for m in meetings if m['id'] != id]
    return jsonify({'message': 'Meeting deleted successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)