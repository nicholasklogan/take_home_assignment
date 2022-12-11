from flask import Blueprint, jsonify, abort
from http import HTTPStatus
from src.extensions import db
from sqlalchemy import or_
from src.models import DummyModel, Appointment
from webargs import fields
from webargs.flaskparser import use_args

home = Blueprint('/', __name__)


# Helpful documentation:
# https://webargs.readthedocs.io/en/latest/framework_support.html
# https://flask.palletsprojects.com/en/2.0.x/quickstart/#variable-rules


@home.route('/')
def index():
    return {'data': 'OK'}


def start_time_overlaps(appointment: dict) -> bool:
    return not Appointment.query.filter(
            Appointment.doctor==appointment['doctor'],
            Appointment.start_time <= appointment['start_time'],
            Appointment.end_time >= appointment['start_time']
            ).first() == None


def end_time_overlaps(appointment: dict) -> bool:
    return not Appointment.query.filter(
            Appointment.doctor==appointment['doctor'],
            Appointment.start_time <= appointment['end_time'],
            Appointment.end_time >= appointment['end_time']
            ).first() == None

@home.route('/schedule_appointment', methods=['POST'])
@use_args({'doctor': fields.String(), 'start_time': fields.Float(), 'end_time': fields.Float()})
def schedule_appointment(args):
    appointment_dict = {'doctor': args.get('doctor'), 'start_time': args.get('start_time'), 'end_time': args.get('end_time')}
    if start_time_overlaps(appointment_dict) or end_time_overlaps(appointment_dict):
        abort(409)

    new_record = Appointment(**appointment_dict)
    db.session.add(new_record)
    db.session.commit()
    return new_record.json()


@home.route('/dummy_model/<id_>', methods=['GET'])
def dummy_model(id_):
    record = DummyModel.query.filter_by(id=id_).first()
    if record is not None:
        return record.json()
    else:
        return jsonify(None), HTTPStatus.NOT_FOUND


@home.route('/dummy_model', methods=['POST'])
@use_args({'value': fields.String()})
def dummy_model_create(args):
    new_record = DummyModel(value=args.get('value'))
    db.session.add(new_record)
    db.session.commit()
    return new_record.json()
