from sklearn.svm import LinearSVC
from sklearn.datasets import load_iris
from sklearn.ensemble import ExtraTreesClassifier
iris = load_iris()
X, y = iris.data, iris.target

X_new = LinearSVC(C=0.01, penalty="l1", dual=False).fit_transform(X, y)
clf = ExtraTreesClassifier()
X_new = clf.fit(X, y).transform(X)