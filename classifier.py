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

# Code_1 for violent Categories
# Code_2 for non-violent Categories

train_file_loc = '/Users/abhi/Documents/data_m/Data_Final/Train/CODE_'
test_file_loc = '/Users/abhi/Documents/data_m/Data_Final/Test/CODE_'

train_data_X = []
train_data_Y = []

test_data_X = []
test_data_Y = []

# reads the text data for
def readData(files_location):
    X= []
    Y= []
    for category in range(0,2):
        files_paths =  glob.glob(files_location + str(category+1) +"/*.txt")

        for file_name in files_paths:
            X.append(readFileFromLine(file_name,3))
            Y.append(category)
    return X, Y

def getData(path):
    pass


def readFileFromLine(file_name,line_no):
    filez = open(file_name,'r')
    lines = filez.readlines()[line_no:]
    # text = text starting from Line line_no
    text = ''.join(lines)
    filez.close()

    return text

# read Train data
train_data_X, train_data_Y =  readData(train_file_loc)

# read Test data
test_data_X, test_data_Y =  readData(test_file_loc)


# cv = CountVectorizer(input ='total_feature_list',stop_words = {'english'},lowercase=True,analyzer ='word',binary =True,max_features =70)
cv = TfidfVectorizer(input ='total_feature_list',stop_words = {'english'},lowercase=True,analyzer ='word',binary =False,max_features =70)

'''
train_data_X = cv.fit_transform(train_data_X).toarray()

clf = DecisionTreeClassifier(max_depth=5)
clf = clf.fit(train_data_X, train_data_Y)

test_data_X = cv.fit_transform(test_data_X).toarray()
print "DecisionTreeClassifier score :", clf.score(test_data_X,test_data_Y)
'''



clf = RandomForestClassifier(n_estimators =70)
clf = clf.fit(train_data_X, train_data_Y)

# test_data_X = cv.fit_transform(test_data_X).toarray()
print "RandomForestClassifier score :", clf.score(test_data_X,test_data_Y)




