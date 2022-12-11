import datetime
from http import HTTPStatus
from src.models import Appointment


def test_successfully_create_appointment_doctor_who(client):
    # Setup
    json_value = {
        "doctor": "Who",
        "start_time": datetime.datetime(year=2022, month=12, day=11, hour=13, minute=0, second=0).timestamp(),
        "end_time": datetime.datetime(year=2022, month=12, day=11, hour=13, minute=30, second=0).timestamp()
    }
    # Test
    response = client.post(
        "/schedule_appointment",
        json=json_value
    )

    # Verify
    assert response.status_code == HTTPStatus.OK
    assert response.json == json_value
    db_value = Appointment.query.filter_by(**json_value).first()
    assert db_value.doctor == json_value['doctor']
    assert db_value.start_time == json_value['start_time']
    assert db_value.end_time == json_value['end_time']

def test_direct_conflict_create_appointment_doctor_who(client):
    # Setup
    json_value = {
        "doctor": "Who",
        "start_time": datetime.datetime(year=2022, month=12, day=11, hour=13, minute=0, second=0).timestamp(),
        "end_time": datetime.datetime(year=2022, month=12, day=11, hour=13, minute=30, second=0).timestamp()
    }

    response = client.post(
        "/schedule_appointment",
        json=json_value
    )
    assert response.status_code == HTTPStatus.OK
    # Test
    response = client.post(
        "/schedule_appointment",
        json=json_value
    )
    # Verify
    assert response.status_code == HTTPStatus.CONFLICT
    assert len(Appointment.query.filter_by(**json_value).all()) == 1


def test_start_time_overlap_create_appointment_doctor_who(client):
    # Setup
    first_appointment = {
        "doctor": "Who",
        "start_time": datetime.datetime(year=2022, month=12, day=11, hour=13, minute=0, second=0).timestamp(),
        "end_time": datetime.datetime(year=2022, month=12, day=11, hour=13, minute=30, second=0).timestamp()
    }
    second_appointment = {
        "doctor": "Who",
        "start_time": datetime.datetime(year=2022, month=12, day=11, hour=13, minute=15, second=0).timestamp(),
        "end_time": datetime.datetime(year=2022, month=12, day=11, hour=13, minute=30, second=0).timestamp()
    }
    response = client.post(
        "/schedule_appointment",
        json=first_appointment
    )
    assert response.status_code == HTTPStatus.OK
    # Test
    response = client.post(
        "/schedule_appointment",
        json=second_appointment
    )
    # Verify
    assert response.status_code == HTTPStatus.CONFLICT
    assert Appointment.query.filter_by(**second_appointment).first() == None


def test_end_time_overlap_create_appointment_doctor_who(client):
    # Setup
    first_appointment = {
        "doctor": "Who",
        "start_time": datetime.datetime(year=2022, month=12, day=11, hour=13, minute=0, second=0).timestamp(),
        "end_time": datetime.datetime(year=2022, month=12, day=11, hour=13, minute=30, second=0).timestamp()
    }
    second_appointment = {
        "doctor": "Who",
        "start_time": datetime.datetime(year=2022, month=12, day=11, hour=12, minute=15, second=0).timestamp(),
        "end_time": datetime.datetime(year=2022, month=12, day=11, hour=13, minute=15, second=0).timestamp()
    }
    response = client.post(
        "/schedule_appointment",
        json=first_appointment
    )
    assert response.status_code == HTTPStatus.OK
    # Test
    response = client.post(
        "/schedule_appointment",
        json=second_appointment
    )
    # Verify
    assert response.status_code == HTTPStatus.CONFLICT
    assert Appointment.query.filter_by(**second_appointment).first() == None

def test_around_existing_create_appointment_doctor_who(client):
    # Setup
    first_appointment = {
        "doctor": "Who",
        "start_time": datetime.datetime(year=2022, month=12, day=11, hour=13, minute=0, second=0).timestamp(),
        "end_time": datetime.datetime(year=2022, month=12, day=11, hour=13, minute=30, second=0).timestamp()
    }
    second_appointment = {
        "doctor": "Who",
        "start_time": datetime.datetime(year=2022, month=12, day=11, hour=12, minute=15, second=0).timestamp(),
        "end_time": datetime.datetime(year=2022, month=12, day=11, hour=13, minute=45, second=0).timestamp()
    }
    response = client.post(
        "/schedule_appointment",
        json=first_appointment
    )
    assert response.status_code == HTTPStatus.OK
    # Test
    response = client.post(
        "/schedule_appointment",
        json=second_appointment
    )
    # Verify
    assert response.status_code == HTTPStatus.CONFLICT
    assert Appointment.query.filter_by(**second_appointment).first() == None



def test_home_api(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    # Response is binary string data because data is the raw data of the output.
    # The switch from ' to " is due to json serialization
    assert response.data == b'{"data":"OK"}\n'
    # json allows us to get back a deserialized data structure without us needing to manually do it
    assert response.json == {'data': 'OK'}


def test_dummy_model_api(client):
    response = client.post('/dummy_model', json={
        'value': 'foobar'
    })
    assert response.status_code == HTTPStatus.OK
    obj = response.json
    new_id = obj.get('id')
    response = client.get(f'/dummy_model/{new_id}')
    assert response.status_code == HTTPStatus.OK
    assert response.json.get('value') == 'foobar'
