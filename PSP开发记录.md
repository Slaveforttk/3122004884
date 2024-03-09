# *PSP*

> *为熟悉软件开发流程，个人项目使用文档记录*

### *计划*

初步计划使用熟悉的语言进行编程，开始使用C语言进行构思，调试无果，改用面向对象语言Python进行开发

### *开发*

#### *需求分析*

- 功能需求：用户需求为比较两个文档的相似度，提供接口接受两个待处理文件，传回一个结果目标文件

- 开发环境：确定为python3进行开发，使用版本为python3.10.0
- 产品功能：默认一种方法，也可以可以传入更多参数来使用多种方法

### *设计文档*

#### *Opening*

项目旨在对给定两个文档进行对比得出相似度

#### *Challenge*

初次使用Python编程，不够熟练，文档的处理，相似度的比较，对不同语言文档的分析

#### *Action*

查找Python第三库来寻找合适的方法

首先我们需要对接收的文本进行处理提高结果准确性

##### *文本处理*

搜寻资料，对文本处理有以下步骤

1. 净化文本—去除标点空格等
2. 停用词处理—去除大多无用的词语（往往需要引入停用词表，需求不允许额外处理文件就不进行处理）
3. 分词—将单词分隔开

##### 接口设计

使用代码实现预设操作——仅仅考虑传入英文和中文文档的情况

###### 针对中文文档

1. 净化文本

   `re`库是Python的正则表达式库，使用它来移除文本中的标点符号，使用正则表达式`[^\w\s]`来匹配所有的标点符号，然后使用`re.sub`函数将它们替换为无

   ```python
   import re
   
   def remove_punctuation_ch(text):
       return re.sub(r'[^\w\s]', '', text)
   ```

2. 停用词处理--需求不允许读写其他文件，此处停用词处理仅供参考

   ```python
   import jieba
   
   def remove_stopwords_ch(text):
       stop_words = set(jieba.analyse.STOP_WORDS)
       words = text.split
       words = [word for word in words if word not in stop_words]
       return ' '.join(words)
   ```

3. 分词处理

   `jieba`库是一个用于中文分词的Python库，这个函数的作用是对文本进行分词。使用`jieba.cut`函数来进行分词，然后使用`' '.join`来将分词后的结果连接成一个字符串

   ```python
   import jieba
   
   def segment_words_ch(text):
       return ' '.join(jieba.cut(text))
   ```

###### 针对英文文档

1. 转换小写

   ```python
   def to_lower(text):
       return text.lower()
   ```

2. 净化文本

   ```python
   import string
   
   def remove_punctuation_en(text):
       return text.translate(str.maketrans('', '', string.punctuation))
   ```

3. 移除停用词

   函数的作用是移除文本中的英文停用词。我们使用`nltk.corpus.stopwords.words('english')`来获取英文的停用词列表，然后移除他们

   ```py
   from nltk.corpus import stopwords as nltk_stopwords
   
   def remove_stopwords_en(text):
       stop_words = set(nltk_stopwords.words('english'))
       words = text.split()
       words = [word for word in words if word not in stop_words]
       return ' '.join(words)
   ```

###### 对两种处理进行区分并相应处理

- 预处理函数的构建

  函数会对传入的文档以及其语言不同分别处理，调用上述文档处理文件执行操作

  ```py
  from langdetect import detect
  
  def preprocess_text(text):
      language = detect(text)
      if language == 'zh-cn':
          text = remove_punctuation_ch(text)
          text = segment_words_ch(text)
      elif language == 'en':
          text = remove_punctuation_en(text)
          text = to_lower_en(text)
          text = remove_stopwords_en(text)
      return Counter(text.split())
  ```

- 相似度的计算

  三种方法均已实现此处仅给出main默认使用的余弦算法

  ```python
  def cosine_similarity_sklearn(vec1, vec2):
      # 将Counter对象转换为字符串
      text1 = ' '.join(['{} {}'.format(k, v) for k, v in vec1.items()])
      text2 = ' '.join(['{} {}'.format(k, v) for k, v in vec2.items()])
  
      # 创建CountVectorizer对象
      vectorizer = CountVectorizer()
  
      # 使用CountVectorizer对象将文本转换为向量
      X = vectorizer.fit_transform([text1, text2])
  
      # 计算余弦相似度
      similarity = cosine_similarity(X[0], X[1])[0][0]
  
      return round(similarity, 2)
  ```

