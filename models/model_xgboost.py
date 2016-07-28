# -*- coding: utf-8 -*-
import numpy as np
from keras.utils import np_utils, generic_utils
import pandas as pd
from sklearn.feature_extraction import DictVectorizer
from hyperopt import hp
from hyperopt import fmin, tpe, Trials
from sklearn import cross_validation
from sklearn.svm import SVR
import xgboost as xgb
import matplotlib.pyplot as plt
from matplotlib.pyplot import savefig
from sklearn.metrics import make_scorer
from sklearn.cross_validation import train_test_split
from sklearn.cross_validation import KFold
# serialization
import cPickle

import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
from config import x_train_file, x_test_file, y_train_file, y_test_file, tags_number, unique_tags_csv


def top5_error(preds, dtrain):
    labels = dtrain.get_label()
    yprob = preds.reshape(labels.shape[0], tags_number)

    correct = 0
    for i in range(labels.shape[0]):
        pred = yprob[i]

        ylabels = pred.argsort()[-5:][::-1]
        ylabels = ylabels.astype(int)
        if labels[i] in ylabels:
            correct += 1
    error = 1 - correct / float(labels.shape[0])
    # print 'top-5 error: %f' % (error)
    return 'error', error


def run_model():
    xg_train = xgb.DMatrix(X_train, label=y_train)
    xg_test = xgb.DMatrix(X_test, label=y_test)

    # setup parameters for xgboost
    param = {}
    # use softmax multi-class classification
    param['objective'] = 'multi:softmax'
    # scale weight of positive examples
    param['eta'] = 0.1
    param['max_depth'] = 6
    param['silent'] = 0
    param['nthread'] = 0
    param['num_class'] = tags_number

    watchlist = [(xg_train, 'train'), (xg_test, 'test')]
    num_round = 1

    # do the same thing again, but output probabilities
    param['objective'] = 'multi:softprob'
    bst = xgb.train(param, xg_train, num_round, watchlist)
    # Note: this convention has been changed since xgboost-unity
    # get prediction, this is in 1D array, need reshape to (ndata, nclass)
    yprob = bst.predict(xg_test).reshape(len(y_test), tags_number)
    print yprob.shape

    correct = 0
    for i in range(len(y_test)):
        pred = yprob[i]

        ylabels = pred.argsort()[-5:][::-1]
        ylabels = ylabels.astype(int)
        print y_test[i], ylabels
        if y_test[i] in ylabels:
            correct += 1
    error = 1 - correct / float(len(y_test))
    print 'top-5 error: %f' % (error)


def score(param_dict):
    print param_dict

    num_rounds = int(param_dict['num_round'])

    # setup parameters for xgboost
    param = {}
    param['booster'] = param_dict['booster']
    param['objective'] = param_dict['objective']

    '''
    param['eta'] = param_dict['eta']
    param['lambda'] = param_dict['lambda']
    param['alpha'] = param_dict['alpha']
    param['lambda_bias'] = param_dict['lambda_bias']
    '''
    param['gamma'] = param_dict['gamma']
    param['min_child_weight'] = param_dict['min_child_weight']
    param['max_depth'] = int(param_dict['max_depth'])
    param['subsample'] = param_dict['subsample']
    param['colsample_bytree'] = param_dict['colsample_bytree']

    param['silent'] = int(param_dict['silent'])
    param['nthread'] = int(param_dict['nthread'])
    param['num_class'] = int(param_dict['num_class'])

    res = xgb.cv(param, xg_train, num_rounds, nfold=2, metrics={'error'}, seed=0, feval=top5_error)

    print 'score: ', res.tail(1).iloc[0][0]
    return res.tail(1).iloc[0][0]


def optimize(trials):
    space = {
        'booster': 'gblinear',
        'objective': 'multi:softprob',
        'eta': hp.quniform('eta', 0.01, 1, 0.01),
        'lambda': hp.quniform('lambda', 0, 5, 0.05),
        'alpha': hp.quniform('alpha', 0, 0.5, 0.005),
        'lambda_bias': hp.quniform('lambda_bias', 0, 3, 0.1),
        'num_round': hp.quniform('num_round', 10, 500, 10),
        'num_class': tags_number,
        'nthread': 0,
        'silent': 1
    }

    space2 = {
        'booster': 'gbtree',
        'objective': 'multi:softprob',
        'eta': hp.quniform('eta', 0.01, 1, 0.01),
        'gamma': hp.quniform('gamma', 0, 2, 0.1),
        'min_child_weight': hp.quniform('min_child_weight', 0, 10, 1),
        'max_depth': hp.quniform('max_depth', 1, 10, 1),
        'subsample': hp.quniform('subsample', 0.5, 1, 0.1),
        'colsample_bytree': hp.quniform('colsample_bytree', 0.1, 1, 0.1),
        'num_round': hp.quniform('num_round', 10, 100, 10),
        'num_class': tags_number,
        'nthread': 0,
        'silent': 1
    }

    best = fmin(score, space2, algo=tpe.suggest, trials=trials, max_evals=100)

    return best


# label-lookup
labels_loopup = []
count = 0
with open(unique_tags_csv) as f:
    for line in f:
        (tag, tag_cn, label) = line.strip().split(',')
        if count != int(label):
            print 'invalid label loopup!'
        labels_loopup.append(tag_cn)
        count = count + 1


# loading data
with open(x_train_file, 'rb') as f:
    X_train = cPickle.load(f)
with open(x_test_file, 'rb') as f:
    X_test = cPickle.load(f)
with open(y_train_file, 'rb') as f:
    y_train = cPickle.load(f)
with open(y_test_file, 'rb') as f:
    y_test = cPickle.load(f)

print(X_train.shape[0], X_train.shape[1], 'train samples')
print(X_test.shape[0], X_test.shape[1], 'test samples')
X_train = X_train.astype('float32')
X_test = X_test.astype('float32')

xg_train = xgb.DMatrix(X_train, label=y_train)
xg_test = xgb.DMatrix(X_test, label=y_test)

# run_model()

# Trials object where the history of search will be stored
trials = Trials()

best_param = optimize(trials)

# run_model(best_param)
print best_param

parameters = ['eta', 'gamma', 'min_child_weight', 'max_depth', 'subsample', 'colsample_bytree', 'num_round']
# parameters = ['eta', 'lambda', 'alpha', 'lambda_bias', 'num_round']
cols = len(parameters)
f, axes = plt.subplots(nrows=1, ncols=cols, figsize=(40, 7))
cmap = plt.cm.jet
for i, val in enumerate(parameters):
    xs = np.array([t['misc']['vals'][val] for t in trials.trials]).ravel()
    ys = [t['result']['loss'] for t in trials.trials]
    xs, ys = zip(*sorted(zip(xs, ys)))
    axes[i].scatter(xs, ys, s=20, linewidth=0.01, alpha=0.25, c=cmap(float(i) / len(parameters)))
    axes[i].set_title(val)
    axes[i].set_ylim([0.2, 0.6])

learn_fig = './learn.png'
savefig(learn_fig)
# plt.show()
