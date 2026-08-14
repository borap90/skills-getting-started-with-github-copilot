"""
Tests for DELETE /activities/{activity_name}/unregister endpoint.

These tests validate that students can unregister from activities,
with proper validation and error handling.
"""

import pytest


class TestUnregister:
    """Tests for the DELETE /unregister endpoint."""

    def test_unregister_success(self, client):
        """
        Test: Successful unregister removes email from participants.
        
        Arrange: Select Chess Club, existing participant "michael@mergington.edu"
        Act: DELETE /activities/Chess Club/unregister?email=michael@mergington.edu
        Assert: Status 200, email removed from list, response confirms removal
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"
        
        # Verify email is present before unregister
        activities = client.get("/activities").json()
        assert email in activities[activity_name]["participants"]
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        assert "message" in response.json()
        assert email in response.json()["message"]
        assert activity_name in response.json()["message"]
        
        # Verify email was removed
        activities = client.get("/activities").json()
        assert email not in activities[activity_name]["participants"]

    def test_unregister_not_enrolled(self, client):
        """
        Test: Unregistering non-enrolled student returns 400.
        
        Arrange: Select Chess Club, prepare email "nonenrolled@mergington.edu" (not in participants)
        Act: DELETE /activities/Chess Club/unregister?email=nonenrolled@mergington.edu
        Assert: Status 400 with "not signed up" message
        """
        # Arrange
        activity_name = "Chess Club"
        non_enrolled_email = "nonenrolled@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": non_enrolled_email}
        )
        
        # Assert
        assert response.status_code == 400
        assert "not signed up for this activity" in response.json()["detail"].lower()

    def test_unregister_activity_not_found(self, client):
        """
        Test: Unregister from non-existent activity returns 404.
        
        Arrange: Prepare fake activity "Fake Activity", any email
        Act: DELETE /activities/Fake Activity/unregister?email=test@example.com
        Assert: Status 404 with "Activity not found" message
        """
        # Arrange
        fake_activity = "Fake Activity"
        email = "test@example.com"
        
        # Act
        response = client.delete(
            f"/activities/{fake_activity}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_unregister_updates_participant_count(self, client):
        """
        Test: Participant count decreases after unregister.
        
        Arrange: Get initial count for Gym Class (should be 2)
        Act: DELETE unregister with existing participant
        Assert: New count is exactly 1 less (becomes 1)
        """
        # Arrange
        activity_name = "Gym Class"
        email = "john@mergington.edu"
        
        # Get initial count
        initial_response = client.get("/activities")
        initial_count = len(initial_response.json()[activity_name]["participants"])
        assert initial_count > 0  # Ensure we can unregister
        
        # Act
        unregister_response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert unregister_response.status_code == 200
        
        # Verify count decreased
        final_response = client.get("/activities")
        final_count = len(final_response.json()[activity_name]["participants"])
        assert final_count == initial_count - 1

    def test_unregister_response_message_format(self, client):
        """
        Test: Response message includes expected information.
        
        Arrange: Select activity with existing participant
        Act: POST DELETE unregister request
        Assert: Response message contains email and activity name
        """
        # Arrange
        activity_name = "Debate Team"
        email = "ava@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        message = response.json()["message"]
        assert email in message
        assert activity_name in message
        assert "Unregistered" in message

    def test_unregister_then_signup_same_activity(self, client):
        """
        Test: Can sign up again after unregistering.
        
        Arrange: Prepare activity and email
        Act: Unregister, then sign up again
        Assert: Both operations succeed
        """
        # Arrange
        activity_name = "Soccer League"
        email = "alex@mergington.edu"
        
        # Act - Unregister
        unregister_response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        # Assert unregister succeeded
        assert unregister_response.status_code == 200
        
        # Act - Sign up again
        signup_response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert signup succeeded
        assert signup_response.status_code == 200
        
        # Verify email is back in participants
        activities = client.get("/activities").json()
        assert email in activities[activity_name]["participants"]

    def test_unregister_cannot_unregister_twice(self, client):
        """
        Test: Cannot unregister the same email twice.
        
        Arrange: Prepare activity and email to unregister
        Act: Unregister twice with same email
        Assert: First succeeds (200), second fails (400)
        """
        # Arrange
        activity_name = "Science Club"
        email = "noah@mergington.edu"
        
        # Act - First unregister
        response1 = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        # Act - Second unregister with same email
        response2 = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 400
        assert "not signed up for this activity" in response2.json()["detail"].lower()
