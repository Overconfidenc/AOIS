import random

class MatrixGenerator:
    @staticmethod
    def create_binary_grid(row_count=16, column_count=16, fill_probability=0.5):
        grid = [[0 for _ in range(column_count)] for _ in range(row_count)]

        for i in range(row_count):
            for j in range(column_count):
                if (i + j) % row_count == i:
                    grid[i][j] = 1 if random.random() < fill_probability else 0
                else:
                    grid[i][j] = 1 if random.random() < fill_probability / 3 else 0

        for j in range(column_count):
            if all(grid[i][j] == 0 for i in range(row_count)):
                random_row = random.randint(0, row_count - 1)
                grid[random_row][j] = 1

        return grid