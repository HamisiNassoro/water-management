"""
In this tests, its good practice that we test the BEHAVIOUR, NOT
THE IMPLEMENTATION

Every Test should have 3 parts, abreviated as AAA:
A: Arrange
A: Act
A: Assert
"""
from rest_framework import status
from rest_framework.test import APIClient
class TestCreateMeter:
    def test_if_user_is_anonymous_returns_401(self):
        client = APIClient()
        response = client.post('/api/meter/meter/', {'description':"meter test", 'current_reading':'45'})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED