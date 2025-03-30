class HashMixin:
    def __hash__(self):
        # Простейшая хэш‑функция для матрицы:
        # Вычисляем сумму всех элементов матрицы и прибавляем произведение числа строк на число столбцов.
        # Берем остаток от деления на 10, чтобы упростить возникновение коллизий.
        total = sum(sum(row) for row in self.data)
        return (total + self.rows * self.cols) % 10

class Matrix(HashMixin):
    _cache = {}  # Глобальный кэш для результатов матричного умножения

    def __init__(self, data):
        if not data or not isinstance(data, list):
            raise ValueError("Данные матрицы должны быть непустым списком списков.")
        # Проверка, что все строки имеют одинаковую длину
        row_length = len(data[0])
        for row in data:
            if len(row) != row_length:
                raise ValueError("Все строки матрицы должны иметь одинаковую длину.")
        self.data = data
        self.rows = len(data)
        self.cols = row_length

    def __add__(self, other):
        if not isinstance(other, Matrix):
            raise ValueError("Можно складывать только с другим объектом Matrix.")
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Размерности матриц должны совпадать для сложения.")
        result = [
            [self.data[i][j] + other.data[i][j] for j in range(self.cols)]
            for i in range(self.rows)
        ]
        return Matrix(result)

    def __mul__(self, other):
        """Покомпонентное умножение матриц"""
        if not isinstance(other, Matrix):
            raise ValueError("Можно умножать только с другим объектом Matrix.")
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Размерности матриц должны совпадать для покомпонентного умножения.")
        result = [
            [self.data[i][j] * other.data[i][j] for j in range(self.cols)]
            for i in range(self.rows)
        ]
        return Matrix(result)

    def __matmul__(self, other):
        """Матричное умножение с кэшированием по хэш‑функции.
        
        Ключ кэша формируется как (hash(self), hash(other)).
        Если разные матрицы дают одинаковый hash, то может возникнуть ситуация,
        когда результат умножения возвращается из кэша, даже если операнды различны.
        """
        if not isinstance(other, Matrix):
            raise ValueError("Можно выполнять матричное умножение только с другим объектом Matrix.")
        if self.cols != other.rows:
            raise ValueError("Число столбцов первой матрицы должно быть равно числу строк второй матрицы для матричного умножения.")
        key = (hash(self), hash(other))
        if key in Matrix._cache:
            return Matrix._cache[key]
        result = []
        for i in range(self.rows):
            row_result = []
            for j in range(other.cols):
                s = sum(self.data[i][k] * other.data[k][j] for k in range(self.cols))
                row_result.append(s)
            result.append(row_result)
        prod = Matrix(result)
        Matrix._cache[key] = prod
        return prod

    def matmul_nocache(self, other):
        """Матричное умножение без кэширования (для получения истинного результата)"""
        if not isinstance(other, Matrix):
            raise ValueError("Можно выполнять матричное умножение только с другим объектом Matrix.")
        if self.cols != other.rows:
            raise ValueError("Число столбцов первой матрицы должно быть равно числу строк второй матрицы для матричного умножения.")
        result = []
        for i in range(self.rows):
            row_result = []
            for j in range(other.cols):
                s = sum(self.data[i][k] * other.data[k][j] for k in range(self.cols))
                row_result.append(s)
            result.append(row_result)
        return Matrix(result)

    def __str__(self):
        # Форматированный вывод матрицы
        return "\n".join(["\t".join(map(str, row)) for row in self.data])
