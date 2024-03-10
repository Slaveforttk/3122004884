import unittest
from collections import Counter

from cosine_similarity import remove_punctuation_ch, segment_words_ch, to_lower_en, remove_punctuation_en, \
    remove_stopwords_en, preprocess_text, cosine_similarity_sklearn


class TestCosine(unittest.TestCase):

    def test_remove_punctuation_ch(self):
        self.assertEqual(remove_punctuation_ch("你好，世界！"), "你好世界")

    def test_segment_words_ch(self):
        self.assertEqual(segment_words_ch("你好世界"), "你好 世界")

    def test_to_lower_en(self):
        self.assertEqual(to_lower_en("Hello World!"), "hello world!")

    def test_remove_punctuation_en(self):
        self.assertEqual(remove_punctuation_en("Hello, World!"), "Hello World")

    def test_remove_stopwords_en(self):
        self.assertEqual(remove_stopwords_en("This is a test"), "This test")

    def test_preprocess_text(self):
        self.assertEqual(preprocess_text("你好，世界！"), Counter(["你好", "世界"]))

    def test_cosine_similarity_sklearn(self):
        vec1 = Counter(["你好", "世界"])
        vec2 = Counter(["你好", "世界"])
        self.assertEqual(cosine_similarity_sklearn(vec1, vec2), 1.0)


if __name__ == '__main__':
    unittest.main()
