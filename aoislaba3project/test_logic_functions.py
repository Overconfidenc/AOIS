import unittest
from functions import *  # Replace 'your_module' with the actual module name

class TestLogicFunctions(unittest.TestCase):
    def test_parse_expression(self):
        self.assertEqual(parse_expression("a -> b"), "a>b")
        self.assertEqual(parse_expression("~a & b"), "=a&b")
        self.assertEqual(parse_expression("a | b"), "a|b")
        self.assertEqual(parse_expression(""), "")

    def test_apply_operator(self):
        stack = [1, 0]
        apply_operator('&', stack)
        self.assertEqual(stack, [0])
        stack = [1, 0]
        apply_operator('|', stack)
        self.assertEqual(stack, [1])
        stack = [1]
        apply_operator('!', stack)
        self.assertEqual(stack, [0])
        stack = [0, 1]
        apply_operator('>', stack)
        self.assertEqual(stack, [1])
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
        self.assertEqual(get_operator_precedence(')'), 0)

    def test_process_pending_operators(self):
        stack = [1, 0]
        op_stack = ['&']
        process_pending_operators('|', stack, op_stack)
        self.assertEqual(stack, [0])
        self.assertEqual(op_stack, [])

    def test_process_closing_parenthesis(self):
        stack = [1, 0]
        op_stack = ['(', '&']
        process_closing_parenthesis(stack, op_stack)
        self.assertEqual(stack, [0])
        self.assertEqual(op_stack, [])

    def test_evaluate_expression(self):
        self.assertEqual(evaluate_expression("a&b", {'a': 1, 'b': 1}), 1)
        self.assertEqual(evaluate_expression("a|b", {'a': 0, 'b': 0}), 0)
        self.assertEqual(evaluate_expression("!a", {'a': 1}), 0)
        self.assertEqual(evaluate_expression("(a&b)|c", {'a': 1, 'b': 0, 'c': 1}), 1)
        self.assertEqual(evaluate_expression("", {}), 0)

    def test_generate_combinations(self):
        self.assertEqual(generate_combinations(['a', 'b']), [[0, 0], [0, 1], [1, 0], [1, 1]])
        self.assertEqual(generate_combinations(['a']), [[0], [1]])
        self.assertEqual(generate_combinations([]), [[]])

    def test_build_truth_table(self):
        table = build_truth_table("a&b", ['a', 'b'])
        self.assertEqual(table, [[0, 0, 0], [0, 1, 0], [1, 0, 0], [1, 1, 1]])
        table = build_truth_table("", [])
        self.assertEqual(table, [[]])

    def test_get_sdnf(self):
        table = [[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 1]]
        self.assertEqual(get_sdnf(table, ['a', 'b']), "(¬a&b) | (a&¬b) | (a&b)")
        table = [[0, 0, 0], [0, 1, 0]]
        self.assertEqual(get_sdnf(table, ['a', 'b']), "0")

    def test_get_sknf(self):
        table = [[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 1]]
        self.assertEqual(get_sknf(table, ['a', 'b']), "(a|b)")
        table = [[0, 0, 1], [0, 1, 1]]
        self.assertEqual(get_sknf(table, ['a', 'b']), "1")

    def test_get_numeric_form_sdnf(self):
        table = [[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 1]]
        self.assertEqual(get_numeric_form_sdnf(table), [1, 2, 3])

    def test_get_numeric_form_sknf(self):
        table = [[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 1]]
        self.assertEqual(get_numeric_form_sknf(table), [0])

    def test_get_index_form(self):
        table = [[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 1]]
        self.assertEqual(get_index_form(table), "0111")

    def test_glue_terms(self):
        self.assertEqual(glue_terms("a&b", "a&¬b", "ab", True), "a")
        self.assertEqual(glue_terms("a|b", "a|¬b", "ab", False), "a")
        self.assertIsNotNone(glue_terms("a&b", "¬a&b", "ab", True))

    def test_evaluate_term(self):
        table = [[1, 1, 1], [1, 0, 0]]
        self.assertTrue(evaluate_term("a&b", table[0], ['a', 'b'], True))
        self.assertFalse(evaluate_term("a&b", table[1], ['a', 'b'], True))
        self.assertFalse(evaluate_term("a|b", [0, 0, 0], ['a', 'b'], False))

    def test_minimize_calculation(self):
        table = [[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 1]]
        terms = ["¬a&b", "a&¬b", "a&b"]
        min_terms, stages, coverage = minimize_calculation(terms, table, ['a', 'b'], True)
        self.assertIn("a", min_terms)
        self.assertIn("b", min_terms)

    def test_remove_redundant_implicants(self):
        table = [[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 1]]
        terms = ["a", "b"]
        coverage = {"a": {2, 3}, "b": {1, 3}}
        result = remove_redundant_implicants(terms, table, ['a', 'b'], coverage, True)
        self.assertEqual(sorted(result), ["a", "b"])

    def test_build_coverage_table(self):
        table = [[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 1]]
        terms = ["a", "b"]
        result = build_coverage_table(terms, table, ['a', 'b'], True)
        self.assertIn("(0,1)", result)
        self.assertIn("X", result)

    def test_build_karnaugh_map(self):
        table = [[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 1]]
        result = build_karnaugh_map(table, ['a', 'b'])
        self.assertIn("b\\a", result)
        self.assertIn("0 1", result)

    def test_build_karnaugh_map_n3(self):
        # Тест для n=3: функция возвращает 1, если хотя бы две переменные равны 1
        expr = "(a&b) | (a&c) | (b&c)"
        variables = ['a', 'b', 'c']
        table = build_truth_table(expr, variables)
        
        expected_map = [
            "bc\\a 00 01 11 10",
            "0    0 0 1 0",
            "1    0 1 1 1"
        ]
        expected_map_str = "\n".join(expected_map)
        
        result = build_karnaugh_map(table, variables)
        self.assertEqual(result, expected_map_str)
    
    def test_build_karnaugh_map_n4(self):
        # Тест для n=4: функция возвращает 1, если четное количество переменных равно 1
        expr = "(a^b^c^d)"
        variables = ['a', 'b', 'c', 'd']
        table = build_truth_table(expr, variables)
        
        expected_map = [
            "cd\\ab 00 01 11 10",
            "00  0 0 0 0",
            "01  0 0 0 0",
            "11  1 1 1 1",
            "10  1 1 1 1"
        ]
        expected_map_str = "\n".join(expected_map)
        
        result = build_karnaugh_map(table, variables)
        self.assertEqual(result, expected_map_str)

    def test_minimize_karnaugh(self):
        table = [[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 1]]
        terms = ["¬a&b", "a&¬b", "a&b"]
        karnaugh_map, min_terms = minimize_karnaugh(terms, table, ['a', 'b'], True)
        self.assertIn("b\\a", karnaugh_map)
        self.assertIn("a", min_terms)
        self.assertIn("b", min_terms)

