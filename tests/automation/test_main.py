from tests.automation.automation_client import AutomationClient
import unittest
import time


server_url = "http://localhost:8000"


class TestMain(unittest.TestCase):

    def setUp(self) -> None:
        self.client = AutomationClient(server_url)

    def fake_proxies(self, count: int, job_name: str, proxy_type: str):
        proxies = []
        for i in range(count):
            proxies.append({
                "ip": f"192.168.1.{i}",
                "port": 8080,
                "username": "username",
                "password": "password",
                "proxy_type": proxy_type,
                "country": "US",
                "service_name": "proxy_service",
                "job_names": [job_name],
                "active": True
            })
        return proxies

    def test_crud(self):

        job_name = f"job_{time.time()}"
        proxies = self.fake_proxies(5, job_name, proxy_type="HTTP")

        outputs = []
        with self.subTest("Create proxies"):
            for proxy in proxies:
                response = self.client.post_proxy(proxy)
                print(response.json())
                outputs.append(response.json()["data"])

            self.assertEqual(len(outputs), 5)

        with self.subTest("Get proxies per one"):
            for output in outputs:
                response = self.client.get_proxy(output["id"])
                self.assertEqual(response.json()["data"], output)

        with self.subTest("Get proxies all"):
            response = self.client.get_proxies(job_name=job_name)
            self.assertEqual(len(response.json()["data"]), 5)

        with self.subTest("Edit proxies"):
            for output in outputs:
                response = self.client.edit_proxy(output["id"], {
                    "port": 8081,
                    "username": "username1",
                    "password": "password1",
                    "job_names": ["job2"],
                    "active": False,
                    "proxy_type": "HTTP"
                })
                print(response.json())
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

    def test_generation(self):

        job_name = f"job_{time.time()}"
        proxies = self.fake_proxies(6, job_name, proxy_type="HTTP")

        outputs = []
        with self.subTest("Create proxies"):
            for proxy in proxies:
                response = self.client.post_proxy(proxy)
                outputs.append(response.json()["data"])

            self.assertEqual(len(outputs), 6)

        with self.subTest("Generate proxies 1"):
            response = self.client.get_generate(3, job_name, proxy_type="HTTP")
            self.assertEqual(len(response.json()["data"]), 3)
            proxy_ids = [proxy["proxy_id"] for proxy in response.json()["data"]]

        with self.subTest("Check new proxies not in previous"):
            response = self.client.get_generate(2, job_name, proxy_type="HTTP")
            self.assertEqual(len(response.json()["data"]), 2)
            self.assertTrue(all([proxy["proxy_id"] not in proxy_ids for proxy in response.json()["data"]]))
            proxy_ids += [proxy["proxy_id"] for proxy in response.json()["data"]]

        with self.subTest("Check new proxies not in previous again"):
            response = self.client.get_generate(1, job_name, proxy_type="HTTP")
            self.assertEqual(len(response.json()["data"]), 1)
            self.assertTrue(all([proxy["proxy_id"] not in proxy_ids for proxy in response.json()["data"]]))

    def test_generation_2(self):

        job_name = f"job_{time.time()}"
        proxies = self.fake_proxies(4, job_name, proxy_type="HTTP")

        outputs = []
        with self.subTest("Create proxies"):
            for proxy in proxies:
                response = self.client.post_proxy(proxy)
                outputs.append(response.json()["data"])

            self.assertEqual(len(outputs), 4)

        with self.subTest("Generate proxies 1"):
            response = self.client.get_generate(3, job_name, proxy_type="HTTP")
            self.assertEqual(len(response.json()["data"]), 3)
            proxy_ids = [proxy["proxy_id"] for proxy in response.json()["data"]]

        with self.subTest("Check one new proxies in previous and one not"):
            response = self.client.get_generate(2, job_name, proxy_type="HTTP")
            self.assertEqual(len(response.json()["data"]), 2)
            new_proxies = [proxy for proxy in response.json()["data"] if proxy["proxy_id"] not in proxy_ids]
            old_proxies = [proxy for proxy in response.json()["data"] if proxy["proxy_id"] not in proxy_ids]
            self.assertEqual(len(new_proxies), 1)
            self.assertEqual(len(old_proxies), 1)
            proxy_ids += [proxy["proxy_id"] for proxy in response.json()["data"]]

        with self.subTest("Check all new proxies in previous"):
            response = self.client.get_generate(2, job_name, proxy_type="HTTP")
            self.assertEqual(len(response.json()["data"]), 2)
            old_proxies = [proxy for proxy in response.json()["data"] if proxy["proxy_id"] in proxy_ids]
            self.assertEqual(len(old_proxies), 2)

    def test_generation_proxy_types(self):

        job_name = f"job_{time.time()}"
        proxies = self.fake_proxies(4, job_name, proxy_type="HTTP")

        outputs = []
        with self.subTest("Create proxies"):
            for proxy in proxies:
                response = self.client.post_proxy(proxy)
                outputs.append(response.json()["data"])

            self.assertEqual(len(outputs), 4)

        with self.subTest("Check no proxies with HTTPS"):
            response = self.client.get_generate(3, job_name, proxy_type="HTTPS")
            self.assertEqual(len(response.json()["data"]), 0)

        proxies = self.fake_proxies(2, job_name, proxy_type="HTTPS")
        for proxy in proxies:
            response = self.client.post_proxy(proxy)
            outputs.append(response.json()["data"])

        with self.subTest("Check there proxies with HTTPS"):
            response = self.client.get_generate(3, job_name, proxy_type="HTTPS")
            self.assertEqual(len(response.json()["data"]), 2)
