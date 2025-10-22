from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def test_get_activities_contains_keys():
    res = client.get("/activities")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, dict)
    # Check a known activity exists
    assert "Chess Club" in data


def test_signup_and_unregister_flow():
    activity = "Chess Club"
    email = "testuser@mergington.edu"

    # Ensure email not present initially
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # Signup
    res = client.post(f"/activities/{activity}/signup?email={email}")
    assert res.status_code == 200
    assert email in activities[activity]["participants"]

    # Signup again should fail with 400
    res2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert res2.status_code == 400

    # Unregister
    res3 = client.delete(f"/activities/{activity}/participants?email={email}")
    assert res3.status_code == 200
    assert email not in activities[activity]["participants"]

    # Unregister again should 404
    res4 = client.delete(f"/activities/{activity}/participants?email={email}")
    assert res4.status_code == 404


def test_signup_nonexistent_activity():
    res = client.post("/activities/NoSuchActivity/signup?email=x@y.z")
    assert res.status_code == 404


def test_unregister_nonexistent_activity():
    res = client.delete("/activities/NoSuchActivity/participants?email=x@y.z")
    assert res.status_code == 404
