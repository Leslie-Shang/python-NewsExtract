#导入textrnak4ZH关键词和生成摘要的类
from textrank4zh import TextRank4Keyword,TextRank4Sentence
from tkinter import *
import tkinter.filedialog #获取文件路径和文件名

#定义窗口
win = Tk()
win.geometry("1600x1200")
win.title("请选择一个文本文件")

#创建分类词实例
tw = TextRank4Keyword()


#输出关键词
def Keyword(file):
    tw.analyze(file, lower=True, window=2)  # 分析文本
    lb = Label(win,text = '关键词为:')
    lb.pack()
    for words in tw.get_keywords(num=10,word_min_len=1):
        disp = Label(win,text = words.word)
        disp.pack()



#输出关键短语
def Kephrase(file):
    tw.analyze(file, lower=True, window=2)  # 分析文本
    lb = Label(win, text='关键短语为:')
    lb.pack()
    for phrase in tw.get_keyphrases(keywords_num=10,min_occur_num=2):
        disp = Label(win,text = phrase)
        disp.pack()


#创建分类句实例
ts = TextRank4Sentence()

#输出关键句
def Keysentence(file):
    ts.analyze(file,lower=True,source='all_filters')
    lb = Label(win,text = '摘要为:')
    lb.pack()
    for sentences in ts.get_key_sentences(num=3):
        disp = Label(win, text = sentences.sentence)
        disp.pack()


#创建GUI界面
def file_choose():
    filename = tkinter.filedialog.askopenfilename()
    if filename != '':
        lb.config(text = "您选择的文件是："+filename);
    else:
        lb.config(text = "您没有选择任何文件");
    file = open(filename,'r')
    news = file.read()
    Keyword(news)
    Kephrase(news)
    Keysentence(news)
    file.close()

lb = Label(win,text = '')
lb.pack()
btn = Button(win,text="选择文件",command=file_choose)
btn.pack()
win.mainloop()
