from django.test import SimpleTestCase
from django.urls import reverse, resolve

class ProjectSmokeTests(SimpleTestCase):
    def test_health_endpoint(self):
        response = self.client.get("/health/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_health_route_resolves(self):
        match = resolve("/health/")
        self.assertEqual(match.url_name, "health")
