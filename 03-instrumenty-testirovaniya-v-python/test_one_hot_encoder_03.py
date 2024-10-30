import unittest
from one_hot_encoder import fit_transform


class TestOneHotEncoder(unittest.TestCase):

    def test_one_value(self):
        data = ["a"]
        expected_result = [
            ("a", [1]),
        ]

        self.assertEqual(fit_transform(data), expected_result)

    def test_duplicate_values(self):
        data = ["Moscow", "New York", "Moscow", "London"]
        expected_result = [
            ("Moscow", [0, 0, 1]),
            ("New York", [0, 1, 0]),
            ("Moscow", [0, 0, 1]),
            ("London", [1, 0, 0]),
        ]
        self.assertEqual(fit_transform(data), expected_result)

    def test_empty_list(self, data=[], expected_result=[]):
        self.assertEqual(fit_transform(data), expected_result)

    def test_type_error_on_empty_input(self):
        with self.assertRaises(TypeError):
            fit_transform()

    def test_type_error_on_int_arg(self):
        # не понятно, зачем было так реализовывать))
        with self.assertRaises(TypeError):
            fit_transform(1, 2, 3)

    def test_keys(self):
        data = ["Moscow", "New York", "Moscow", "London"]
        result = fit_transform(data)
        for k, val in result:
            self.assertTrue(k in data)
            self.assertEqual(sum(val), 1)
