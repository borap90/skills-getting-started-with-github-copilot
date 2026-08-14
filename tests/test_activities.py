"""
Tests for GET /activities endpoint.

These tests validate that the activities endpoint returns all activities
with correct structure and data types.
"""

import pytest


class TestGetActivities:
    """Tests for the GET /activities endpoint."""

    def test_get_activities_returns_all_activities(self, client):
        """
        Test: Verify response contains all 9 activities.
        
        Arrange: Initialize test client
        Act: Call GET /activities
        Assert: Response has 200 status and contains all 9 activity names
        """
        # Arrange
        expected_activities = [
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Basketball Team",
            "Soccer League",
            "Art Studio",
            "Drama Club",
            "Debate Team",
            "Science Club"
        ]
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        activities = response.json()
        assert len(activities) == 9
        for activity_name in expected_activities:
            assert activity_name in activities

    def test_get_activities_response_structure(self, client):
        """
        Test: Verify each activity has required fields.
        
        Arrange: Initialize test client
        Act: Call GET /activities
        Assert: Each activity contains description, schedule, max_participants, participants
        """
        # Arrange
        required_fields = {
            "description",
            "schedule",
            "max_participants",
            "participants"
        }
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        assert response.status_code == 200
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_data, dict)
            assert required_fields.issubset(set(activity_data.keys()))

    def test_get_activities_participants_are_lists(self, client):
        """
        Test: Verify participants field is a list.
        
        Arrange: Initialize test client
        Act: Call GET /activities
        Assert: All participants fields are lists
        """
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        assert response.status_code == 200
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_data["participants"], list)
            assert isinstance(activity_data["max_participants"], int)
            assert isinstance(activity_data["description"], str)
            assert isinstance(activity_data["schedule"], str)

    def test_get_activities_initial_participants(self, client):
        """
        Test: Verify initial participant counts are correct.
        
        Arrange: Initialize test client
        Act: Call GET /activities
        Assert: Each activity has the expected initial participants
        """
        # Arrange
        expected_participants = {
            "Chess Club": ["michael@mergington.edu", "daniel@mergington.edu"],
            "Programming Class": ["emma@mergington.edu", "sophia@mergington.edu"],
            "Gym Class": ["john@mergington.edu", "olivia@mergington.edu"],
            "Basketball Team": ["james@mergington.edu"],
            "Soccer League": ["alex@mergington.edu", "marcus@mergington.edu"],
            "Art Studio": ["isabella@mergington.edu"],
            "Drama Club": ["lucas@mergington.edu", "grace@mergington.edu"],
            "Debate Team": ["ava@mergington.edu"],
            "Science Club": ["noah@mergington.edu", "liam@mergington.edu"]
        }
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        assert response.status_code == 200
        for activity_name, expected_emails in expected_participants.items():
            actual_participants = activities[activity_name]["participants"]
            assert sorted(actual_participants) == sorted(expected_emails)
