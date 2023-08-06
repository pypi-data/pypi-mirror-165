import unittest

from fastforward.model_for_encoding import ModelForEncoding


class ModelForEncodingTest(unittest.TestCase):

    def test_encode(self):
        encoder = ModelForEncoding("./dummy")
        self.assertTrue(encoder("A") is not None)

    def test_encode_batch(self):
        encoder = ModelForEncoding("./dummy")
        self.assertEqual(len(encoder(["A", "B C D"])), 2)
