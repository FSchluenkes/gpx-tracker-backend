from extensions import db
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from sqlalchemy.exc import IntegrityError
from uuid import uuid4
from datetime import datetime

class Fahrer(db.Model):
  __tablename__   =   'Fahrer'

  fahrer_id:     Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  fahrer_name:   Mapped[str] = mapped_column(nullable=False, unique=True)

  def save(self):
    db.session.add(self)
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  @classmethod
  def get_fahrer_by_name(cls, name: str):
    fahrer = cls.query.filter_by(fahrer_name=name).first()
    
    if fahrer:
       return fahrer

    try:
      new_fahrer = cls(fahrer_name=name)
      db.session.add(new_fahrer)
      db.session.commit()
      return new_fahrer

    except IntegrityError:
      db.session.rollback()
      return cls.query.filter_by(fahrer_name=name).first()
    
class Fahrzeug(db.Model):
  __tablename__   = 'Fahrzeug'

  fahrzeug_id:   Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  license_plate: Mapped[str] = mapped_column(nullable=False, unique=True)
  
  def save(self):
      db.session.add(self)
      db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()
  
  @classmethod
  def get_fahrzeug_by_license_plate(cls, license_plate: str):
    fahrzeug = cls.query.filter_by(license_plate = license_plate).first()
    
    if fahrzeug:
       return fahrzeug

    try:
      new_fahrzeug = cls(license_plate=license_plate)
      db.session.add(new_fahrzeug)
      db.session.commit()
      return new_fahrzeug

    except IntegrityError:
      db.session.rollback()
      return cls.query.filter_by(license_plate = license_plate).first()
    
class Track(db.Model):
  __tablename__   = 'Track'

  track_id:     Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  fahrer_id:    Mapped[str] = mapped_column(ForeignKey('Fahrer.fahrer_id'), nullable=False)
  fahrzeug_id:  Mapped[str] = mapped_column(ForeignKey('Fahrzeug.fahrzeug_id'), nullable=False)
  dateiname:    Mapped[str] = mapped_column(nullable=False, unique=True)
  
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