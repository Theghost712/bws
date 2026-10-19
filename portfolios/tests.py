from django.test import TestCase
from django.urls import reverse


class PortfolioViewTests(TestCase):
    def test_obedi_portfolio_loads(self):
        response = self.client.get(reverse("portfolios:obedi"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Obedi Ming")
        self.assertContains(response, "css/portfolio.css")

    def test_portfolio_is_public(self):
        self.client.logout()
        response = self.client.get(reverse("portfolios:obedi"))
        self.assertEqual(response.status_code, 200)

    def test_nav_links_to_portfolio(self):
        response = self.client.get(reverse("core:home"))
        self.assertContains(response, reverse("portfolios:obedi"))
