import unittest

from icenews.server import app
from starlette.testclient import TestClient
from typing import Tuple


class TestApi(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_important_words_ok(self) -> None:
        r = self.client.post(
            "/v1/important_words", json={"input_string": "Fjórðungur til fósturs ber"}
        )
        self.assertEqual(200, r.status_code)
        self.assertEqual(
            {"important_words": ["Fjórðungur", "fóstur", "ber", "fjórðungur", "bera"]},
            r.json(),
        )

    def test_important_words_invalid_input(self) -> None:
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

    def test_important_words_limit(self) -> None:
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

    def test_parse_ok(self) -> None:
        response = self.client.post(
            "/v1/parse", json={"in": "Fjórðungur til fósturs ber"}
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual(
            {"important_words": ["Fjórðungur", "fóstur", "ber", "fjórðungur", "bera"]},
            response.json(),
        )

    def api_detect_language(self, input_string: str) -> Tuple[str, bool]:
        response = self.client.post(
            "/v1/detect_language", json={"input_string": input_string},
        )
        self.assertEqual(200, response.status_code)
        result = response.json()
        return result["language"], result["reliable"]

    def test_detect_language_ok(self):
        self.assertEqual(("un", False), self.api_detect_language("Hello"))
        self.assertEqual(
            ("is", True), self.api_detect_language("Fjórðungur til fósturs ber")
        )
        self.assertEqual(
            ("en", True),
            self.api_detect_language("I would have called Friðhildur earlier."),
        )


if __name__ == "__main__":
    unittest.main()
