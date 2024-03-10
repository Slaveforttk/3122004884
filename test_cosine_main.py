import sys
import unittest
import tempfile
import os
from cosine_similarity import main_cosine


class TestIntegration(unittest.TestCase):

    def setUp(self):
        # 创建一些临时文件
        self.file1_ch = tempfile.NamedTemporaryFile(delete=False)
        self.file2_ch = tempfile.NamedTemporaryFile(delete=False)
        self.file1_en = tempfile.NamedTemporaryFile(delete=False)
        self.file2_en = tempfile.NamedTemporaryFile(delete=False)
        self.output_ch = tempfile.NamedTemporaryFile(delete=False)
        self.output_en = tempfile.NamedTemporaryFile(delete=False)


        # 写入一些测试数据
        self.file1_ch.write('你好，世界！'.encode())
        self.file2_ch.write('你好，Python！'.encode())
        self.file1_en.write('Hello, World!'.encode())
        self.file2_en.write('Hello, Python!'.encode())
        self.file1_ch.close()
        self.file2_ch.close()
        self.file1_en.close()
        self.file2_en.close()

    def tearDown(self):
        # 测试结束后删除临时文件
        self.file1_ch.close()
        self.file2_ch.close()
        self.file1_en.close()
        self.file2_en.close()
        self.output_ch.close()
        self.output_en.close()
        os.unlink(self.file1_ch.name)
        os.unlink(self.file2_ch.name)
        os.unlink(self.file1_en.name)
        os.unlink(self.file2_en.name)
        os.unlink(self.output_ch.name)
        os.unlink(self.output_en.name)

    def test_empty_text(self):
        # 创建一个空的临时文件
        self.file_empty = tempfile.NamedTemporaryFile(delete=False)
        self.file_empty.close()

        # 修改命令行参数
        sys.argv = ['cosine_similarity', self.file_empty.name, self.file_empty.name, self.output_empty.name]

        # 运行函数
        main_cosine()

        # 检查输出文件
        with open(self.output_empty.name, 'r') as f:
            result = f.read()
        self.assertTrue('cosine_similarity is:' in result)

    def test_main_cosine(self):
        # 修改命令行参数
        sys.argv = ['cosine_similarity.py', self.file1_ch.name, self.file2_ch.name, self.output_ch.name]
        # 运行函数
        main_cosine()
        # 检查输出文件
        with open(self.output_ch.name, 'r') as f:
            result = f.read()
        self.assertTrue('cosine_similarity is:' in result)

        # 修改命令行参数
        sys.argv = ['cosine_similarity.py', self.file1_en.name, self.file2_en.name, self.output_en.name]
        # 运行函数
        main_cosine()
        # 检查输出文件
        with open(self.output_en.name, 'r') as f:
            result = f.read()
        self.assertTrue('cosine_similarity is:' in result)


if __name__ == '__main__':
    unittest.main()
