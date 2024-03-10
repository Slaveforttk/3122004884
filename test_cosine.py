import unittest
from collections import Counter

from main import remove_punctuation_ch, segment_words_ch, to_lower_en, remove_punctuation_en, \
    remove_stopwords_en, preprocess_text, cosine_similarity_sklearn, worker


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

    # 第一次修改可能存在的问题测试
    def test_file_not_found(self):
        with self.assertRaises(ValueError):
            preprocess_text('')

    def test_file_not_writable(self):
        with self.assertRaises(PermissionError):
            worker(Counter(), Counter(), '/non_writable_file.txt')

    def test_invalid_language(self):
        with self.assertRaises(ValueError):
            preprocess_text('Invalid language text')

if __name__ == '__main__':
    unittest.main()
