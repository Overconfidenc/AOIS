import random
from MatrixVisualizer import MatrixVisualizer
from MatrixGenerator import MatrixGenerator
from MatrixProcessor import MatrixProcessor
from LogicalOperations import LogicalOperations

def main():

    matrix = MatrixGenerator.create_binary_grid(16, 16)
    processor = MatrixProcessor(matrix)

    print("Исходная матрица (16x16):")
    MatrixVisualizer.display_grid(matrix)

    print("\nСчитывание адресного столбца 2:")
    bits = processor.extract_diagonal_address(2)
    print(bits)

    print("\nСчитывание слова 3:")
    word = processor._get_vertical_data_word(3)
    print(word)

    print(
        "\nИспользование f6 к словам 2 и 8, записать в слово 15:")
    processor.apply_logical_operation(2, 8, 15, "xor")
    MatrixVisualizer.display_grid(matrix)

    print(
        "\nИспользование f11 к словам 1 и 10, записать в слово 0:")
    processor.apply_logical_operation(1, 10, 0, "implication")
    MatrixVisualizer.display_grid(matrix)

    print(
        "\nИспользование f9 к словам 4 и 7, записать в слово 14:")
    processor.apply_logical_operation(4, 7, 14, "equivalence")
    MatrixVisualizer.display_grid(matrix)

    print(
        "\nИспользование f4 к словам 2 и 13, 1:")
    processor.apply_logical_operation(2, 13, 1, "disjunction_neg")
    MatrixVisualizer.display_grid(matrix)

    print("\nСложение полей A и B для слов с V = 011:")
    processor.process_key_addition("100")
    MatrixVisualizer.display_grid(matrix)

    print("\nОперация сортировки - упорядоченная выборка (по убыванию):")
    sorted_indices = processor.get_sorted_indices(True)
    sorted_matrix = [matrix[i] for i in sorted_indices]
    MatrixVisualizer.display_grid(sorted_matrix)

    print("\nОперация сортировки - упорядоченная выборка (по возрастанию):")
    sorted_indices = processor.get_sorted_indices(False)
    sorted_matrix = [matrix[i] for i in sorted_indices]
    MatrixVisualizer.display_grid(sorted_matrix)

if __name__ == "__main__":
    main()