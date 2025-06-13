# Вариант 13
# Кодер: Уравнение (строится по проверочной матрице)
# Декодер: Лидер смежного класса
# Матрицы хранятся в виде векторов (списки). Комбинации хранятся аналогичным образом. Анализ разрешенных комбинаций
# Размер длины информационного слова: 5

from math import floor
from pprint import pprint

# G = [  # Порождающая матрица (выдаёт только d = 2, т.к матрица = склейка из двух единичных)
#     [1, 0, 0, 0, 0, 1, 0, 0, 0, 0],
#     [0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
#     [0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
#     [0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
#     [0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
# ]

G = [
    [1, 0, 0, 0, 0, 1, 1, 0, 1, 0],
    [0, 1, 0, 0, 0, 0, 1, 1, 1, 1],
    [0, 0, 1, 0, 0, 0, 0, 1, 0, 1],
    [0, 0, 0, 1, 0, 1, 0, 1, 1, 0],
    [0, 0, 0, 0, 1, 1, 1, 0, 0, 1],
]


class Coder:

    def __init__(self, generator_matrix):

        self.info_bits_count = len(generator_matrix)  # Количество информационных битов (размерность единичный матрицы)
        self.check_matrix = self.generate_check_matrix(generator_matrix)  # Проверочная матрица
        self.codeword_length = len(self.check_matrix[0])  # Длина закодированного слова
        self.all_info_words = self.generate_all_info_words()  # Генерирует и кодирует все возможные инф.слова
        self.true_distance_value = self.calculate_code_distance()  # Истинное кодовое расстояние
        self.error_correction_capacity = self.calculate_correction_capacity()  # Количество исправляемых ошибок
        self.standard_array = self.build_standard_array()  # Таблица смежных классов

        # Test
        self.decode_by_standard_array(self.all_info_words[5])

    # Создание проверочной матрицы из порождающей
    def generate_check_matrix(self, matrix):

        check_matrix = []  # Проверочная матрица
        q_matrix = [row[self.info_bits_count :] for row in matrix]

        # Транспонируем матрицу Q
        for column_index in range(len(q_matrix[0])):
            temp_row = []  # Временный список для хранения транспонированной строки
            for row_index in range(len(q_matrix)):
                temp_row.append(q_matrix[row_index][column_index])

            check_matrix.append(temp_row)

        # Добавляем единичную матрицу в конец проверочной матрицы
        for row_index_check_matrix in range(len(check_matrix)):
            zero_row = [0] * len(check_matrix)  # Создаем строку из нулей
            zero_row[row_index_check_matrix] = 1
            check_matrix[row_index_check_matrix] += zero_row

        return check_matrix

    # Кодирование слова (кодирование с помощью уравнений)
    def encode_data(self, codeword):

        redundantPart = []

        for row_index in range(len(self.check_matrix)):

            bitsToSum = []

            for column_index in range(self.info_bits_count):
                if self.check_matrix[row_index][column_index] > 0:
                    bitsToSum.append(codeword[column_index])

            redundantPart.append(sum(bitsToSum) % 2)

        return codeword + redundantPart

    # Генерирует все возможные информационные слова + кодирует их
    def generate_all_info_words(self):

        combinations = []

        while len(combinations) < 2**5:
            array = list(bin(len(combinations))[2:])
            element = list(map(lambda block: int(block), array))
            combinations.append(self.encode_data([0] * (self.info_bits_count - len(element)) + element))

        return combinations

    # Определение истинного кодового расстояния O(n^2)
    def calculate_code_distance(self):
        true_code_distance = None

        for first_row_index in range(len(self.all_info_words)):

            first_row_to_compare = self.all_info_words[first_row_index]

            for second_row_index in range(first_row_index + 1, len(self.all_info_words)):

                pairwise_code_distance = 0
                second_row_to_compare = self.all_info_words[second_row_index]

                for index in range(len(self.all_info_words[second_row_index])):

                    if first_row_to_compare[index] != second_row_to_compare[index]:
                        pairwise_code_distance += 1

                if true_code_distance is None or pairwise_code_distance < true_code_distance:
                    true_code_distance = pairwise_code_distance

        return true_code_distance

    # Вычисляет количество исправляемых ошибок t на основе кодового расстояния d
    def calculate_correction_capacity(self):
        return floor((self.true_distance_value - 1) / 2)

    # Построение таблицы смежных классов
    def build_standard_array(self):

        # Каждая строка: сначала вектор ошибки (лидер), потом — смежные вектора
        error_leaders = []

        # 1 Построение вектора ошибки
        for index in range(0, 2**self.codeword_length):
            binary = format(index, f"0{self.codeword_length}b")
            vector = [int(bit) for bit in binary]

            if sum(vector) <= self.error_correction_capacity:
                error_leaders.append([vector])

        # 2 Применение вектора ошибки к кодовым словам
        for position, error_vector in enumerate(error_leaders):
            leader = error_vector[0]

            for encoded_string in self.all_info_words:
                coset_vector = []  # Смежный вектор

                for index in range(len(leader)):
                    xor_result = (leader[index] + encoded_string[index]) % 2

                    coset_vector.append(xor_result)

                error_leaders[position].append(coset_vector)

        return error_leaders

    # Декодер по таблице смежных классов
    def decode_by_standard_array(self, decoded_input):

        # Проверка векторов на схожесть (не использую готовые функции по типу list1 == list2 в целях унификации алгоритмов с С++ версией)
        def are_lists_equal(list1, list2):
            for index in range(len(list1)):
                if list1[index] != list2[index]:
                    return False

            return True

        for coset_index, coset_table in enumerate(self.standard_array):
            for word_idx in range(1, len(coset_table)):
                if sum(coset_table[word_idx]) == sum(decoded_input):
                    if are_lists_equal(coset_table[word_idx], decoded_input) == True:
                        error_vector = coset_table[0]
                        decoded_word = []  # Декодированная комбинация

                        print(f"Combination: {decoded_input}")
                        print(f"ErrorVector: {error_vector}\n")

                        for index in range(len(decoded_input)):
                            decoded_word.append((decoded_input[index] + error_vector[index]) % 2)

                        print(f"Декодированная комбинация: {decoded_word}\n")


def main(info_bits_count):
    coder = Coder(G)
    pass


if __name__ == "__main__":
    main(5)
