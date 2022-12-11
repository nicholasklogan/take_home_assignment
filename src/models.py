from src.extensions import db
from flask import jsonify


class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    doctor = db.Column(db.String, nullable=False)
    start_time = db.Column(db.Float, nullable=False)
    end_time = db.Column(db.Float, nullable=False)

    def json(self) -> str:
        """
        :return: Serializes this object to JSON
        """
        return jsonify({
            'doctor': self.doctor,
            'start_time': self.start_time,
            'end_time': self.end_time
        })