- 将结果输出保存到目标文件

  ```py
  def worker(vec1, vec2, output_file):
      similarity = cosine_similarity_sklearn(vec1, vec2)
  
      with open(output_file, 'w') as f:
          f.write('cosine_similarity is:' + str(similarity))
  ```

- 接受文件参数以及函数调用入口

  ```py
  def main_cosine(file_path1, file_path2, output_file):
      text1 = preprocess_text(file_path1)
      text2 = preprocess_text(file_path2)
  
      similarity = cosine_similarity_score(text1, text2)
      similarity = round(similarity, 2)
  
      with open(output_file, 'w') as f:
          f.write('cosine_similarity is ' + str(similarity))
      print(similarity)
  ```

##### 接口优化

对于当前代码我们在执行的时候不难发现有许多存在的问题，最主要的问题是无法满足5s完成计算的需求，所以我们来分析程序的运行

通过测试案例：使用命令行来传入

```py
 python cosine_similarity.py .\orig.txt .\orig_0.8_add.txt .\output.txt
```

此处的两个文件有千字

运行函数监测并发图

![](E:\Software-engineering\picture\first_test.png)

不难发现这是进程耗时巨大

开始优化处理

###### 考虑多进程执行

```py
def main():
    file_paths1 = sys.argv[1::3]  # 第一个输入文件的路径在命令行参数的第1个位置，然后每隔3个位置就是一个输入文件的路径
    file_paths2 = sys.argv[2::3]  # 第二个输入文件的路径在命令行参数的第2个位置，然后每隔3个位置就是一个输入文件的路径
    output_files = sys.argv[3::3]  # 输出文件的路径在命令行参数的第3个位置，然后每隔3个位置就是一个输出文件的路径

    with multiprocessing.Pool() as pool:
        texts1 = pool.map(preprocess_text, file_paths1)
        texts2 = pool.map(preprocess_text, file_paths2)
        pool.starmap(worker, zip(texts1, texts2, output_files))
```

优化之后：

![](E:\Software-engineering\picture\second_test.png)

不难发现变快了近一秒

再次尝试优化分析

通过Python的`cProfile`模块生成性能分析报告

```html
ncalls  tottime  percall  cumtime  percall filename:lineno(function)
2       0.000    0.000    3.900    1.950 pool.py:359(map)
3       0.000    0.000    3.901    1.300 pool.py:761(wait)
3       0.000    0.000    3.901    1.300 pool.py:764(get)
6       0.000    0.000    3.905    0.651 threading.py:288(wait)
```

表中列出花销比较大的几个函数，查阅资料：`multiprocessing.Pool().map`函数和`multiprocessing.pool.wait/get`函数以及`threading.wait`函数都是用于并行处理和线程同步的，执行时间主要取决于代码的并行部分的运行时间，没有办法从这些代码入手

那么改变思路，来优化并行任务减少并行任务量

```py
def main():
    file_paths1 = sys.argv[1::3]  # 第一个输入文件的路径在命令行参数的第1个位置，然后每隔3个位置就是一个输入文件的路径
    file_paths2 = sys.argv[2::3]  # 第二个输入文件的路径在命令行参数的第2个位置，然后每隔3个位置就是一个输入文件的路径
    output_files = sys.argv[3::3]  # 输出文件的路径在命令行参数的第3个位置，然后每隔3个位置就是一个输出文件的路径

    with multiprocessing.Pool(min(len(file_paths1), multiprocessing.cpu_count())) as pool:
        texts1 = pool.map(preprocess_text, file_paths1)
        texts2 = pool.map(preprocess_text, file_paths2)
        pool.starmap(worker, zip(texts1, texts2, output_files))
```

通过对比cpu核心数量与文件数量，取其中最小值可以大大减少无用进程

执行代码

![](E:\Software-engineering\picture\last_test.png)

时间减少1秒左右，两次优化将效率提高一倍左右

