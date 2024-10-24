import scipy.sparse as sparse


class CountVectorizer:
    def __init__(self, splitter=" ", is_lower=True):
        self.splitter = splitter
        self.is_lower = is_lower

    def _create_vocab(self, X):
        """
        Создание отсортированного по ключу словаря. Ключ - уникальное слово из X
        """
        set_words = set()
        for text in X:
            text = text.lower() if self.is_lower else text
            set_words.update(text.split(self.splitter))
        sorted_words = sorted(list(set_words))
        self._vocab: dict = {w: i for i, w in enumerate(sorted_words)}

    def fit_transform(self, X):
        self._create_vocab(X)
        rows = []
        cols = []
        count_word = []

        for ir, text in enumerate(X):
            text = text.lower() if self.is_lower else text
            set_words = set(text.split(self.splitter))
            rows = rows + [ir] * len(set_words)
            for word in set(text.split(self.splitter)):
                cols.append(self._vocab[word])
                count_word.append(text.count(word))

        self._sparce_matrix = sparse.coo_matrix((count_word, (rows, cols)))
        return self._sparce_matrix

    def get_feature_names(self):
        return self._vocab.keys()


if __name__ == '__main__':
    corpus = [
        "Crock Pot Pasta Never boil pasta again",
        "Pasta Pomodoro Fresh ingredients Parmesan to taste",
    ]

    count_vectorizer = CountVectorizer()
    print(count_vectorizer.fit_transform(corpus).toarray())
    print(count_vectorizer.get_feature_names())
