#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sklearn import tree
from sklearn.model_selection import KFold
import pandas as pd
import numpy as np
import pydot
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report
from sklearn.externals.six import StringIO  
from IPython.display import Image  
from sklearn.tree import export_graphviz
import pydotplus

#Pienso que tendras que guardar las etiquetas otra vez como haciamos antes :_)
path_mergered     = "data/data_merged.csv"
path_train        = "model/data_train.csv"
path_test         = "model/data_test.csv"

def read_dataset(path):
    return pd.read_csv(path)

def to_csv(path,dataframe):
    np.savetxt(path, dataframe, delimiter=",")

def cross_validations(dataframe, tree_model):
    cv = KFold(n_splits = 10, shuffle=False)
    acc = list()
    max_attb = len(list(dataframe))
    depth_range = range(1, max_attb * 2)

    
    for depth in depth_range:
      fold_accuracy = []
        
      for train_fold, test_fold in cv.split(dataframe):
        f_test = dataframe.loc[test_fold]

        test_acc = tree_model.score(X = f_test.drop(['attack'], axis=1), 
                                  y = f_test['attack'])
        fold_accuracy.append(test_acc)  

      average = sum(fold_accuracy)/len(fold_accuracy)
      acc.append(average)

#    plt.plot(depth_range, acc, marker='o')
#    plt.xlabel('max_depth')
#    plt.ylabel('accuracy')
#    plt.show()
#    plt.savefig("plots/accuracie.png")


def decision_tree(train, test):
  
    features  = train.columns[:13]
    x_train   = train[features]
    y_train   = train['attack']
    
    x_test    = test[features]
    y_test    = test['attack']
    
    X, y      = x_train, y_train
  
    clf = tree.DecisionTreeClassifier(criterion='entropy',
                                  min_samples_leaf = 20, max_depth = 4,
                                  class_weight={0:3.28})
    
    clf.fit(X, y)

    preds_dt = clf.predict(x_test)
    
    print("Decision treee: \n" 
          +classification_report(y_true=y_test, y_pred=preds_dt))
    
    # Matriz de confusión
    
    print("Matriz de confusión:\n")
    matriz = pd.crosstab(test['attack'], preds_dt, rownames=['actual'], colnames=['preds'])
    print(matriz)
    
    # Variables relevantes
    
    print("Relevancia de variables:\n")
    print(pd.DataFrame({'Indicador': features ,
                  'Relevancia': clf.feature_importances_}),"\n")
    print("Máxima relevancia RF :" , max(clf.feature_importances_), "\n")
    
    dot_data = StringIO()

    export_graphviz(clf, out_file=dot_data,
                    feature_names=list(test.drop(['attack'], axis=1)),
                    filled=True, rounded=True,
                    special_characters=True, class_names = ['No attack','Attack'])
  
    graph = pydotplus.graph_from_dot_data(dot_data.getvalue())  
    Image(graph.create_png())
        
    return clf,graph
    
if __name__ == '__main__':
   
  train = read_dataset(path_train)
  test  = read_dataset(path_test)
  
#  train.drop(train.columns[[0,1]], axis=1, inplace=True)
#  test.drop(test.columns[[0,1]], axis=1, inplace=True)
  
  decision_moriarty_tree, graph = decision_tree(train, test)
   
#  data_merged = read_dataset(r.path_merged_data)
#  cross_validations(data_merged, decision_moriarty_tree)
   
   
   
   
   
