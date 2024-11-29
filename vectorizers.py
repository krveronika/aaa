class SparceMatrix:
    def __init__(self):
        """ключ - tuple(irow, icol), значение - число повторений"""
        self.data = dict()

    def update(self, ir, ic) -> None:
        """увеличиваем счетчик"""
        self.data.setdefault((ir, ic), 0)
        self.data[(ir, ic)] += 1

    def to_array(self) -> list[list[str]]:
        """Преобразует разреженную матрицу в плотную"""
        max_row = max(row for row, _ in self.data.keys()) + 1
        max_col = max(col for _, col in self.data.keys()) + 1
        dense_matrix = [[0] * max_col for _ in range(max_row)]

        for (row, col), value in self.data.items():
            dense_matrix[row][col] = value
        return dense_matrix


class CountVectorizer:
    def __init__(self, splitter: str = " ", is_lower: bool = True):
        self.splitter = splitter
        self.is_lower = is_lower
        self._vocab: dict = dict()
        self._sparce_matrix = SparceMatrix()

    def fit_transform(self, X: list[str]) -> SparceMatrix:
        ic = -1
        for ir, text in enumerate(X):
            text = text.lower() if self.is_lower else text
            words = text.split(self.splitter)
            for word in words:
                if word not in self._vocab:
                    ic += 1
                    self._vocab[word] = ic
                self._sparce_matrix.update(ir, self._vocab[word])
        return self._sparce_matrix

    def get_feature_names(self) -> list:
        return list(self._vocab.keys())


if __name__ == "__main__":
    corpus = [
        "Crock Pot Pasta Never boil pasta again",
        "Pasta Pomodoro Fresh ingredients Parmesan to taste",
    ]

    count_vectorizer = CountVectorizer()
    print(count_vectorizer.fit_transform(corpus).to_array())
    print(count_vectorizer.get_feature_names())
