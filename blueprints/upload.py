from flask import request, jsonify, Blueprint, current_app
import os
import re
from models import Fahrer, Fahrzeug, Track, TrackPoint
import gpxpy
from extensions import db
import time
from sqlalchemy.exc import IntegrityError

upload_bp = Blueprint("upload", __name__)

pattern = r'^([A-Za-z0-9]+)_([A-Za-z0-9]+)_(\d{3})\.gpx$'

def extract_driver_and_license(filename):
  match = re.match(pattern, filename)
  if match:
    driver:         str  = match.group(1)
    license_plate:  str  = match.group(2)
    return driver, license_plate
  else:
    raise ValueError("Invalid file format. Please use  <NAME_Fahrer>_<POLKZ>_001.gpx")
  
def get_track_points(file, track_id):
  gpx = gpxpy.parse(file)
        
  track_points = []
  
  for track in gpx.tracks:
      for segment in track.segments:
          for point in segment.points:
              track_point = TrackPoint(
                  track_id=track_id,
                  timestamp=point.time,
                  lat=point.latitude,
                  lon=point.longitude,
                  ele=point.elevation
              )
              track_points.append(track_point)
  
  if track_points:
      db.session.bulk_save_objects(track_points)
      db.session.commit()
  
  
def write_to_db(driver, license_plate, file_name, file):
  fahrer = Fahrer.get_fahrer_by_name(name = driver)
  fahrzeug = Fahrzeug.get_fahrzeug_by_license_plate(license_plate = license_plate)
  track = Track(fahrer_id=fahrer.fahrer_id, fahrzeug_id=fahrzeug.fahrzeug_id, dateiname=file_name)
  track.save()

  get_track_points(file, track.track_id)

@upload_bp.post("")
def upload_file():
  if 'file' not in request.files:
    return jsonify({"error": "No file provided"}), 400

  file = request.files['file']

  if file.filename == '':
    return jsonify({"error": "No selected file"}), 400
  
  if Track.file_exists(file.filename):
    return jsonify({"error": "File already exists"}), 400
  
  try:
    driver, license_plate = extract_driver_and_license(file.filename)
  except ValueError as e:
    return jsonify({"error": str(e)}), 400

  if file:
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename)
    try:
      write_to_db(driver, license_plate, file.filename, file)
    except IntegrityError:
      db.session.rollback()
      return jsonify({"error": "File already exists"}), 400
    file.save(file_path)
    return jsonify({"message": f"File {file.filename} uploaded successfully"}), 200

  return jsonify({"error": "File upload failed"}), 500