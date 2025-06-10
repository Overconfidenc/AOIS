import unittest
from hash_utils import standardize_key, format_entry
from hash_table import HashTable


class TestHashTableFunctions(unittest.TestCase):
    def test_standardize_key(self):
        self.assertEqual(standardize_key("иММуниТЕТ"), "Иммунитет")
        self.assertEqual(standardize_key("вирус"), "Вирус")

    def test_format_entry(self):
        table = HashTable()
        table.insert("A", "B")
        self.assertEqual(format_entry(table, "A"), "A - B")
        self.assertEqual(format_entry(table, "C"), "C - None")
