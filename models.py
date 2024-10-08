from extensions import db
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from uuid import uuid4
from datetime import datetime

class Fahrer(db.Model):
    __tablename__   =   'Fahrer'

    fahrer_id:     Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))
    fahrer_name:   Mapped[str] = mapped_column(nullable=False)
  
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
      db.session.delete(self)
      db.session.commit()

class Fahrzeug(db.Model):
    __tablename__   = 'Fahrzeug'

    fahrzeug_id:   Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))
    license_plate: Mapped[str] = mapped_column(nullable=False)
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
      db.session.delete(self)
      db.session.commit()

class Track(db.Model):
    __tablename__   = 'Track'

    track_id:     Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))
    fahrer_id:    Mapped[str] = mapped_column(ForeignKey('Fahrer.fahrer_id'), nullable=False)
    fahrzeug_id:  Mapped[str] = mapped_column(ForeignKey('Fahrzeug.fahrzeug_id'), nullable=False)
    dateiname:    Mapped[str] = mapped_column(nullable=False)
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
      db.session.delete(self)
      db.session.commit()

class TrackPoint(db.Model):
    __tablename__   = 'TrackPoint'

    punkt_id:   Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))
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

    