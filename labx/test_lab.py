# LabX
# Simple architecture, design and prototype of a Lab Test Result distribution system via QR Codes
# London, Apr 2021 - https://github.com/narcismpap/labx

import unittest
import json

from lab import create_app

EXAMPLE_QR = (
    "00|a7738550-d543-4f78-b464-1f3e4c6690d5|1619818359|John Snow00000000000|3|9618d8811f3627afdab84cfe6b98f9f0"
)


class LabTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        # @todo: setup db

    def tearDown(self):
        # @todo: close db
        pass

    def test_qr_generation(self):
        response = self.client.get("/api/1.0/qr/a7738550-d543-4f78-b464-1f3e4c6690d5/")
        rsp = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(rsp, EXAMPLE_QR)

    def test_online_verification(self):
        response = self.client.get("/api/1.0/result/a7738550-d543-4f78-b464-1f3e4c6690d5/")
        rsp = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            json.loads(rsp),
            {
                "name": "John Snow",
                "outcome": 3,
                "test": "a7738550-d543-4f78-b464-1f3e4c6690d5",
                "time": "2021-04-30 21:09:1619818359",
                "version": "00",
            },
        )

    def test_offline_verification(self):
        response = self.client.post("/api/1.0/verify/", data={"qr": EXAMPLE_QR})
        rsp = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            json.loads(rsp),
            {
                "name": "John Snow",
                "outcome": 3,
                "test": "a7738550-d543-4f78-b464-1f3e4c6690d5",
                "time": "2021-04-30 21:09:1619818359",
                "version": "00",
            },
        )
