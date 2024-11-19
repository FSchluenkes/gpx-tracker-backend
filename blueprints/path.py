import math
from flask import request, jsonify, Blueprint
from models import TrackPoint

path_bp = Blueprint("path", __name__)

@path_bp.post("")
def get_path():
  track_id:int = int(request.get_json().get('trackId'))

  if track_id > 0:
    trackpoints: list[TrackPoint] = TrackPoint.query.order_by(TrackPoint.timestamp).filter_by(track_id = track_id).all()

  
  if len(trackpoints) > 0:
    result = []
    for trackpoint in trackpoints:
      result.append({
        "id": trackpoint.punkt_id,
        "lat": trackpoint.lat,
        "lon": trackpoint.lon,
        "alt": trackpoint.ele,
        "timestamt": trackpoint.timestamp.isoformat()
      })
  
    return jsonify(result)