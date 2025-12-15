import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestSweetCRUD:

    def setup_method(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            username="user1",
            password="testpass123"
        )

        self.admin = User.objects.create_superuser(
            username="admin",
            password="adminpass123"
        )

        self.client.force_authenticate(user=self.user)

    def test_create_sweet(self):
        response = self.client.post(
            "/api/sweets/",
            {
                "name": "Ladoo",
                "category": "Indian",
                "price": 10.5,
                "quantity": 50
            },
            format="json"
        )

        assert response.status_code == 201
        assert response.data["name"] == "Ladoo"

    def test_list_sweets(self):
        self.client.post(
            "/api/sweets/",
            {
                "name": "Barfi",
                "category": "Indian",
                "price": 20,
                "quantity": 10
            },
            format="json"
        )

        response = self.client.get("/api/sweets/")

        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]["name"] == "Barfi"

    def test_update_sweet(self):
        sweet = self.client.post(
            "/api/sweets/",
            {
                "name": "Jalebi",
                "category": "Indian",
                "price": 15,
                "quantity": 25
            },
            format="json"
        ).data

        response = self.client.put(
            f"/api/sweets/{sweet['id']}/",
            {
                "name": "Jalebi",
                "category": "Indian",
                "price": 18,
                "quantity": 25
            },
            format="json"
        )

        assert response.status_code == 200
        assert response.data["price"] == 18

    def test_delete_sweet_admin_only(self):
        sweet = self.client.post(
            "/api/sweets/",
            {
                "name": "Peda",
                "category": "Indian",
                "price": 12,
                "quantity": 30
            },
            format="json"
        ).data

        # normal user cannot delete
        response = self.client.delete(f"/api/sweets/{sweet['id']}/")
        assert response.status_code == 403

        # admin can delete
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(f"/api/sweets/{sweet['id']}/")
        assert response.status_code == 204
