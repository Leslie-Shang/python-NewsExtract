import math
import heapq
from itertools import product
import string
import nltk
from nltk.tokenize import WordPunctTokenizer #nltk中的句子分割器
from nltk.corpus import stopwords #nltk中的停用词库

class TextRank(object):
    def init (self,filename,d,min,n):
        #后两个参数为可变参数，可调参优化算法
        self.filename = filename #初始化需要读取的文本的Path
        self.d = d #初始化阻尼系数
        self.min = min #初始化判断是否继续迭代的误差最小值
        self.n = n #摘要所需要的句子数

#读取文本内容
    def FileRead(self):
        f = open(self.filename,encoding='UTF-8')
        text = f.read()
        return text

#进行句子分割
    def SentenceToken(self,text):
        sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')	# 句子分割器
        sentences = sent_tokenizer.tokenize(text)
        return sentences

#去除标点符号和非字母字符
    def CleanSent(self,sentences):
        delEstr = string.punctuation + string.digits
        identify = str.maketrans('', '', delEstr)	# 转换字符
        Cleansentences = []
        for sentence in sentences:
            sentence = sentence.lower()
            Cleansentence = sentence.translate(identify)	# 删除非字母字符和标点符号
            Cleansentences.append(Cleansentence)
        return Cleansentences

#进行分词并去停用词
    def WordTokenpro(self,sentence):
        #stopwordlist = set(stopwords.words('english'))
        # 在很多新闻中去掉了nltk停用词则公式中分母可能会为0
        #如果在专业性的英文中则可以选用
        stopwordlist = ['is', 'am', 'are', 'a', 'an', 'the']
        Words = nltk.word_tokenize(sentence)
        Words = [i for i in Words if i not in stopwordlist]
        return Words

#计算两个句子的相似度
    def Sentsimilarity(self, sent1, sent2):
        count = 0
        for word in sent1:
            if word in sent2:
                count = count + 1
        return (count / math.log(len(sent1))*math.log(len(sent2)))

#创建相似度矩阵
    def SimilarMatrix(self,sentences):
        N = len(sentences)
        Matrix = [[0.0 for _ in range(N)]for _ in range(N)] #创建N X N的浮点数列表
        for i,j in product(range(N),repeat=2):
            if(i != j):
                Matrix[i][j] = self.Sentsimilarity(sentences[i],sentences[j])
            return Matrix

#TextRank公式计算
    def Culculate(self,Matrix,scores,i):
        Sump = 0.0
        for j in range(len(Matrix)):
            fraction = 0.0
            denominator = 0.0
            # 先计算分子
            fraction = Matrix[j][i]*scores[j]
            # 计算分母
            for k in range(len(Matrix)):
                denominator += Matrix[j][k]
            Sump += fraction / denominator
        Sum = (1-self.d) + self.d*Sump
        return Sum

#判断是否需要继续迭代
    def Different(self,scores,prevent_scores):
        flag = False
        for i in range(len(scores)):
            if(math.fabs(scores[i]-prevent_scores[i]) >= self.min):
                flag = True
                break
        return flag

#迭代计算每个句子的分数
    def Sentscore(self,Matrix):
        scores = [1.0 for _ in range(len(Matrix))]
        prevent_scores = [0.0 for _ in range(len(Matrix))]
        while self.Different(scores,prevent_scores):
            for i in range(len(scores)):
                prevent_scores[i] = scores[i]
            for j in range(len(scores)):
                scores[j] = self.Culculate(Matrix,scores,j)
        return scores

#主函数
def main():
    Test = TextRank('News.txt', 0.85, 0.0001, 2)
    text = Test.FileRead()
    sentences = Test.SentenceToken(text)  # 句子分割
    cleansentences = Test.CleanSent(sentences)
    wordSets = []
    for sentence in cleansentences:
        sentence = Test.WordTokenpro(sentence)
        wordSets.append(sentence)
    Matrix = Test.SimilarMatrix(wordSets)
    scores = Test.Sentscore(Matrix)
    print(scores)
    max_index = map(scores.index, heapq.nlargest(Test.n, scores))  # 找出分数最大的n个句子的索引
    for index in list(max_index):  # 输出分数最大的n个句子
        print(sentences[index])

if __name__== '_main_':
    main()
