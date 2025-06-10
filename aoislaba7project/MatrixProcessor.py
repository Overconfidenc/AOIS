from LogicalOperations import *

class MatrixProcessor:
    def __init__(self, data_grid):
        self.grid = data_grid
        self.row_num = len(data_grid)
        self.col_num = len(data_grid[0]) if self.row_num > 0 else 0

    def apply_logical_operation(
        self, source_col1, source_col2, target_col, operation_name
    ):
        word1 = [
            int(bit)
            for bit in self._get_vertical_data_word(source_col1)
        ]
        word2 = [
            int(bit)
            for bit in self._get_vertical_data_word(source_col2)
        ]

        operation_result = []
        for i in range(self.row_num):
            if operation_name == "xor":
                result_bit = LogicalOperations.xor_operation(word1[i], word2[i])
            elif operation_name == "equivalence":
                result_bit = LogicalOperations.equivalence_operation(
                    word1[i], word2[i]
                )
            elif operation_name == "implication":
                result_bit = LogicalOperations.implication_operation(word1[i], word2[i])
            elif operation_name == "disjunction_neg":
                result_bit = LogicalOperations.disjunction_with_negation(
                    word1[i], word2[i]
                )
            else:
                result_bit = 0
            operation_result.append(int(result_bit))

        rotated_word = operation_result[(-1 * target_col) :] + operation_result[
            : (-1 * target_col)
        ]

        for i in range(self.row_num):
            self.grid[i][target_col] = rotated_word[i]

    def process_key_addition(self, binary_key):
        key_digits = [int(bit) for bit in binary_key]

        for column in range(self.col_num):
            validation_bits = []
            for bit_pos in range(3):
                row = (column + bit_pos) % self.row_num
                validation_bits.append(self.grid[row][column])

            if validation_bits != key_digits:
                continue

            operand_a = []
            for bit_pos in range(3, 7):
                row = (column + bit_pos) % self.row_num
                operand_a.append(self.grid[row][column])

            operand_b = []
            for bit_pos in range(7, 11):
                row = (column + bit_pos) % self.row_num
                operand_b.append(self.grid[row][column])

            num_a = int("".join(map(str, operand_a)), 2)
            num_b = int("".join(map(str, operand_b)), 2)
            total = num_a + num_b

            sum_bits = [int(bit) for bit in f"{total:05b}"]
            for bit_pos in range(5):
                row = (column + 11 + bit_pos) % self.row_num
                self.grid[row][column] = sum_bits[bit_pos]

    def _get_vertical_data_word(self, column_pos):
        vertical_data = []
        for row in range(self.row_num):
            vertical_data.append(self.grid[row][column_pos])

        rotated_data = (
            vertical_data[column_pos:] + vertical_data[:column_pos]
        )
        return "".join(map(str, rotated_data))

    def get_sorted_indices(self, reverse_order=True):
        remaining_indices = set(range(self.row_num))
        sorted_indices = []

        while remaining_indices:
            candidate_indices = list(remaining_indices)
            selected = []

            for bit_pos in range(self.col_num):
                target_value = 1 if reverse_order else 0
                current_selection = []

                for row in candidate_indices:
                    if self.grid[row][bit_pos] == target_value:
                        current_selection.append(row)

                if current_selection:
                    candidate_indices = current_selection
                    if len(candidate_indices) == 1:
                        break

            sorted_indices.extend(candidate_indices)
            remaining_indices.difference_update(candidate_indices)

        return sorted_indices

    def extract_diagonal_address(self, column_position):
        diagonal_values = []
        for bit_pos in range(self.col_num):
            current_row = (column_position + bit_pos) % self.row_num
            diagonal_values.append(self.grid[current_row][bit_pos])
        return diagonal_values