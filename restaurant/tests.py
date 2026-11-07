from django.contrib.auth import get_user_model
from django.contrib.staticfiles import finders
from django.test import TestCase
from rest_framework.test import APITestCase

from .models import MenuItem

MENU = "/restaurant/menu/items/"
BOOKINGS = "/restaurant/booking/tables/"


class RestaurantTests(TestCase):
    def test_menu_item_representation(self):
        item = MenuItem.objects.create(title="IceCream", price=80, inventory=100)
        self.assertEqual(str(item), "IceCream : 80")

    def test_home_and_stylesheet(self):
        response = self.client.get("/")
        self.assertContains(response, "Little Lemon")
        self.assertContains(response, "/static/restaurant/style.css")
        self.assertIsNotNone(finders.find("restaurant/style.css"))


class RestaurantAPITests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user("reviewer", password="test-only-example")

    def test_registration_login_and_logout(self):
        credentials = {"username": "newguest", "password": "Review-Example-9301"}
        self.assertEqual(self.client.post("/auth/users/", credentials).status_code, 201)
        response = self.client.post("/auth/token/login/", credentials)
        self.assertEqual(response.status_code, 200)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + response.data["auth_token"])
        self.assertEqual(self.client.get(BOOKINGS).status_code, 200)
        self.assertEqual(self.client.post("/auth/token/logout/").status_code, 204)
        self.assertEqual(self.client.get(BOOKINGS).status_code, 401)

    def test_anonymous_access(self):
        for path in [MENU, BOOKINGS]:
            with self.subTest(path=path):
                self.assertEqual(self.client.get(path).status_code, 401)
                self.assertEqual(self.client.post(path, {}, format="json").status_code, 401)

    def check_crud(self, path, data, updated, patch):
        self.client.force_authenticate(self.user)
        response = self.client.post(path, data, format="json")
        self.assertEqual(response.status_code, 201, response.data)
        detail = f'{path}{response.data["id"]}/'
        self.assertEqual(self.client.get(path).data, [response.data])
        self.assertEqual(self.client.get(detail).data, response.data)
        self.assertEqual(self.client.put(detail, updated, format="json").status_code, 200)
        result = self.client.patch(detail, patch, format="json")
        self.assertEqual(result.status_code, 200)
        for field, value in patch.items():
            self.assertEqual(result.data[field], value)
        self.assertEqual(self.client.delete(detail).status_code, 204)
        self.assertEqual(self.client.get(detail).status_code, 404)

    def test_menu_crud(self):
        item = {"title": "Greek salad", "price": "12.50", "inventory": 8}
        self.check_crud(MENU, item, item | {"price": "14.00"}, {"inventory": 6})

    def test_booking_crud(self):
        data = {"name": "Alex", "no_of_guests": 2, "booking_date": "2030-08-15T18:00:00Z"}
        self.check_crud(BOOKINGS, data, data | {"no_of_guests": 3}, {"name": "Sam"})

    def test_validation(self):
        self.client.force_authenticate(self.user)
        for path, data in [
            (MENU, {"title": "Soup", "price": "-1.00", "inventory": 8}),
            (BOOKINGS, {"name": "Sam", "no_of_guests": 0, "booking_date": "2030-08-15T18:00:00Z"}),
        ]:
            with self.subTest(path=path):
                self.assertEqual(self.client.post(path, data, format="json").status_code, 400)
