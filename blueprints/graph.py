import math
from flask import request, jsonify, Blueprint
from models import TrackPoint

graph_bp = Blueprint("graph", __name__)

def getGraphData(trackpoints: list[TrackPoint]) -> list[dict]:

  altitude: list[float] = []
  for i in range(1, len(trackpoints)):
    duration = trackpoints[i].timestamp - trackpoints[i-1].timestamp 
    if duration.seconds > 0:
      km = haversine(trackpoints[i-1].lat, trackpoints[i-1].lon, trackpoints[i].lat, trackpoints[i].lon)
      kmh = km / (duration.seconds / 3600)

      altitude.append({
        "timestamp": trackpoints[i].timestamp.isoformat(), 
        "altitude": round(trackpoints[i].ele, 2),
        "speed": round(kmh, 2),
      }) 

  return altitude

def haversine(lat1, lon1, lat2, lon2) -> float:
    R = 6371.0

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c

@graph_bp.post("")
def get_stats():
  track_id:int = int(request.get_json().get('trackId'))

  if track_id > 0:
    trackpoints: list[TrackPoint] = TrackPoint.query.order_by(TrackPoint.timestamp).filter_by(track_id = track_id).all()

  
  if len(trackpoints) > 0:
    data: list[float] = getGraphData(trackpoints)

    return jsonify({
      "data": data,
      "count": len(trackpoints),
    })
  