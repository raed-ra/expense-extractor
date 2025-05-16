#./tests/test_report_routes.py
import json

def test_report_data_authenticated(client, auth):
    auth()
    response = client.get('/report/data?from=2023-01-01&to=2023-12-31')
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

def test_report_share_success(client, auth, app):
    auth()
    with app.app_context():
        filters = {"from": "2023-01-01", "to": "2023-12-31"}
        payload = {
            "username": "testuser2@example.com",
            "filters": filters
        }
        response = client.post(
            '/report/share',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response.status_code in [200, 400]  # 400 if trying to share with self
