from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.model_selection import GridSearchCV
import numpy as np
import os.path
import glob

import pickle
from sklearn.externals import joblib

# Code_1 for violent Categories      -  0
# Code_2 for non-violent Categories  -  1

class ArticleClassifer(object):
    """docstring for ArticleClassifer"""
    def __init__(self):
        super(ArticleClassifer, self).__init__()
        self.train_file_loc = '/Users/abhi/Documents/data_m/Data_Final/Train/CODE_'
        self.test_file_loc = '/Users/abhi/Documents/data_m/Data_Final/Test/CODE_'

        self.train_data_X = []
        self.train_data_Y = []

        self.test_data_X = []
        self.test_data_Y = []

        self.cv = 0
        self.clf = 0
        # load the vectorizer if exists
        if os.path.isfile('tdif.pkl') :
            self.cv =joblib.load('tdif.pkl')
        else:
            self.cv = TfidfVectorizer(input ='total_feature_list',stop_words = {'english'},lowercase=True,analyzer ='word',binary =False,max_features =70)
            joblib.dump(self.cv, 'tdif.pkl')

        # load the classfier If exists
        if os.path.isfile('classifer.pkl'):
            self.clf =joblib.load('classifer.pkl')
        else:
            self.loadData()
            self.trainData()



    # load data into test and training set
    def loadData(self):
        # read Train data
        self.train_data_X, self.train_data_Y =  self.readData(self.train_file_loc)

        # read Test data
        self.test_data_X, self.test_data_Y =  self.readData(self.test_file_loc)

    def trainData(self):
        self.train_data_X = self.cv.fit_transform(self.train_data_X).toarray()
        self.test_data_X = self.cv.fit_transform(self.test_data_X).toarray()

        self.clf = RandomForestClassifier(n_estimators =70)
        self.clf = self.clf.fit(self.train_data_X, self.train_data_Y)

        # save classifer
        joblib.dump(self.clf, 'classifer.pkl')

        print "Accuracy Score :", self.clf.score(self.test_data_X,self.test_data_Y)



    # reads the text data for
    def readData(self, files_location):
        X= []
        Y= []
        for category in range(0,2):
            files_paths =  glob.glob(files_location + str(category+1) +"/*.txt")

            for file_name in files_paths:
                X.append(self.readFileFromLine(file_name,3))
                Y.append(category)
        return X, Y

    def readFileFromLine(self, file_name, line_no):
        filez = open(file_name,'r')
        lines = filez.readlines()[line_no:]
        # text = text starting from Line line_no
        text = ''.join(lines)
        filez.close()

        return text

    def classify(articleText):
        # violent1 = '/Users/abhi/Documents/hack2017/hackuvic2017/violent1.txt'
        # f1 = readFileFromLine(violentFile,0)
        # f2 = readFileFromLine(nonviolentFile,0)
        # f3 = readFileFromLine(nv1,0)
        # f4 = readFileFromLine(violent1,0)
        # f5 = readFileFromLine(nv2,0)

        Reddit_articles = []
        Reddit_articles.append(articleText)

        X = cv.transform(Reddit_articles)

        out =clf.predict(X)

        return out




articleClassifier = ArticleClassifer()






