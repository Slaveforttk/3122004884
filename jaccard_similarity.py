# _*_ coding : utf-8 _*_
# @Time : 2024/3/8 14:19
# @Author : Slave
# @File : jaccard_similarity
# @Project : 3122004884

# jaccard 相似度实现
import os
import re
import string

import jieba
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


# 停用词处理 -- 不允许读写其他文件，中文停用词不做处理
# def remove_stopwords_ch(text):
#     stop_words = set(jieba.analyse.STOP_WORDS)
#     words = text.split
#     words = [word for word in words if word not in stop_words]
#     return ' '.join(words)


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


# 综合使用


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
    return text


def jaccard_similarity(text1, text2):
    words_text1 = set(text1.split())
    words_text2 = set(text2.split())
    intersection = words_text1.intersection(words_text2)
    union = words_text1.union(words_text2)
    return len(intersection) / len(union)


def main_jaccard(file_path1, file_path2, output_file):
    text1 = preprocess_text(file_path1)
    text2 = preprocess_text(file_path2)

    similarity = jaccard_similarity(text1, text2)
    similarity = round(similarity, 2)

    with open(output_file, 'w') as f:
        f.write('jaccard_similarity is ' + str(similarity))
    print(similarity)


# 编写测试函数


def test_jaccard_similarity_en():
    # 创建两个测试文件
    with open('test1.txt', 'w', encoding='utf-8') as f:
        f.write('This is python test')
    with open('test2.txt', 'w', encoding='utf-8') as f:
        f.write('This is Java test')

    # 计算两个文件的Jaccard相似度并将结果写入一个新的文件
    main_jaccard('test1.txt', 'test2.txt', 'output.txt')

    # 读取输出文件中的相似度
    # with open('output.txt', 'r') as f:
    #   similarity = float(f.read())

    # 删除测试文件和输出文件
    os.remove('test1.txt')
    os.remove('test2.txt')
    os.remove('output.txt')


test_jaccard_similarity_en()
