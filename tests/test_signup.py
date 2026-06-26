from src import app as app_module


def test_signup_success_adds_new_participant(client):
    # Arrange
    activity_name = "Chess Club"
    new_email = "new.student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={new_email}")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {new_email} for {activity_name}"}
    assert new_email in app_module.activities[activity_name]["participants"]


def test_signup_returns_404_for_unknown_activity(client):
    # Arrange
    activity_name = "Unknown Club"
    email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_returns_400_for_duplicate_email(client):
    # Arrange
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={existing_email}")

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_supports_url_encoded_activity_name(client):
    # Arrange
    encoded_activity_name = "Math%20Club"
    email = "encoded.test@mergington.edu"

    # Act
    response = client.post(f"/activities/{encoded_activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert email in app_module.activities["Math Club"]["participants"]


def test_signup_accepts_non_email_formatted_string(client):
    # Arrange
    activity_name = "Programming Class"
    non_standard_email = "not-an-email"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={non_standard_email}")

    # Assert
    assert response.status_code == 200
    assert non_standard_email in app_module.activities[activity_name]["participants"]


def test_signup_allows_exceeding_max_participants(client):
    # Arrange
    activity_name = "Chess Club"
    max_participants = app_module.activities[activity_name]["max_participants"]
    app_module.activities[activity_name]["participants"] = [
        f"student{i}@mergington.edu" for i in range(max_participants)
    ]
    extra_email = "over.limit@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={extra_email}")

    # Assert
    assert response.status_code == 200
    assert len(app_module.activities[activity_name]["participants"]) == max_participants + 1
    assert extra_email in app_module.activities[activity_name]["participants"]
