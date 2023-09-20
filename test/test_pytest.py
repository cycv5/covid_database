import pytest

from main import app
from main import ADMIN_SECRET

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            pass
        yield client


def test_upload_time_series_death(client):
    file = {'file': open("test/time_series_test.csv", 'rb')}
    response = client.post("/time_series/death", data=file, content_type='multipart/form-data')
    assert response.data == b'Success'
    file['file'].close()


def test_upload_time_series_confirmed(client):
    file = {'file': open("test/time_series_test.csv", 'rb')}
    response = client.post("/time_series/confirmed", data=file, content_type='multipart/form-data')
    assert response.data == b'Success'
    file['file'].close()


def test_upload_time_series_active(client):
    file = {'file': open("test/time_series_test.csv", 'rb')}
    response = client.post("/time_series/active", data=file, content_type='multipart/form-data')
    assert response.data == b'Success'
    file['file'].close()


def test_upload_time_series_recovered(client):
    file = {'file': open("test/time_series_test.csv", 'rb')}
    response = client.post("/time_series/recovered", data=file, content_type='multipart/form-data')
    assert response.data == b'Success'
    file['file'].close()


def test_upload_daily_report(client):
    file = {'file': open("test/daily_report_test.csv", 'rb')}
    response = client.post("/daily_reports/2020-03-25", data=file, content_type='multipart/form-data')
    assert response.data == b'Success'
    file['file'].close()


def test_upload_error(client):
    response = client.post("/daily_reports/2020")
    assert response.data == b'no file part'


def test_query_multi_types_multi_date_json(client):
    req = '/cases?data_type=death&data_type=confirmed&locations=%7B%0A%20%20%22country_region%22%3A%20%22US%22%2C%0A%20%20%22state_province%22%3A%20%22Kentucky%22%2C%0A%20%20%22combined_key%22%3A%20%22%22%0A%7D&locations=%7B%0A%20%20%22country_region%22%3A%20%22Canada%22%2C%0A%20%20%22state_province%22%3A%20%22British%20Columbia%22%2C%0A%20%20%22combined_key%22%3A%20%22%22%0A%7D&start_time=2020-01-23&end_time=2020-01-31'
    response = client.get(req, headers={'accept': 'application/json'}, )
    assert response.json == [{'country_region': 'US', 'state_province': 'Kentucky', 'combined_key': '', 'date': '2020-01-23', 'cases': 2, 'type': 'death'}, {'country_region': 'US', 'state_province': 'Kentucky', 'combined_key': '', 'date': '2020-01-24', 'cases': 3, 'type': 'death'}, {'country_region': 'US', 'state_province': 'Kentucky', 'combined_key': '', 'date': '2020-01-25', 'cases': 122, 'type': 'death'}, {'country_region': 'US', 'state_province': 'Kentucky', 'combined_key': '', 'date': '2020-01-26', 'cases': 3, 'type': 'death'}, {'country_region': 'US', 'state_province': 'Kentucky', 'combined_key': '', 'date': '2020-01-23', 'cases': 2, 'type': 'confirmed'}, {'country_region': 'US', 'state_province': 'Kentucky', 'combined_key': '', 'date': '2020-01-24', 'cases': 3, 'type': 'confirmed'}, {'country_region': 'US', 'state_province': 'Kentucky', 'combined_key': '', 'date': '2020-01-25', 'cases': 122, 'type': 'confirmed'}, {'country_region': 'US', 'state_province': 'Kentucky', 'combined_key': '', 'date': '2020-01-26', 'cases': 3, 'type': 'confirmed'}, {'country_region': 'Canada', 'state_province': 'British Columbia', 'combined_key': '', 'date': '2020-01-23', 'cases': 2, 'type': 'death'}, {'country_region': 'Canada', 'state_province': 'British Columbia', 'combined_key': '', 'date': '2020-01-24', 'cases': 4, 'type': 'death'}, {'country_region': 'Canada', 'state_province': 'British Columbia', 'combined_key': '', 'date': '2020-01-26', 'cases': 5, 'type': 'death'}, {'country_region': 'Canada', 'state_province': 'British Columbia', 'combined_key': '', 'date': '2020-01-23', 'cases': 2, 'type': 'confirmed'}, {'country_region': 'Canada', 'state_province': 'British Columbia', 'combined_key': '', 'date': '2020-01-24', 'cases': 4, 'type': 'confirmed'}, {'country_region': 'Canada', 'state_province': 'British Columbia', 'combined_key': '', 'date': '2020-01-26', 'cases': 5, 'type': 'confirmed'}]


def test_query_single_type_multi_date_csv(client):
    req = '/cases?data_type=active&locations=%7B%0A%20%20%22country_region%22%3A%20%22Canada%22%2C%0A%20%20%22state_province%22%3A%20%22British%20Columbia%22%2C%0A%20%20%22combined_key%22%3A%20%22%22%0A%7D&start_time=2020-01-23&end_time=2020-01-31'
    response = client.get(req, headers={'accept': 'text/csv'})
    assert response.data == b'index,country_region,state_province,combined_key,date,cases,type\n0,Canada,British Columbia,,2020-01-23,2,active\n1,Canada,British Columbia,,2020-01-24,4,active\n2,Canada,British Columbia,,2020-01-26,5,active\n'


def test_query_multi_type_single_date_csv(client):
    req = '/cases?data_type=active&data_type=recovered&locations=%7B%0A%20%20%22country_region%22%3A%20%22Canada%22%2C%0A%20%20%22state_province%22%3A%20%22British%20Columbia%22%2C%0A%20%20%22combined_key%22%3A%20%22%22%0A%7D&start_time=2020-01-23'
    response = client.get(req, headers={'accept': 'text/csv'})
    assert response.data == b'index,country_region,state_province,combined_key,date,cases,type\n0,Canada,British Columbia,,2020-01-23,2,active\n1,Canada,British Columbia,,2020-01-23,2,recovered\n'


def test_query_single_type_single_date_json(client):
    req = '/cases?data_type=active&locations=%7B%0A%20%20%22country_region%22%3A%20%22Canada%22%2C%0A%20%20%22state_province%22%3A%20%22British%20Columbia%22%2C%0A%20%20%22combined_key%22%3A%20%22%22%0A%7D&start_time=2020-01-23'
    response = client.get(req, headers={'accept': 'application/json'})
    assert response.json == [{'country_region': 'Canada', 'state_province': 'British Columbia', 'combined_key': '', 'date': '2020-01-23', 'cases': 2, 'type': 'active'}]


def test_delete_db(client):
    response = client.get("/admin", headers={'secret': ADMIN_SECRET})
    assert response.data == b'DB Cleared'

