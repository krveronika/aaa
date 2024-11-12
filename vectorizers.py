from numpy import log


class SparceMatrix:
    def __init__(self):
        """ключ - tuple(irow, icol), значение - число повторений"""
        self.data = dict()

    def update(self, ir, ic):
        self.data.setdefault((ir, ic), 0)
        self.data[(ir, ic)] += 1

    def to_array(self) -> list[list[str]]:
        """Преобразует разреженную матрицу в плотную"""
        max_row = self.get_count_rows()
        max_col = self.get_count_cols()
        dense_matrix = [[0] * max_col for _ in range(max_row)]

        for (row, col), value in self.data.items():
            dense_matrix[row][col] = value
        return dense_matrix

    def get_count_rows(self) -> int:
        """Кол-во строк в dense"""
        return max(row for row, _ in self.data.keys()) + 1

    def get_count_cols(self) -> int:
        """Кол-во столбцов в dense"""
        return max(col for _, col in self.data.keys()) + 1


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


class TfidfTransformer:
    """
    Задание 4
    """

    @staticmethod
    def tf_transform(sparse_coo_matrix: SparceMatrix) -> SparceMatrix:
        """
        Расчет term frequency (задание 2)
        """
        tfs = SparceMatrix()
        sum_words = dict()
        for (row, col), value in sparse_coo_matrix.data.items():
            sum_words.setdefault(row, 0)
            sum_words[row] += value

        for (row, col), value in sparse_coo_matrix.data.items():
            tfs.data[(row, col)] = round(value / sum_words[row], 3)
        return tfs

    @staticmethod
    def idf_transform(sparse_coo_matrix: SparceMatrix) -> list[float]:
        """
        Расчет inverse document-frequency (задание 3)
        """
        doc_count = sparse_coo_matrix.get_count_rows()
        words_count = sparse_coo_matrix.get_count_cols()
        doc_count_pl_1 = 1 + doc_count
        sum_doc_words = {}
        for _, col in sparse_coo_matrix.data.keys():
            sum_doc_words.setdefault(col, 1)
            sum_doc_words[col] += 1
        idf = [
            round(1 + log(doc_count_pl_1 / sum_doc_words[i]), 3)
            for i in range(words_count)
        ]
        return idf

    def fit_transform(self, sparse_coo_matrix: SparceMatrix) -> SparceMatrix:
        tfidf = SparceMatrix()
        tf_matrix: SparceMatrix = self.tf_transform(sparse_coo_matrix)
        idf_values: list[float] = self.idf_transform(sparse_coo_matrix)

        for (row, col), tf in tf_matrix.data.items():
            tfidf.data[(row, col)] = round(tf * idf_values[col], 3)
        self._sparse_matrix = tfidf
        return self._sparse_matrix


class TfidfVectorizer(CountVectorizer):
    """
    Задание 5
    """

    def __init__(self, splitter: str = " ", is_lower: bool = True):
        super().__init__(splitter, is_lower)
        self.tfidf_transformer = TfidfTransformer()

    def fit_transform(self, X):
        count_matrix = super().fit_transform(X)
        return self.tfidf_transformer.fit_transform(count_matrix)


if __name__ == "__main__":
    corpus = [
        "Crock Pot Pasta Never boil pasta again",
        "Pasta Pomodoro Fresh ingredients Parmesan to taste",
    ]

    count_vectorizer = CountVectorizer()
    print(count_vectorizer.fit_transform(corpus).to_array())
    print(count_vectorizer.get_feature_names())

    tfidf_vectorizer = TfidfVectorizer()
    print(tfidf_vectorizer.fit_transform(corpus).to_array())
    print(tfidf_vectorizer.get_feature_names())