class TestMinimizeKarnaughSDNFN3(unittest.TestCase):
    def test_sdnf_single_variable(self):
        # Test case: F = a (all rows where a=1 are 1)
        expr = "a"
        variables = ['a', 'b', 'c']
        table = build_truth_table(expr, variables)
        _, terms = minimize_karnaugh([], table, variables, is_dnf=True)
        self.assertEqual(set(terms), {"a", "c"})

    def test_sdnf_two_variables(self):
        # Test case: F = a&b (rows where a=1, b=1 are 1)
        expr = "a&b"
        variables = ['a', 'b', 'c']
        table = build_truth_table(expr, variables)
        _, terms = minimize_karnaugh([], table, variables, is_dnf=True)
        self.assertEqual(set(terms), {"a","b"})

    def test_sdnf_pair_ab(self):
        # Test case: F = a&b | a&¬b (group where a=1, b varies, c varies)
        expr = "a&b | a&¬b"
        variables = ['a', 'b', 'c']
        table = build_truth_table(expr, variables)
        _, terms = minimize_karnaugh([], table, variables, is_dnf=True)
        self.assertEqual(set(terms), {"a","b"})

    def test_sdnf_pair_ac(self):
        # Test case: F = a&c | a&¬c (group where a=1, c varies, b varies)
        expr = "a&c | a&¬c"
        variables = ['a', 'b', 'c']
        table = build_truth_table(expr, variables)
        _, terms = minimize_karnaugh([], table, variables, is_dnf=True)
        self.assertEqual(set(terms), {"a","c"})

    def test_sdnf_pair_bc(self):
        # Test case: F = b&c | b&¬c (group where b=1, c varies, a varies)
        expr = "b&c | b&¬c"
        variables = ['a', 'b', 'c']
        table = build_truth_table(expr, variables)
        _, terms = minimize_karnaugh([], table, variables, is_dnf=True)
        self.assertEqual(set(terms), {"b","c"})

    def test_sdnf_no_groups(self):
        # Test case: F = a&b&c (single minterm, no larger groups)
        expr = "a&b&c"
        variables = ['a', 'b', 'c']
        table = build_truth_table(expr, variables)
        _, terms = minimize_karnaugh([], table, variables, is_dnf=True)
        self.assertEqual(set(terms), set())

if __name__ == '__main__':
    unittest.main()