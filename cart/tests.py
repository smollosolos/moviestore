from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from movies.models import Movie
from .models import Order, Item
from .services import get_top_purchaser


class TopPurchaserTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin_user = User.objects.create_superuser(
            username="test_admin",
            email="admin@example.com",
            password="TestPassword123!",
        )
        cls.user_a = User.objects.create_user(
            username="buyer_a",
            password="TestPassword123!",
        )
        cls.user_b = User.objects.create_user(
            username="buyer_b",
            password="TestPassword123!",
        )
        cls.movie = Movie.objects.create(
            name="Test Movie",
            description="Movie used for testing.",
            price=10,
        )

    def setUp(self):
        self.url = reverse("admin:cart_order_purchase_leader")

    def make_purchase(self, user, quantity):
        order = Order.objects.create(
            user=user,
            total=self.movie.price * quantity,
        )
        Item.objects.create(
            order=order,
            movie=self.movie,
            price=self.movie.price,
            quantity=quantity,
        )

    def test_admin_can_access_page(self):
        self.client.force_login(self.admin_user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "admin/cart/order/purchase_leader.html",
        )

    def test_regular_user_cannot_access_page(self):
        self.client.force_login(self.user_a)

        response = self.client.get(self.url)

        self.assertRedirects(
            response,
            reverse("admin:login") + "?next=" + self.url,
            fetch_redirect_response=False,
        )

    def test_staff_without_order_permission_is_forbidden(self):
        staff_user = User.objects.create_user(
            username="staff_without_permission",
            password="TestPassword123!",
            is_staff=True,
        )
        self.client.force_login(staff_user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 403)

    def test_empty_purchase_history(self):
        self.assertIsNone(get_top_purchaser())

        self.client.force_login(self.admin_user)
        response = self.client.get(self.url)

        self.assertContains(
            response,
            "No purchases have been recorded yet.",
        )

    def test_quantities_are_summed_across_orders(self):
        self.make_purchase(self.user_a, 2)
        self.make_purchase(self.user_a, 3)
        self.make_purchase(self.user_b, 4)

        result = get_top_purchaser()

        self.assertEqual(result["order__user__id"], self.user_a.id)
        self.assertEqual(result["total_movies"], 5)

    def test_leader_updates_after_another_user_purchases_more(self):
        self.make_purchase(self.user_a, 2)
        self.client.force_login(self.admin_user)

        response = self.client.get(self.url)
        self.assertContains(response, "buyer_a")
        self.assertEqual(
            response.context["top_purchaser"]["total_movies"],
            2,
        )

        self.make_purchase(self.user_b, 3)

        response = self.client.get(self.url)
        self.assertContains(response, "buyer_b")
        self.assertEqual(
            response.context["top_purchaser"]["total_movies"],
            3,
        )

    def test_tie_uses_lowest_user_id(self):
        self.make_purchase(self.user_a, 2)
        self.make_purchase(self.user_b, 2)

        result = get_top_purchaser()

        self.assertEqual(result["order__user__id"], self.user_a.id)