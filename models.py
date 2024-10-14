from extensions import db
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from uuid import uuid4
from datetime import datetime

class Fahrer(db.Model):
  __tablename__   =   'Fahrer'

  fahrer_id:     Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  fahrer_name:   Mapped[str] = mapped_column(nullable=False)

  def save(self):
    db.session.add(self)
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  @classmethod
  def get_fahrer_by_name(cls, name: str):
    if cls.query.filter_by(fahrer_name = name).count() > 0:
      return cls.query.filter_by(fahrer_name = name).scalar()
    else:
      fahrer = Fahrer(fahrer_name=name)
      fahrer.save()
      return fahrer
    
class Fahrzeug(db.Model):
  __tablename__   = 'Fahrzeug'

  fahrzeug_id:   Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  license_plate: Mapped[str] = mapped_column(nullable=False)
  
  def save(self):
      db.session.add(self)
      db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()
  
  @classmethod
  def get_fahrzeug_by_license_plate(cls, license_plate: str):
    if cls.query.filter_by(license_plate = license_plate).count() > 0:
      return cls.query.filter_by(license_plate = license_plate).scalar()
    else:
      fahrzeug = Fahrzeug(license_plate = license_plate)
      fahrzeug.save()
      return fahrzeug
    
class Track(db.Model):
  __tablename__   = 'Track'

  track_id:     Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  fahrer_id:    Mapped[str] = mapped_column(ForeignKey('Fahrer.fahrer_id'), nullable=False)
  fahrzeug_id:  Mapped[str] = mapped_column(ForeignKey('Fahrzeug.fahrzeug_id'), nullable=False)
  dateiname:    Mapped[str] = mapped_column(nullable=False)
  
  def save(self):
    db.session.add(self)
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()
  
  @classmethod
  def file_exists(cls, filename: str):
    return cls.query.filter_by(dateiname = filename).count() > 0

class TrackPoint(db.Model):
  __tablename__   = 'TrackPoint'

  punkt_id:   Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  track_id:   Mapped[str] = mapped_column(ForeignKey('Track.track_id'), nullable=False)
  timestamp:  Mapped[datetime] = mapped_column(nullable=False)
  lat:        Mapped[float] = mapped_column(nullable=False)
  lon:        Mapped[float] = mapped_column(nullable=False)
  ele:        Mapped[float] = mapped_column(nullable=False)
  
  def save(self):
    db.session.add(self)
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()