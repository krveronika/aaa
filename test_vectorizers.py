from vectorizers import CountVectorizer, TfidfTransformer, TfidfVectorizer


corpus = [
    "Crock Pot Pasta Never boil pasta again",
    "Pasta Pomodoro Fresh ingredients Parmesan to taste",
]


class TestCountVectorizer:
    expected_count_vectorizer = [
        [1, 1, 2, 1, 1, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1],
    ]
    expected_features = [
        "crock",
        "pot",
        "pasta",
        "never",
        "boil",
        "again",
        "pomodoro",
        "fresh",
        "ingredients",
        "parmesan",
        "to",
        "taste",
    ]

    def test_cv(self):
        count_vectorizer = CountVectorizer()
        assert (
            count_vectorizer.fit_transform(corpus).to_array()
            == self.expected_count_vectorizer
        )
        assert count_vectorizer.get_feature_names() == self.expected_features


class TestTfidfTransformer:
    expected_tf = [
        [0.143, 0.143, 0.286, 0.143, 0.143, 0.143, 0, 0, 0, 0, 0, 0],
        [0, 0, 0.143, 0, 0, 0, 0.143, 0.143, 0.143, 0.143, 0.143, 0.143],
    ]
    expected_idf = [
        1.405,
        1.405,
        1.0,
        1.405,
        1.405,
        1.405,
        1.405,
        1.405,
        1.405,
        1.405,
        1.405,
        1.405,
    ]
    expected_tfidf = [
        [0.201, 0.201, 0.286, 0.201, 0.201, 0.201, 0, 0, 0, 0, 0, 0],
        [0, 0, 0.143, 0, 0, 0, 0.201, 0.201, 0.201, 0.201, 0.201, 0.201],
    ]

    def test_tfidf_transform(self):
        count_vectorizer = CountVectorizer()
        tfidf_transformer = TfidfTransformer()
        assert (
            tfidf_transformer.tf_transform(
                count_vectorizer.fit_transform(corpus)
            ).to_array()
            == self.expected_tf
        )
        assert (
            tfidf_transformer.idf_transform(count_vectorizer.fit_transform(corpus))
            == self.expected_idf
        )
        assert (
            tfidf_transformer.fit_transform(
                count_vectorizer.fit_transform(corpus)
            ).to_array()
            == self.expected_tfidf
        )


class TestTfidfVectorizer:
    expected_tfidf = [
        [0.201, 0.201, 0.286, 0.201, 0.201, 0.201, 0, 0, 0, 0, 0, 0],
        [0, 0, 0.143, 0, 0, 0, 0.201, 0.201, 0.201, 0.201, 0.201, 0.201],
    ]

    def test_tfidf_transform(self):
        tfidf_vectorizer = TfidfVectorizer()
        assert tfidf_vectorizer.fit_transform(corpus).to_array() == self.expected_tfidf
        assert (
            tfidf_vectorizer.get_feature_names()
            == TestCountVectorizer.expected_features
        )
