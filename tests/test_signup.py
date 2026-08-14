"""
Tests for POST /activities/{activity_name}/signup endpoint.

These tests validate that students can sign up for activities,
with proper duplicate prevention and error handling.
"""

import pytest


class TestSignup:
    """Tests for the POST /signup endpoint."""

    def test_signup_success(self, client):
        """
        Test: Successful signup adds email to participants.
        
        Arrange: Prepare activity "Chess Club", new email "newstudent@mergington.edu"
        Act: POST /activities/Chess Club/signup?email=newstudent@mergington.edu
        Assert: Status 200, email in participants list, response message contains email & activity
        """
        # Arrange
        activity_name = "Chess Club"
        new_email = "newstudent@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": new_email}
        )
        
        # Assert
        assert response.status_code == 200
        assert "message" in response.json()
        assert new_email in response.json()["message"]
        assert activity_name in response.json()["message"]
        
        # Verify participant was added
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert new_email in activities[activity_name]["participants"]

    def test_signup_duplicate_prevention(self, client):
        """
        Test: Duplicate signup is prevented.
        
        Arrange: Select Chess Club and a new email
        Act: POST signup with same email twice
        Assert: First succeeds (200), second returns 400 with error message
        """
        # Arrange
        activity_name = "Chess Club"
        new_email = "duplicate_test@mergington.edu"
        
        # Act - First signup (should succeed)
        response1 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": new_email}
        )
        
        # Act - Second signup with same email (should fail)
        response2 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": new_email}
        )
        
        # Assert
        assert response1.status_code == 200  # First signup succeeds
        assert response2.status_code == 400  # Second signup fails
        assert "already signed up" in response2.json()["detail"].lower()

    def test_signup_activity_not_found(self, client):
        """
        Test: Signup for non-existent activity returns 404.
        
        Arrange: Prepare fake activity "Nonexistent Club", valid email
        Act: POST /activities/Nonexistent Club/signup?email=test@example.com
        Assert: Status 404 with "Activity not found" message
        """
        # Arrange
        fake_activity = "Nonexistent Club"
        email = "test@example.com"
        
        # Act
        response = client.post(
            f"/activities/{fake_activity}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_signup_updates_participant_count(self, client):
        """
        Test: Participant count increases after signup.
        
        Arrange: Get initial count for Programming Class (should be 2)
        Act: POST signup with new email
        Assert: New count is exactly 1 more (becomes 3)
        """
        # Arrange
        activity_name = "Programming Class"
        new_email = "newparticipant@mergington.edu"
        
        # Get initial count
        initial_response = client.get("/activities")
        initial_count = len(initial_response.json()[activity_name]["participants"])
        
        # Act
        signup_response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": new_email}
        )
        
        # Assert
        assert signup_response.status_code == 200
        
        # Verify count increased
        final_response = client.get("/activities")
        final_count = len(final_response.json()[activity_name]["participants"])
        assert final_count == initial_count + 1

    def test_signup_response_message_format(self, client):
        """
        Test: Response message includes expected information.
        
        Arrange: Prepare activity and email for signup
        Act: POST signup request
        Assert: Response message contains both email and activity name
        """
        # Arrange
        activity_name = "Art Studio"
        email = "student@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        message = response.json()["message"]
        assert email in message
        assert activity_name in message
        assert "Signed up" in message

    def test_signup_multiple_different_activities(self, client):
        """
        Test: Same email can sign up for different activities.
        
        Arrange: Prepare a new email and two different activities
        Act: POST signup for first activity, then second activity
        Assert: Both signups succeed (200)
        """
        # Arrange
        email = "versatile@mergington.edu"
        activity1 = "Chess Club"
        activity2 = "Drama Club"
        
        # Act
        response1 = client.post(
            f"/activities/{activity1}/signup",
            params={"email": email}
        )
        response2 = client.post(
            f"/activities/{activity2}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        # Verify email in both activities
        activities = client.get("/activities").json()
        assert email in activities[activity1]["participants"]
        assert email in activities[activity2]["participants"]
