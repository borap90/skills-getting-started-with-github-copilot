"""
Shared test fixtures and configuration for the Activities API tests.

This module provides pytest fixtures for:
- app: A fresh FastAPI application instance per test
- client: A TestClient bound to the app
- activities_backup: A deep copy of the initial activities state for isolation
"""

import pytest
from copy import deepcopy
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def test_app():
    """
    Fixture that provides a fresh FastAPI app instance for each test.
    
    Arrange: Initialize a new app instance
    """
    return app


@pytest.fixture
def client(test_app):
    """
    Fixture that provides a TestClient bound to the test app.
    
    Arrange: Create a TestClient for making HTTP requests
    """
    return TestClient(test_app)


@pytest.fixture(autouse=True)
def reset_activities():
    """
    Fixture that resets the in-memory activities data before each test.
    
    This ensures test isolation by providing a clean slate.
    The fixture uses deep copy to preserve original data structure.
    
    Arrange: Reset activities to initial state before each test
    """
    # Store original activities data
    original_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Competitive basketball team for intramural and tournament play",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["james@mergington.edu"]
        },
        "Soccer League": {
            "description": "Co-ed soccer team with regular matches and friendly competitions",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 22,
            "participants": ["alex@mergington.edu", "marcus@mergington.edu"]
        },
        "Art Studio": {
            "description": "Explore painting, drawing, and sculpture techniques",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 16,
            "participants": ["isabella@mergington.edu"]
        },
        "Drama Club": {
            "description": "Perform in theatrical productions and develop acting skills",
            "schedule": "Fridays, 4:00 PM - 5:30 PM",
            "max_participants": 24,
            "participants": ["lucas@mergington.edu", "grace@mergington.edu"]
        },
        "Debate Team": {
            "description": "Develop critical thinking and public speaking through competitive debate",
            "schedule": "Mondays and Thursdays, 3:30 PM - 4:45 PM",
            "max_participants": 18,
            "participants": ["ava@mergington.edu"]
        },
        "Science Club": {
            "description": "Conduct experiments and explore scientific concepts through hands-on projects",
            "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
            "max_participants": 20,
            "participants": ["noah@mergington.edu", "liam@mergington.edu"]
        }
    }
    
    # Clear and reset activities with a deep copy
    activities.clear()
    activities.update(deepcopy(original_activities))
    
    yield
    
    # Cleanup after test (reset again for safety)
    activities.clear()
    activities.update(deepcopy(original_activities))
