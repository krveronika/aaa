class SparceMatrix:
    def __init__(self):
        """ключ - tuple(irow, icol), значение - число повторений"""
        self.data = dict()

    def update(self, ir, ic):
        if (ir, ic) in self.data:
            self.data[(ir, ic)] += 1
        else:
            self.data[(ir, ic)] = 1

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


class TfidfTransformer:
    """
    Задание 4
    """

    @staticmethod
    def tf_transform(sparse_coo_matrix: sparse.spmatrix) -> sparse.spmatrix:
        """
        Расчет term frequency (задание 2)
        """
        sparse_size = sparse_coo_matrix.size
        rows = [0] * sparse_size
        cols = [0] * sparse_size
        tfs = [0] * sparse_size
        sum_words = {}
        for irow, val in zip(sparse_coo_matrix.row, sparse_coo_matrix.data):
            sum_words.setdefault(irow, 0)
            sum_words[irow] += val

        zip_data = zip(
            sparse_coo_matrix.row, sparse_coo_matrix.col, sparse_coo_matrix.data
        )
        for i, (ir, ic, val) in enumerate(zip_data):
            rows[i] = ir
            cols[i] = ic
            tfs[i] = round(val / sum_words[ir], 3)
        return sparse.coo_matrix((tfs, (rows, cols)))

    @staticmethod
    def idf_transform(sparse_coo_matrix: sparse.spmatrix) -> list[float]:
        """
        Расчет inverse document-frequency (задание 3)
        """
        doc_count, words_count = sparse_coo_matrix.shape
        doc_count += 1
        sum_doc_words = {}
        for icol in sparse_coo_matrix.col:
            sum_doc_words.setdefault(icol, 1)
            sum_doc_words[icol] += 1
        idf = [
            round(1 + log(doc_count / sum_doc_words[i]), 3) for i in range(words_count)
        ]
        return idf

    def fit_transform(self, sparse_coo_matrix: sparse.spmatrix) -> sparse.spmatrix:
        sparse_size = sparse_coo_matrix.size
        rows = [0] * sparse_size
        cols = [0] * sparse_size
        tfidf = [0] * sparse_size
        tf_matrix: sparse.spmatrix = self.tf_transform(sparse_coo_matrix)
        idf_values: list[float] = self.idf_transform(sparse_coo_matrix)
        zip_data = zip(tf_matrix.row, tf_matrix.col, tf_matrix.data)
        for i, (irow, icol, tf) in enumerate(zip_data):
            rows[i], cols[i] = irow, icol
            tfidf[i] = round(tf * idf_values[icol], 3)
        self._sparse_matrix = sparse.coo_matrix((tfidf, (rows, cols)))
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
    tfidf_vectorizer = TfidfVectorizer()
    print(tfidf_vectorizer.fit_transform(corpus).toarray())
    print(tfidf_vectorizer.get_feature_names())
