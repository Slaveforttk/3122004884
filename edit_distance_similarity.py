# _*_ coding : utf-8 _*_
# @Time : 2024/3/8 14:19
# @Author : Slave
# @File : jaccard_similarity
# @Project : 3122004884
import cProfile
import multiprocessing
import re
import jieba
import string
import sys
from nltk import edit_distance
from langdetect import detect
from nltk.corpus import stopwords as nltk_stopwords

from main import cosine_similarity_sklearn


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
    return ' '.join(text.split())
    # return text


def edit_distance_similarity(text1, text2):
    # 计算编辑距离
    edit_dist = edit_distance(text1, text2)

    # 计算相似度
    similarity = 1 - (edit_dist / max(len(text1), len(text2)))

    return round(similarity, 2)


def worker(text1, text2, output_file):
    similarity = edit_distance_similarity(text1, text2)

    with open(output_file, 'w') as f:
        f.write('edit_distance_similarity is:' + str(similarity))


def main_edit_distance():
    file_paths1 = sys.argv[1::3]  # 第一个输入文件的路径在命令行参数的第1个位置，然后每隔3个位置就是一个输入文件的路径
    file_paths2 = sys.argv[2::3]  # 第二个输入文件的路径在命令行参数的第2个位置，然后每隔3个位置就是一个输入文件的路径
    output_files = sys.argv[3::3]  # 输出文件的路径在命令行参数的第3个位置，然后每隔3个位置就是一个输出文件的路径

    with multiprocessing.Pool(min(len(file_paths1), multiprocessing.cpu_count())) as pool:
        texts1 = pool.map(preprocess_text, file_paths1)
        texts2 = pool.map(preprocess_text, file_paths2)
        pool.starmap(worker, zip(texts1, texts2, output_files))


if __name__ == '__main__':
    main_edit_distance()
    # profiler = cProfile.Profile()
    # profiler.runcall(main)
    # profiler.print_stats()
