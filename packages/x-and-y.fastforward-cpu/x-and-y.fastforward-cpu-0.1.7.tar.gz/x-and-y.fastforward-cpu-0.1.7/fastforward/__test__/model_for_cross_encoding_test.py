import unittest

from fastforward.model_for_cross_encoding import ModelForCrossEncoding


class ModelForCrossEncodingTest(unittest.TestCase):

    def test_encode(self):
        encoder = ModelForCrossEncoding("./dummy", use_sigmoid=True)
        self.assertTrue(encoder(("A", "B")) is not None)
        self.assertTrue(encoder(("A", "B")) is not None)

    def test_encode_batch(self):
        encoder = ModelForCrossEncoding("./dummy", use_sigmoid=True)
        self.assertEqual(len(encoder([("A", "B"), ("A", "B")])), 2)
        self.assertEqual(len(encoder([("A", "B"), ("A", "B")])), 2)

    def test_encode_batch_with_different_sequence_lengths(self):
        encoder = ModelForCrossEncoding("./dummy", use_sigmoid=True)
        self.assertEqual(len(encoder([("A", "B"), ("A", "B")])), 2)
        self.assertEqual(len(encoder([("A", "B C"), ("A", "B C D E")])), 2)