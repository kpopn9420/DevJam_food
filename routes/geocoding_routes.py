from flask import Blueprint, request, jsonify
from geo_service import GeoService

geocoding_bp = Blueprint('geocoding', __name__)

@geocoding_bp.route('/api/geocoding/address-to-coordinates', methods=['POST'])
def address_to_coordinates():
    """地址轉經緯度"""
    try:
        data = request.get_json()
        if not data or 'address' not in data:
            return jsonify({'status': 'error', 'message': '缺少地址參數'}), 400
        
        address = data['address'].strip()
        if not address:
            return jsonify({'status': 'error', 'message': '地址不能為空'}), 400
        
        result = GeoService.address_to_coordinates(address)
        
        if result:
            return jsonify({
                'status': 'success',
                'data': {
                    'original_address': address,
                    'coordinates': {'lat': result['lat'], 'lng': result['lng']},
                    'formatted_address': result['formatted_address'],
                    'service_used': result['service']
                }
            })
        else:
            return jsonify({
                'status': 'error',
                'message': '無法找到該地址的座標'
            }), 404
            
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@geocoding_bp.route('/api/geocoding/coordinates-to-address', methods=['POST'])
def coordinates_to_address():
    """經緯度轉地址"""
    try:
        data = request.get_json()
        if not data or 'lat' not in data or 'lng' not in data:
            return jsonify({'status': 'error', 'message': '缺少座標參數'}), 400
        
        lat, lng = float(data['lat']), float(data['lng'])
        
        if not GeoService.validate_coordinates(lat, lng):
            return jsonify({'status': 'error', 'message': '座標超出台灣範圍'}), 400
        
        result = GeoService.coordinates_to_address(lat, lng)
        
        if result:
            return jsonify({
                'status': 'success',
                'data': {
                    'coordinates': {'lat': lat, 'lng': lng},
                    'address': result['address'],
                    'details': result['details']
                }
            })
        else:
            return jsonify({'status': 'error', 'message': '無法找到該座標的地址'}), 404
            
    except ValueError:
        return jsonify({'status': 'error', 'message': '座標格式錯誤'}), 400
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@geocoding_bp.route('/api/geocoding/batch-geocode', methods=['POST'])
def batch_geocode():
    """批量地址轉換"""
    try:
        data = request.get_json()
        if not data or 'addresses' not in data:
            return jsonify({'status': 'error', 'message': '缺少地址列表'}), 400
        
        addresses = data['addresses']
        if not isinstance(addresses, list) or len(addresses) > 10:
            return jsonify({'status': 'error', 'message': '地址列表格式錯誤或超過10個'}), 400
        
        results = GeoService.batch_geocode(addresses)
        success_count = sum(1 for r in results if r['status'] == 'success')
        
        return jsonify({
            'status': 'success',
            'data': {
                'total': len(addresses),
                'success_count': success_count,
                'results': results
            }
        })
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# CORS 處理
@geocoding_bp.route('/api/geocoding/<path:endpoint>', methods=['OPTIONS'])
def handle_options(endpoint):
    response = jsonify()
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'POST,OPTIONS')
    return response