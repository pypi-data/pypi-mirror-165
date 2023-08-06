import unittest

from fastforward.model_for_sequence_classification import ModelForSequenceClassification


class ModelForEncodingTest(unittest.TestCase):

    def test_classification(self):
        model = ModelForSequenceClassification("./dummy")
        self.assertTrue(model("The product is great!") is not None)

    def test_classification_batch(self):
        model = ModelForSequenceClassification("./dummy")
        self.assertEqual(len(model(["The product is great!", "the product is bad!"])), 2)
