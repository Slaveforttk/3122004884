# _*_ coding : utf-8 _*_
# @Time : 2024/3/8 14:19
# @Author : Slave
# @File : jaccard_similarity
# @Project : 3122004884

# import cProfile
import multiprocessing
import os
import re
import jieba
import string
import sys
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from langdetect import detect
from nltk.corpus import stopwords as nltk_stopwords


# 净化文本内容

# 中文净化

# 移除标点
def remove_punctuation_ch(text):
    return re.sub(r'[^\w\s]', '', text)


# 分词处理
def segment_words_ch(text):
    return ' '.join(jieba.cut(text))


# 英文净化
# 转换大小写
def to_lower_en(text):
    return text.lower()


# 移除标点符号
def remove_punctuation_en(text):
    return text.translate(str.maketrans('', '', string.punctuation))


# 移除停用词
def remove_stopwords_en(text):
    stop_words = set(nltk_stopwords.words('english'))
    words = text.split()
    words = [word for word in words if word not in stop_words]
    return ' '.join(words)


def preprocess_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    language = detect(text)
    if language == 'zh-cn':
        text = remove_punctuation_ch(text)
        text = segment_words_ch(text)
    elif language == 'en':
        text = remove_punctuation_en(text)
        text = to_lower_en(text)
        text = remove_stopwords_en(text)
    return Counter(text.split())


# def preprocess_text(text):
#     language = detect(text)
#     if language == 'zh-cn':
#         text = remove_punctuation_ch(text)
#         text = segment_words_ch(text)
#     elif language == 'en':
#         text = remove_punctuation_en(text)
#         text = to_lower_en(text)
#         text = remove_stopwords_en(text)
#     return Counter(text.split())


def cosine_similarity_sklearn(vec1, vec2):
    # 将Counter对象转换为字符串
    text1 = ' '.join(['{} {}'.format(k, v) for k, v in vec1.items()])
    text2 = ' '.join(['{} {}'.format(k, v) for k, v in vec2.items()])

    # 创建CountVectorizer对象
    vectorizer = CountVectorizer()

    # 使用CountVectorizer对象将文本转换为向量
    x = vectorizer.fit_transform([text1, text2])

    # 计算余弦相似度
    similarity = cosine_similarity(x[0], x[1])[0][0]
    similarity = round(similarity, 2)
    print(similarity)
    return similarity


def worker(vec1, vec2, output_file):
    similarity = cosine_similarity_sklearn(vec1, vec2)

    with open(output_file, 'w') as f:
        f.write('cosine_similarity is:' + str(similarity))


def main_cosine():
    file_paths1 = [os.path.normpath(path) for path in sys.argv[1::3]]
    file_paths2 = [os.path.normpath(path) for path in sys.argv[2::3]]
    output_files = [os.path.normpath(path) for path in sys.argv[3::3]]

    # 检查文件路径是否存在
    for file_path in file_paths1 + file_paths2:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件 {file_path} 不存在")

    with multiprocessing.Pool(min(len(file_paths1), multiprocessing.cpu_count())) as pool:
        texts1 = pool.map(preprocess_text, file_paths1)
        texts2 = pool.map(preprocess_text, file_paths2)
        pool.starmap(worker, zip(texts1, texts2, output_files))


if __name__ == '__main__':
    main_cosine()
    # profiler = cProfile.Profile()
    # profiler.runcall(main_cosine)
    # profiler.print_stats()
