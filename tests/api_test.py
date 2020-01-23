import unittest

from starlette.testclient import TestClient
from icenews.server import app


class TestApi(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_important_words_ok(self):
        r = self.client.post(
            "/v1/important_words", json={"input_string": "Fjórðungur til fósturs ber"}
        )
        self.assertEqual(200, r.status_code)
        self.assertEqual(
            {"important_words": ["Fjórðungur", "fóstur", "ber", "fjórðungur", "bera"]},
            r.json(),
        )

    def test_important_words_invalid_input(self):
        self.assertEqual(
            422,
            self.client.post(
                "/v1/important_words", json={"input_String": "hæ"}
            ).status_code,
        )
        self.assertEqual(
            422,
            self.client.post(
                "/v1/important_words", json={"input_string": ""}
            ).status_code,
        )
        self.assertEqual(
            422,
            self.client.post(
                "/v1/important_words", json={"input_string": None}
            ).status_code,
        )
        self.assertEqual(
            422,
            self.client.post(
                "/v1/important_words", json={"input_stringx": "hæ"}
            ).status_code,
        )

    def test_important_words_limit(self):
        self.assertEqual(
            200,
            self.client.post(
                "/v1/important_words", json={"input_string": "x" * 2000}
            ).status_code,
        )
        self.assertEqual(
            422,
            self.client.post(
                "/v1/important_words", json={"input_string": "x" * 2001}
            ).status_code,
        )

    def test_parse_ok(self):
        response = self.client.post(
            "/v1/parse", json={"in": "Fjórðungur til fósturs ber"}
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual(
            {"important_words": ["Fjórðungur", "fóstur", "ber", "fjórðungur", "bera"]},
            response.json(),
        )


if __name__ == "__main__":
    unittest.main()
