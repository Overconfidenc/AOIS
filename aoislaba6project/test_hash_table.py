import unittest
from hash_table import HashTable, create_table_from_dict


class TestHashTableClass(unittest.TestCase):
    def test_expand_table(self):
        table = HashTable()
        self.assertEqual(table.capacity, 8)
        table.insert("A", "B")
        table.insert("C", "D")
        table.insert("E", "F")
        table.insert("G", "H")
        table.insert("I", "J")
        table.insert("K", "L")
        self.assertEqual(table.capacity, 16)

    def test_insert(self):
        table = HashTable()
        self.assertEqual(str(table), "")
        table.insert("A", "B")
        self.assertEqual(str(table), "A - B")
        table.insert("C", "D")
        self.assertEqual(str(table), "A - B\nC - D")
        table.insert("C", "E")
        self.assertEqual(str(table), "A - B\nC - D")

    def test_retrieve(self):
        table = HashTable()
        table.insert("A", "B")
        self.assertEqual(table.retrieve("A"), "B")
        self.assertIsNone(table.retrieve("C"))

    def test_remove(self):
        table = HashTable()
        table.insert("A", "B")
        table.insert("C", "D")
        table.remove("A")
        self.assertEqual(str(table), "C - D")
        table.remove("E")
        self.assertEqual(str(table), "C - D")

    def test_create_table_from_dict(self):
        terms = {
            "A": "B",
            "C": "D",
            "E": "F"
        }
        table = create_table_from_dict(terms)
        self.assertEqual(str(table), "A - B\nC - D\nE - F")
