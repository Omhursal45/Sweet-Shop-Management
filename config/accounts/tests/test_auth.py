import pytest
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


def test_user_can_register():
    client = APIClient()

    response = client.post(
        "/api/auth/register/",
        {
            "username": "om",
            "email": "om@test.com",
            "password": "testpass123",
        },
        format="json",
    )

    assert response.status_code == 201
    assert "access" in response.data


def test_user_can_login():
    client = APIClient()

    client.post(
        "/api/auth/register/",
        {
            "username": "om",
            "email": "om@test.com",
            "password": "testpass123",
        },
        format="json",
    )

    response = client.post(
        "/api/auth/login/",
        {
            "username": "om",
            "password": "testpass123",
        },
        format="json",
    )

    assert response.status_code == 200
    assert "access" in response.data
