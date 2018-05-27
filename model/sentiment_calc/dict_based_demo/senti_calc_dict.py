# -*-coding:utf8-*-
from collections import defaultdict
import jieba
import codecs

help_file_dir = '../../../resource/sentiment_calc/dict_based_demo/'


class SentiCalc():
    @classmethod
    def readLines(cls, filename):
        var = []
        with codecs.open(filename, 'r', encoding='utf-8-sig') as file:
            for line in file:
                var.append(line.strip())
        return var

    # 文本切割
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

        stopwords = cls.readLines(help_file_dir + 'stop_words.txt')
        newSent = []
        for word in segResult:
            if word in stopwords:
                continue
            else:
                newSent.append(word)
        return newSent

    # 情感定位
    @classmethod
    def classifyWords(cls, wordDict):
        # 情感词
        senList = cls.readLines(help_file_dir + 'BosonNLP_sentiment_score.txt')
        senDict = defaultdict()
        for s in senList:
            if len(s.split(' ')) == 2:
                senDict[s.split(' ')[0]] = s.split(' ')[1]
        # 否定词
        notList = cls.readLines(help_file_dir + 'notDict.txt')
        # 程度副词
        degreeList = cls.readLines(help_file_dir + 'degreeDict.txt')
        degreeDict = defaultdict()
        for d in degreeList:
            degreeDict[d.split(' ')[0]] = d.split(' ')[1]

        senWord = defaultdict()
        notWord = defaultdict()
        degreeWord = defaultdict()

        for word in wordDict.keys():
            if word in senDict.keys() and word not in notList and word not in degreeDict.keys():
                senWord[wordDict[word]] = senDict[word]
            elif word in notList and word not in degreeDict.keys():
                notWord[wordDict[word]] = -1
            elif word in degreeDict.keys():
                degreeWord[wordDict[word]] = degreeDict[word]
        return senWord, notWord, degreeWord

    # 情感聚合
    @classmethod
    def scoreSent(cls, senWord, notWord, degreeWord, segResult):
        W = 1
        score = 0
        # scores = []
        # 存所有情感词的位置的列表
        senLoc = senWord.keys()
        notLoc = notWord.keys()
        degreeLoc = degreeWord.keys()
        senloc = -1

        # 遍历句中所有单词senResult，i为单词绝对位置
        for i in range(0, len(segResult)):
            # 如果该词为情感词
            if i in senLoc:
                # loc为情感词位置列表的序号
                senloc += 1
                # 直接添加该情感词分数
                # scores.append(W * float(k2v(i,senWord)))
                score += W * float(senWord[i])
                if senloc < len(senLoc) - 1:
                    # 判断该情感词与下一情感词之间是否有否定词或程度副词
                    # j为绝对位置
                    for j in range(senLoc[senloc], senLoc[senloc + 1]):
                        # 如果有否定词
                        if j in notLoc:
                            W *= -1
                        # 如果有程度副词
                        elif j in degreeLoc:
                            W *= float(degreeWord[j])
            # i定位至下一个情感词
            if senloc < len(senLoc) - 1:
                i = senLoc[senloc + 1]
        return score

    @classmethod
    def score_calc(cls, sentense):
        NewSentence = cls.sen2word(sentense)
        wordDict = defaultdict()
        for i in range(len(NewSentence)):
            wordDict[NewSentence[i]] = i
        # print wordDict
        senWord, notWord, degreeWord = cls.classifyWords(wordDict)
        score = cls.scoreSent(senWord, notWord, degreeWord, NewSentence)
        # 1-5分算中性
        if score < 1:
            return -1
        elif score < 5:
            return 0
        else:
            return 1

# print SentiCalc.score_calc('2500万欧元！尤文图斯pk罗马国米抢意大利红星')
# print SentiCalc.score_calc('媒体：德不愿看中美贸易摩擦加剧 望谈判解决争端')
