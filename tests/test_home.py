import datetime
from http import HTTPStatus

def test_successfully_create_appointment_doctor_who(client):
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
    assert response.json == json_value



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
