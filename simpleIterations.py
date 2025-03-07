import random

def is_diagonally_dominant(A):
    n = len(A)
    for i in range(n):
        diag = abs(A[i][i])
        off_diag = sum(abs(A[i][j]) for j in range(n) if j != i)
        if diag < off_diag:
            return False
    return True


def find_diagonally_dominant_order(A, b):
    n = len(A)
    def backtrack(i, used, order):
        if i == n:
            return order
        for r in range(n):
            if not used[r]:
                row_sum = sum(abs(A[r][j]) for j in range(n))
                if 2 * abs(A[r][i]) >= row_sum:
                    used[r] = True
                    order.append(r)
                    result = backtrack(i + 1, used, order)
                    if result is not None:
                        return result
                    order.pop()
                    used[r] = False
        return None

    used = [False] * n
    order = backtrack(0, used, [])
    if order is None:
        return None, None

    new_A = [A[r] for r in order]
    new_b = [b[r] for r in order]
    return new_A, new_b



def matrix_infinity_norm(A):
    n = len(A)
    return max(sum(abs(A[i][j]) for j in range(n)) for i in range(n))


def simple_iteration_method(A, b, eps, max_iterations=1000):
    n = len(A)
    x_old = [0.0] * n
    iterations = 0

    while iterations < max_iterations:
        x_new = [0.0] * n
        for i in range(n):
            s = 0.0
            for j in range(n):
                if j != i:
                    s += A[i][j] * x_old[j]
            x_new[i] = (b[i] - s) / A[i][i]
        error_vector = [abs(x_new[i] - x_old[i]) for i in range(n)]
        iterations += 1
        if max(error_vector) < eps:
            return x_new, iterations, error_vector
        x_old = x_new
    print("Максимальное число итераций достигнуто.")
    return x_new, iterations, error_vector


def generate_random_diagonally_dominant_matrix(n, min_val=-10, max_val=10):
    A = []
    for i in range(n):
        row = []
        for j in range(n):
            if i == j:
                row.append(0.0)
            else:
                row.append(random.uniform(min_val, max_val))
        off_diag_sum = sum(abs(x) for j, x in enumerate(row) if j != i)
        diag = off_diag_sum + random.uniform(1, 10)
        row[i] = diag
        A.append(row)
    return A


def generate_random_vector(n, min_val=-10, max_val=10):
    return [random.uniform(min_val, max_val) for _ in range(n)]


def generate_random_matrix(n, min_val=-10, max_val=10):
    A = []
    for i in range(n):
        row = [random.uniform(min_val, max_val) for _ in range(n)]
        A.append(row)
    return A


