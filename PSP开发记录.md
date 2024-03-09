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
  
  def preprocess_text(file_path, language):
      with open(file_path, 'r', encoding='utf-8') as f:
          text = f.read()
      if language == 'zh-cn':
          text = remove_punctuation_ch(text)
          text = segment_words_ch(text)
      elif language == 'en':
          text = remove_punctuation_en(text)
          text = to_lower_en(text)
          text = remove_stopwords_en(text)
      return text
  ```



