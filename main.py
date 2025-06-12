# Вариант 13
# Кодер: Уравнение (строится по проверочной матрице)
# Декодер: Лидер смежного класса
# Матрицы хранятся в виде векторов (списки). Комбинации хранятся аналогичным образом. Анализ разрешенных комбинаций
# Размер длины информационного слова: 5

G = [  # Порождающая матрица
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
]


class Coder:

    def __init__(self, generator_matrix):

        self.info_bits_count = len(generator_matrix)  # Количество информационных битов (размерность единичный матрицы)
        self.check_matrix = self.generate_check_matrix(generator_matrix)  # Проверочная матрица
        self.code_distance = self.calculate_code_distance(self.info_bits_count)
        pass

    # Создание проверочной матрицы из порождающей
    def generate_check_matrix(self, matrix):

        check_matrix = []  # Проверочная матрица

        for index, string in enumerate(matrix):
            matrix[index] = string[self.info_bits_count :]

        # Транспонируем матрицу Q
        for column_index in range(len(matrix[0])):
            temp_row = []  # Временный список для хранения транспонированной строки
            for row_index in range(len(matrix)):
                temp_row.append(matrix[row_index][column_index])

            check_matrix.append(temp_row)

        # Добавляем единичную матрицу в конец проверочной матрицы
        for row_index_check_matrix in range(len(check_matrix)):
            zero_row = [0] * len(check_matrix)  # Создаем строку из нулей
            zero_row[row_index_check_matrix] = 1
            check_matrix[row_index_check_matrix] += zero_row

        return check_matrix

    # Определение истинного кодового расстояния
    def calculate_code_distance(self):

        combinations = []

        while len(combinations) < 2**5:
            array = list(bin(len(combinations))[2:])
            element = list(map(lambda block: int(block), array))
            combinations.append([0] * (self.info_bits_count - len(element)) + element)


def main(info_bits_count):
    coder = Coder(G)
    pass


if __name__ == "__main__":
    main(5)