def main():
    print("Решение СЛАУ методом простых итераций.")
    print("Выберите способ ввода данных:")
    print("1 – с клавиатуры")
    print("2 – из файла")
    print("3 – генерация случайной диагонально преобладающей матрицы")
    print("4 – генерация случайной матрицы (любая)")
    choice = input("Ваш выбор (1, 2, 3 или 4): ").strip()

    if choice == "1":
        try:
            n = int(input("Введите размерность матрицы n (<=20): "))
        except ValueError:
            print("Ошибка ввода числа n.")
            return
        if n > 20 or n < 1:
            print("Размерность матрицы должна быть от 1 до 20.")
            return
        A = []
        print("Введите коэффициенты матрицы A построчно, разделяя пробелами:")
        for i in range(n):
            row_str = input(f"Строка {i + 1}: ")
            try:
                row = list(map(float, row_str.split()))
            except ValueError:
                print("Ошибка преобразования коэффициентов в числа.")
                return
            if len(row) != n:
                print("Неверное количество коэффициентов в строке.")
                return
            A.append(row)
        b_str = input("Введите вектор правых частей b (числа через пробел): ")
        try:
            b = list(map(float, b_str.split()))
        except ValueError:
            print("Ошибка преобразования коэффициентов в числа.")
            return
        if len(b) != n:
            print("Неверное количество коэффициентов в векторе b.")
            return
        try:
            eps = float(input("Введите требуемую точность eps: "))
        except ValueError:
            print("Ошибка ввода точности.")
            return

    elif choice == "2":
        filename = input("Введите имя файла: ").strip()
        try:
            with open(filename, "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f if line.strip()]
        except Exception as e:
            print(f"Ошибка чтения файла: {e}")
            return
        try:
            n = int(lines[0])
        except ValueError:
            print("Ошибка преобразования размерности матрицы.")
            return
        if n > 20 or n < 1:
            print("Размерность матрицы должна быть от 1 до 20.")
            return
        if len(lines) < n + 3:
            print("Недостаточно данных в файле.")
            return
        A = []
        for i in range(n):
            try:
                row = list(map(float, lines[i + 1].split()))
            except ValueError:
                print("Ошибка преобразования коэффициентов в числа.")
                return
            if len(row) != n:
                print("Неверное количество коэффициентов в строке матрицы файла.")
                return
            A.append(row)
        try:
            b = list(map(float, lines[n + 1].split()))
        except ValueError:
            print("Ошибка преобразования коэффициентов в числа для вектора b.")
            return
        if len(b) != n:
            print("Неверное количество коэффициентов в векторе b файла.")
            return
        try:
            eps = float(lines[n + 2])
        except ValueError:
            print("Ошибка ввода точности eps.")
            return

    elif choice == "3":
        try:
            n = int(input("Введите размерность матрицы n (<=20): "))
        except ValueError:
            print("Ошибка ввода числа n.")
            return
        if n > 20 or n < 1:
            print("Размерность матрицы должна быть от 1 до 20.")
            return
        try:
            eps = float(input("Введите требуемую точность eps: "))
        except ValueError:
            print("Ошибка ввода точности.")
            return

        A = generate_random_diagonally_dominant_matrix(n)
        b = generate_random_vector(n)
        print("\nСгенерированная матрица A (диагонально преобладающая):")
        for row in A:
            print("  " + " ".join(f"{elem:.3f}" for elem in row))
        print("\nСгенерированный вектор b:")
        print("  " + " ".join(f"{elem:.3f}" for elem in b))

    elif choice == "4":
        try:
            n = int(input("Введите размерность матрицы n (<=20): "))
        except ValueError:
            print("Ошибка ввода числа n.")
            return
        if n > 20 or n < 1:
            print("Размерность матрицы должна быть от 1 до 20.")
            return
        try:
            eps = float(input("Введите требуемую точность eps: "))
        except ValueError:
            print("Ошибка ввода точности.")
            return

        A = generate_random_matrix(n)
        b = generate_random_vector(n)
        print("\nСгенерированная матрица A (произвольная):")
        for row in A:
            print("  " + " ".join(f"{elem:.3f}" for elem in row))
        print("\nСгенерированный вектор b:")
        print("  " + " ".join(f"{elem:.3f}" for elem in b))

    else:
        print("Неверный выбор ввода.")
        return

    print("\nПроверка диагонального преобладания матрицы A...")
    if not is_diagonally_dominant(A):
        print("Исходная матрица не обладает диагональным преобладанием.")
        print("Пытаемся переставить строки для обеспечения диагонального преобладания...")
        new_A, new_b = find_diagonally_dominant_order(A, b)
        if new_A is None:
            print("Не удалось добиться диагонального преобладания перестановкой строк/столбцов.")
            return
        else:
            print("Перестановка строк выполнена. Новая матрица имеет диагональное преобладание.")
            A, b = new_A, new_b
    else:
        print("Матрица обладает диагональным преобладанием.")

    normA = matrix_infinity_norm(A)
    print(f"\nНорма матрицы A (∞-норма): {normA}")

    print("\nВыполняется метод простых итераций...")
    x, iterations, error_vector = simple_iteration_method(A, b, eps)

    print("\nНайденное решение:")
    for i, xi in enumerate(x):
        print(f"  x[{i + 1}] = {xi}")

    print(f"\nКоличество итераций: {iterations}")

    print("\nВектор погрешностей |x_i^(k) - x_i^(k-1)|:")
    for i, err in enumerate(error_vector):
        print(f"  Компонента {i + 1}: {err}")


if __name__ == "__main__":
    main()
