from flask import Blueprint, render_template, request, redirect, jsonify
from services.itinerary_service import ItineraryService

itineraries_bp = Blueprint('itineraries', __name__)

@itineraries_bp.route('/')
def home():
    itineraries = ItineraryService.get_all_itineraries()
    return render_template('index.html', itineraries=itineraries)

@itineraries_bp.route('/generate_itinerary', methods=['POST'])
def generate_itinerary():
    try:
        ItineraryService.create_itinerary(
            title=request.form.get('itinerary_title'),
            location=request.form.get('itinerary_location'),
            duration=int(request.form.get('itinerary_days', 3))
        )
        return redirect('/')
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@itineraries_bp.route('/itinerary/<int:itinerary_id>')
def view_itinerary(itinerary_id):
    itinerary = ItineraryService.get_itinerary_by_id(itinerary_id)
    if not itinerary:
        return redirect('/')
    days = itinerary.duration
    return render_template('itinerary.html', itinerary=itinerary, days=days)

@itineraries_bp.route('/update_itinerary/<int:itinerary_id>', methods=['POST'])
def update_itinerary(itinerary_id):
    day_updates = {}
    for key, value in request.form.items():
        if key.startswith('day_'):
            parts = key.split('_')
            if len(parts) >= 2:
                day_num = int(parts[1])
                field = '_'.join(parts[2:])
                day_key = "day_{}".format(day_num)
                if day_key not in day_updates:
                    day_updates[day_key] = {}
                day_updates[day_key][field] = value

    if ItineraryService.update_itinerary_days(itinerary_id, day_updates):
        return redirect('/itinerary/{}'.format(itinerary_id))
    return jsonify({'error': 'Itinerary not found'}), 404

@itineraries_bp.route('/delete_itinerary/<int:itinerary_id>', methods=['POST'])
def delete_itinerary(itinerary_id):
    if ItineraryService.delete_itinerary(itinerary_id):
        return redirect('/')
    return jsonify({'error': 'Itinerary not found'}), 404

# API endpoints for itineraries
@itineraries_bp.route('/api/itineraries', methods=['GET'])
def get_itineraries_api():
    itineraries = ItineraryService.get_all_itineraries()
    return jsonify([itinerary.to_dict() for itinerary in itineraries])

@itineraries_bp.route('/api/itineraries', methods=['POST'])
def create_itinerary_api():
    data = request.get_json()
    try:
        itinerary = ItineraryService.create_itinerary(
            title=data['title'],
            location=data['location'],
            duration=data['duration']
        )
        return jsonify(itinerary.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@itineraries_bp.route('/api/itineraries/<int:itinerary_id>', methods=['GET'])
def get_itinerary_api(itinerary_id):
    itinerary = ItineraryService.get_itinerary_by_id(itinerary_id)
    if itinerary:
        return jsonify(itinerary.to_dict())
    return jsonify({'error': 'Itinerary not found'}), 404

@itineraries_bp.route('/api/itineraries/<int:itinerary_id>', methods=['PUT'])
def update_itinerary_api(itinerary_id):
    data = request.get_json()
    itinerary = ItineraryService.update_itinerary_days(itinerary_id, data)
    if itinerary:
        return jsonify(itinerary.to_dict())
    return jsonify({'error': 'Itinerary not found'}), 404

@itineraries_bp.route('/api/itineraries/<int:itinerary_id>', methods=['DELETE'])
def delete_itinerary_api(itinerary_id):
    if ItineraryService.delete_itinerary(itinerary_id):
        return jsonify({'message': 'Itinerary deleted successfully'})
    return jsonify({'error': 'Itinerary not found'}), 404