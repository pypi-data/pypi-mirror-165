import unittest

from fastforward.model_for_sequence_similarity import ModelForSequenceSimilarity


class ModelForSimilarityTest(unittest.TestCase):

    def test_encode(self):
        model = ModelForSequenceSimilarity("./dummy")
        self.assertTrue(model(("A", "B")) is not None)

    def test_encode_batch(self):
        model = ModelForSequenceSimilarity("./dummy")
        self.assertEqual(len(model([("A", "B"), ("A", "B")])), 2)
