from tests.automation.automation_client import AutomationClient
import unittest


server_url = "http://localhost:8000"


class TestMain(unittest.TestCase):

    def setUp(self) -> None:
        self.client = AutomationClient(server_url)

    def fake_proxies(self, count: int, job_name: str):
        proxies = []
        for i in range(count):
            proxies.append({
                "ip": f"192.168.1.{i}",
                "port": 8080,
                "username": "username",
                "password": "password",
                "proxy_type": "HTTP",
                "country": "US",
                "service_name": "proxy_service",
                "job_names": [job_name],
                "active": True
            })
        return proxies

    def test_main(self):

        proxies = self.fake_proxies(5, "job1")

        outputs = []
        with self.subTest("Create proxies"):
            for proxy in proxies:
                response = self.client.post_proxy(proxy)
                outputs.append(response.json()["data"])

            self.assertEqual(len(outputs), 5)

        with self.subTest("Get proxies per one"):
            for output in outputs:
                response = self.client.get_proxy(output["id"])
                self.assertEqual(response.json()["data"], output)

        with self.subTest("Get proxies all"):
            response = self.client.get_proxies()
            self.assertEqual(len(response.json()["data"]), 5)

        with self.subTest("Edit proxies"):
            for output in outputs:
                response = self.client.edit_proxy(output["id"], {
                    "port": 8081,
                    "username": "username1",
                    "password": "password1",
                    "job_names": ["job2"],
                    "active": False
                })
                self.assertEqual(response.json()["data"]["port"], 8081)
                self.assertEqual(response.json()["data"]["username"], "username1")
                self.assertEqual(response.json()["data"]["password"], "password1")
                self.assertEqual(response.json()["data"]["job_names"], ["job2"])
                self.assertEqual(response.json()["data"]["active"], False)
                output["port"] = 8081
                output["username"] = "username1"
                output["password"] = "password1"
                output["job_names"] = ["job2"]
                output["active"] = False

        with self.subTest("Delete proxies"):
            for output in outputs:
                response = self.client.delete_proxy(output["id"])
                self.assertEqual(response.json()["data"], output)

            response = self.client.get_proxies()
            self.assertEqual(len(response.json()["data"]), 0)
