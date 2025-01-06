import math
from flask import request, jsonify, Blueprint
from models import TrackPoint

stats_bp = Blueprint("stats", __name__)

def haversine(lat1, lon1, lat2, lon2) -> float:
    R = 6371.0

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c

def getTrackLength(trackpoints: list[TrackPoint]) -> float:
  distance:float = 0

  for i in range(1, len(trackpoints)):
        lat1, lon1 = trackpoints[i-1].lat, trackpoints[i-1].lon
        lat2, lon2 = trackpoints[i].lat, trackpoints[i].lon
        distance += haversine(lat1, lon1, lat2, lon2)

  return distance

def getAltitude(trackpoints: list[TrackPoint]) -> tuple[float, float]:
  gain: float = 0
  loss: float = 0

  for i in range(1, len(trackpoints)):
    ele1: float = trackpoints[i-1].ele
    ele2: float = trackpoints[i].ele


    if ele1 < ele2:
      gain += ele2 - ele1
    else:
       loss += ele1 - ele2

  return gain, loss

def getMaxSpeed(trackpoints: list[TrackPoint]) -> float:
  max_kmh: float = 0
  for i in range(1, len(trackpoints)):
    km = haversine(trackpoints[i-1].lat, trackpoints[i-1].lon, trackpoints[i].lat, trackpoints[i].lon)
    duration = trackpoints[i].timestamp - trackpoints[i-1].timestamp   
    if duration.seconds == 0:
      kmh = 0
    else:
      kmh = (km * 3600 ) / duration.seconds

    max_kmh = max(max_kmh, kmh)

  return max_kmh

@stats_bp.post("")
def get_stats():
  track_id:int = int(request.get_json().get('trackId'))

  if track_id > 0:
    trackpoints: list[TrackPoint] = TrackPoint.query.order_by(TrackPoint.timestamp).filter_by(track_id = track_id).all()

  
  if len(trackpoints) > 0:
    distance = getTrackLength(trackpoints)
    gain, loss = getAltitude(trackpoints)
    duration = trackpoints[-1].timestamp - trackpoints[0].timestamp
    avg = (distance * 3600) / duration.seconds
    max_kmh = getMaxSpeed(trackpoints)
  

    return jsonify({
      "distance": {
        "value": round(distance, 2),
        "unit": "km",
      },
      "elevation": {
        "gain": {
          "value": int(round(gain, 0)),
          "unit": "m",         
            },
        "loss": {
          "value": int(round(loss)),
          "unit": 'm'
        },
      },
      "speed": {
        "avg": {
          "value": round(avg, 2),
          "unit": "km/h",
        },
        "max": {
          "value": round(max_kmh, 2),
          "unit": "km/h",
        },
      },
      "time": {
        "start": trackpoints[0].timestamp.isoformat(),
        "end": trackpoints[-1].timestamp.isoformat(),
        "duration": str(duration),
      },
      "count": len(trackpoints),
    })
  