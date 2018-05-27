# -*-coding:utf8-*-
from collections import defaultdict
import os
import jieba
import codecs

class SentiCalc():
    @classmethod
    def readLines(cls, filename):
        var = []
        with codecs.open(filename, 'r', encoding='utf-8-sig') as file:
            for line in file:
                var.append(line.strip())
        return var

    #文本切割
    @classmethod
    def sen2word(cls, sentence):
        '''
        切割句子为单词
        去掉停用词
        :param sentence:
        :return:
        '''
        segList = jieba.cut(sentence)
        segResult = []
        for w in segList:
            segResult.append(w)

        stopwords = cls.readLines('stop_words.txt')
        newSent = []
        for word in segResult:
            if word in stopwords:
                continue
            else:
                newSent.append(word)
        return newSent

    #情感定位
    @classmethod
    def classifyWords(cls, wordList):
        #情感词
        senList = cls.readLines('BosonNLP_sentiment_score.txt')
        senDict = defaultdict()
        for s in senList:
            if len(s.split(' '))==2:
                senDict[s.split(' ')[0]] = s.split(' ')[1]
        #否定词
        notList = cls.readLines('notDict.txt')
        #程度副词
        degreeList = cls.readLines('degreeDict.txt')
        degreeDict = defaultdict()
        for d in degreeList:
            degreeDict[d.split(' ')[0]] = d.split(' ')[1]

        senWord = []
        notWord = []
        degreeWord = []

        for word in wordList:
            if word[0] in senDict.keys() and word[0] not in notList:
                sen = [word[1],senDict[word[0]]]
                senWord.append(sen)
            elif word[0] in notList and word[0] not in degreeDict.keys():
                noot = [word[1] ,-1]
                notWord.append(noot)
            elif word[0] in degreeDict.keys():
                degree = [word[1],degreeDict[word[0]]]
                degreeWord.append(degree)
        return senWord,notWord,degreeWord

    #取嵌入数组中每个数组的第i个值
    @classmethod
    def extractLoc(cls, mulList,i):
        List = []
        for list in mulList:
            List.append(list[i])
        return List

    #根据嵌入数组中的第一个值找到相应的第二个值
    @classmethod
    def k2v(cls, mulLi0val,mulList):
        for list in mulList:
            if list[0] == mulLi0val:
                return list[1]

    #情感聚合
    @classmethod
    def scoreSent(cls, senWord,notWord,degreeWord,segResult):
        W = 1
        score = 0
        #存所有情感词的位置的列表
        senLoc = cls.extractLoc(senWord,0)
        notLoc = cls.extractLoc(notWord,0)
        degreeLoc = cls.extractLoc(degreeWord,0)
        senloc = -1

        if(senLoc[0]!=0):
            for k in range(0,senLoc[0]):
                if k in senLoc:
                    W = 1
                elif k in notLoc:
                    W *= -1
                elif k in degreeLoc:
                    W *= float(cls.k2v(k,degreeWord))

        #遍历句中所有单词senResult，i为单词绝对位置
        for i in range(0,len(segResult)):
            #如果该词为情感词
            if i in senLoc:
                #loc为情感词位置列表的序号
                senloc += 1
                #直接添加该情感词分数
                score += W * float(cls.k2v(i, senWord))
                W = 1
                if senloc < len(senLoc) -1:
                    #判断该情感词与下一情感词之间是否有否定词或程度副词
                    #j为绝对位置
                    for j in range(senLoc[senloc],senLoc[senloc+1]):
                        #如果有否定词
                        if j in notLoc:
                            W *= -1
                        #如果有程度副词
                        elif j in degreeLoc:
                            W *= float(cls.k2v(j, degreeWord))
            #i定位至下一个情感词
            if senloc < len(senLoc) -1:
                i = senLoc[senloc + 1]
        return score

    @classmethod
    def score_calc(cls, sentense):
        NewSentence = cls.sen2word(sentense)
        wordList = []
        for i in range(len(NewSentence)):
            word = [NewSentence[i], i]
            wordList.append(word)
        # print wordList
        senWord, notWord, degreeWord = cls.classifyWords(wordList)
        score = cls.scoreSent(senWord, notWord, degreeWord, NewSentence)
        return score

# print SentiCalc.score_calc('冯潇霆:惨败后里皮没说啥但很生气争取击败捷克。')

