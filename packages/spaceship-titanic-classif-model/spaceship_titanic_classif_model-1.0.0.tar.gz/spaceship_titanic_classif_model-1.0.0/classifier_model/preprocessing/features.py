from sklearn.base import BaseEstimator, TransformerMixin


class CabinPreprocess(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self

    def transform(self, X):

        X = X.copy()
        X["CabinDeck"] = X["Cabin"].str[0]
        X["CabinSide"] = X["Cabin"].str[-1]
        X.drop("Cabin", axis=1, inplace=True)
        return X
