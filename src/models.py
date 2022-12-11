from src.extensions import db
from flask import jsonify


class DummyModel(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.String, nullable=False)

    def json(self) -> str:
        """
        :return: Serializes this object to JSON
        """
        return jsonify({'id': self.id, 'value': self.value})


class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    doctor = db.Column(db.String, nullable=False)
    start_time = db.Column(db.DATETIME, nullable=False)
    end_time = db.Column(db.DATETIME, nullable=False)

    def json(self) -> str:
        """
        :return: Serializes this object to JSON
        """
        return jsonify({
            'id': self.id,
            'doctor': self.doctor,
            'start_time': self.start_time,
            'end_time': self.end_time
        })