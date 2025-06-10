class MatrixVisualizer:
    @staticmethod
    def display_grid(grid_data):
        for row in grid_data:
            print("".join(str(cell) for cell in row))