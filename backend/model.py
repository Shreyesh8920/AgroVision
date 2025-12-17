from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class FarmData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)
    state = db.Column(db.String(100))
    district = db.Column(db.String(100))
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Float)
    rainfall = db.Column(db.Float)
    soil_moisture = db.Column(db.Float)
    soil_temperature = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "lat": self.lat,
            "lon": self.lon,
            "state": self.state,
            "district": self.district,
            "temperature": self.temperature,
            "humidity": self.humidity,
            "rainfall": self.rainfall,
            "soil_moisture": self.soil_moisture,
            "soil_temperature": self.soil_temperature,
            "created_at": self.created_at.isoformat()
        }