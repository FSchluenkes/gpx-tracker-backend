from flask import request, jsonify, Blueprint
from models import Track, TrackPoint, Fahrer, Fahrzeug
from sqlalchemy import select, func
from extensions import db

tracks_bp = Blueprint("tracks", __name__)

@tracks_bp.post("")
def get_tracks():

  query = (
    select(
      Track.track_id,
      Fahrer.fahrer_name,
      Fahrzeug.license_plate,
      func.min(TrackPoint.timestamp).label("start_time"),
      func.max(TrackPoint.timestamp).label("end_time")
    )
    .join(Fahrer, Fahrer.fahrer_id == Track.fahrer_id)
    .join(Fahrzeug, Fahrzeug.fahrzeug_id == Track.fahrzeug_id)
    .join(TrackPoint, TrackPoint.track_id == Track.track_id)
    .group_by(
      Track.track_id,
      Fahrer.fahrer_name,
      Fahrzeug.license_plate
    )
  )

  records = db.session.execute(query).fetchall()

  result = []
  for record in records:
    result.append(
      {
        "id": record[0],
        "driver": record[1],
        "licensePlate": record[2],
        "startTime": record[3].isoformat(),
        "endTime": record[4].isoformat(),
      }
    )

  return jsonify(result)