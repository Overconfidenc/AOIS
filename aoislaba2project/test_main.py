import unittest
from main import (
    parse_expression, apply_operator, get_operator_precedence, evaluate_expression,
    generate_combinations, build_truth_table, get_sdnf, get_sknf,
    get_numeric_form_sdnf, get_numeric_form_sknf, get_index_form
)

class TestLogicEvaluator(unittest.TestCase):
    def test_parse_expression(self):
        self.assertEqual(parse_expression("a -> b"), "a>b")
        self.assertEqual(parse_expression("a ~ b"), "a=b")
        self.assertEqual(parse_expression("a & b "), "a&b")
        self.assertEqual(parse_expression(""), "")

    def test_apply_operator(self):
        stack = [1]
        apply_operator('!', stack)
        self.assertEqual(stack, [0])

        stack = [1, 0]
        apply_operator('&', stack)
        self.assertEqual(stack, [0])

        stack = [1, 0]
        apply_operator('|', stack)
        self.assertEqual(stack, [1])

        stack = [1, 0]
        apply_operator('>', stack)
        self.assertEqual(stack, [0])

        stack = [1, 1]
        apply_operator('=', stack)
        self.assertEqual(stack, [1])

    def test_get_operator_precedence(self):
        self.assertEqual(get_operator_precedence('!'), 3)
        self.assertEqual(get_operator_precedence('&'), 2)
        self.assertEqual(get_operator_precedence('|'), 2)
        self.assertEqual(get_operator_precedence('>'), 1)
        self.assertEqual(get_operator_precedence('='), 1)
        self.assertEqual(get_operator_precedence('('), 0)

    def test_evaluate_expression(self):
        values = {'a': 1, 'b': 0, 'c': 1}
        self.assertEqual(evaluate_expression("a&b", values), 0)
        self.assertEqual(evaluate_expression("!a|c", values), 1)
        self.assertEqual(evaluate_expression("(a>b)&c", values), 0)
        self.assertEqual(evaluate_expression("a=b", values), 0)
        self.assertEqual(evaluate_expression("", {}), 0)

    def test_generate_combinations(self):
        self.assertEqual(generate_combinations(['a']), [[0], [1]])
        self.assertEqual(generate_combinations(['a', 'b']), [[0, 0], [0, 1], [1, 0], [1, 1]])
        self.assertEqual(generate_combinations([]), [[]])

    def test_build_truth_table(self):
        table = build_truth_table("a&b", ['a', 'b'])
        self.assertEqual(table, [[0, 0, 0], [0, 1, 0], [1, 0, 0], [1, 1, 1]])

        table = build_truth_table("!a", ['a'])
        self.assertEqual(table, [[0, 1], [1, 0]])

        table = build_truth_table("", [])
        self.assertEqual(table, [[]])

    def test_get_sdnf(self):
        table = [[0, 0, 0], [0, 1, 0], [1, 0, 0], [1, 1, 1]]
        variables = ['a', 'b']
        self.assertEqual(get_sdnf(table, variables), "(a&b)")

        table = [[0, 0], [1, 0]]
        self.assertEqual(get_sdnf(table, ['a']), "0")

    def test_get_sknf(self):
        table = [[0, 0, 0], [0, 1, 0], [1, 0, 0], [1, 1, 1]]
        variables = ['a', 'b']
        self.assertEqual(get_sknf(table, variables), "(!a|b) & (a|!b) & (a|b)")
 
        table = [[0, 1], [1, 1]]
        self.assertEqual(get_sknf(table, ['a']), "1")

    def test_get_numeric_form_sdnf(self):
        table = [[0, 0, 0], [0, 1, 0], [1, 0, 0], [1, 1, 1]]
        self.assertEqual(get_numeric_form_sdnf(table), [3])

        table = [[0, 0], [1, 0]]
        self.assertEqual(get_numeric_form_sdnf(table), [])

    def test_get_numeric_form_sknf(self):
        table = [[0, 0, 0], [0, 1, 0], [1, 0, 0], [1, 1, 1]]
        self.assertEqual(get_numeric_form_sknf(table), [0, 1, 2])

        table = [[0, 1], [1, 1]]
        self.assertEqual(get_numeric_form_sknf(table), [])

    def test_get_index_form(self):
        table = [[0, 0, 0], [0, 1, 0], [1, 0, 0], [1, 1, 1]]
        self.assertEqual(get_index_form(table), "0001")

        table = [[0, 1], [1, 0]]
        self.assertEqual(get_index_form(table), "10")

        table = []
        self.assertEqual(get_index_form(table), "")

if __name__ == "__main__":
    unittest.main()