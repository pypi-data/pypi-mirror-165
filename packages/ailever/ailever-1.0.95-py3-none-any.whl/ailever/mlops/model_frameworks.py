from abc import *
from importlib import import_module
import os
import re

import pandas as pd
import joblib

class Framework(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_model_class(self):
        pass

    @abstractmethod
    def train(self):
        pass

    @abstractmethod
    def predict(self):
        pass

    @abstractmethod
    def upload(self):
        pass
 
    @abstractmethod
    def save_insidemodel(self):
        pass

    @abstractmethod
    def save_outsidemodel(self):
        pass


class FrameworkSklearn(Framework):
    def __init__(self):
        self.modules = dict()
        self.modules['linear_model'] = list(filter(
            lambda x: re.search('Classifier|Regression|Regressor', x), import_module('sklearn.linear_model').__all__))
        self.modules['ensemble'] = list(filter(
            lambda x: re.search('Classifier|Regressor', x), import_module('sklearn.ensemble').__all__))
        self.modules['neighbors'] = list(filter(
            lambda x: re.search('Classifier|Regressor', x), import_module('sklearn.neighbors').__all__))
        self.modules['tree'] = list(filter(
            lambda x: re.search('Classifier|Regressor', x), import_module('sklearn.tree').__all__))
        self.modules['svm'] = list(filter(
            lambda x: re.search('SVC|SVR', x), import_module('sklearn.svm').__all__))
        self.modules['pipeline'] = list(filter(
            lambda x: re.search('Pipeline', x), import_module('sklearn.pipeline').__all__))
 
        self.models = list()
        for model_set in self.modules.values():
            self.models.extend(model_set)

    def get_model_class(self, supported_framework, module_name, model_name):
        model_class = getattr(import_module(supported_framework+'.'+module_name), model_name)
        return model_class

    def train(self, model, dataset):
        X = dataset.loc[:, dataset.columns != 'target']
        y = dataset.loc[:, 'target'].ravel()
        model.fit(X, y)
        return model

    def predict(self, model, X):
        return model.predict(X)

    def upload(self, model_registry_path):
        return joblib.load(model_registry_path)

    def save_insidemodel(self, model, mlops_path, saving_name):
        saving_name = saving_name + '.joblib'
        model_registry_saving_path = os.path.join(mlops_path, saving_name)
        joblib.dump(model, model_registry_saving_path)

        training_info_detail = dict()
        training_info_detail['saving_model_name'] = saving_name
        return training_info_detail

    def save_outsidemodel(self, model, model_registry_path, outsidelog_path):
        extension = '.joblib'
        model_registry_path = model_registry_path + extension
        outsidelog = pd.read_csv(outsidelog_path)
        outsidelog.iat[0, 4] = outsidelog.iat[0, 4] + extension
        outsidelog.to_csv(outsidelog_path, index=False)
        return joblib.dump(model, model_registry_path)


class FrameworkXgboost(Framework):
    def __init__(self):
        self.modules = dict()
        self.modules['xgboost_model'] = list(filter(lambda x: re.search('Classifier|Regressor', x), import_module('xgboost').__all__))

        self.models = list()
        for model_set in self.modules.values():
            self.models.extend(model_set)

    def get_model_class(self, supported_framework, module_name, model_name):
        model_class = getattr(import_module(supported_framework), model_name)
        return model_class

    def train(self, model, dataset):
        X = dataset.loc[:, dataset.columns != 'target']
        y = dataset.loc[:, 'target'].ravel()
        model.fit(X, y)
        return model

    def predict(self, model, X):
        return model.predict(X)

    def upload(self, model_registry_path):
        return joblib.load(model_registry_path)

    def save_insidemodel(self, model, mlops_path, saving_name):
        saving_name = saving_name + '.joblib'
        model_registry_saving_path = os.path.join(mlops_path, saving_name)
        joblib.dump(model, model_registry_saving_path)

        training_info_detail = dict()
        training_info_detail['saving_model_name'] = saving_name
        return training_info_detail

    def save_outsidemodel(self, model, model_registry_path, outsidelog_path):
        extension = '.joblib'
        model_registry_path = model_registry_path + extension
        outsidelog = pd.read_csv(outsidelog_path)
        outsidelog.iat[0, 4] = outsidelog.iat[0, 4] + extension
        outsidelog.to_csv(outsidelog_path, index=False)
        return joblib.dump(model, model_registry_path)

class FrameworkLightgbm(Framework):
    def __init__(self):
        self.modules = dict()
        self.modules['lightgbm_model'] = list(filter(lambda x: re.search('Classifier|Regressor', x), import_module('lightgbm').__all__))

        self.models = list()
        for model_set in self.modules.values():
            self.models.extend(model_set)

    def get_model_class(self, supported_framework, module_name, model_name):
        model_class = getattr(import_module(supported_framework), model_name)
        return model_class

    def train(self, model, dataset):
        X = dataset.loc[:, dataset.columns != 'target']
        y = dataset.loc[:, 'target'].ravel()
        model.fit(X, y)
        return model

    def predict(self, model, X):
        return model.predict(X)

    def upload(self, model_registry_path):
        return joblib.load(model_registry_path)

    def save_insidemodel(self, model, mlops_path, saving_name):
        saving_name = saving_name + '.joblib'
        model_registry_saving_path = os.path.join(mlops_path, saving_name)
        joblib.dump(model, model_registry_saving_path)

        training_info_detail = dict()
        training_info_detail['saving_model_name'] = saving_name
        return training_info_detail

    def save_outsidemodel(self, model, model_registry_path, outsidelog_path):
        extension = '.joblib'
        model_registry_path = model_registry_path + extension
        outsidelog = pd.read_csv(outsidelog_path)
        outsidelog.iat[0, 4] = outsidelog.iat[0, 4] + extension
        outsidelog.to_csv(outsidelog_path, index=False)
        return joblib.dump(model, model_registry_path)


class FrameworkCatboost(Framework):
    def __init__(self):
        self.modules = dict()
        self.modules['catboost_model'] = list(filter(lambda x: re.search('Classifier|Regressor', x), import_module('catboost').__all__))

        self.models = list()
        for model_set in self.modules.values():
            self.models.extend(model_set)

    def get_model_class(self, supported_framework, module_name, model_name):
        model_class = getattr(import_module(supported_framework), model_name)
        return model_class

    def train(self, model, dataset):
        X = dataset.loc[:, dataset.columns != 'target']
        y = dataset.loc[:, 'target'].ravel()
        model.fit(X, y, silent=True)
        return model

    def predict(self, model, X):
        return model.predict(X).squeeze()

    def upload(self, model_registry_path):
        return joblib.load(model_registry_path)

    def save_insidemodel(self, model, mlops_path, saving_name):
        saving_name = saving_name + '.joblib'
        model_registry_saving_path = os.path.join(mlops_path, saving_name)
        joblib.dump(model, model_registry_saving_path)

        training_info_detail = dict()
        training_info_detail['saving_model_name'] = saving_name
        return training_info_detail

    def save_outsidemodel(self, model, model_registry_path, outsidelog_path):
        extension = '.joblib'
        model_registry_path = model_registry_path + extension
        outsidelog = pd.read_csv(outsidelog_path)
        outsidelog.iat[0, 4] = outsidelog.iat[0, 4] + extension
        outsidelog.to_csv(outsidelog_path, index=False)
        return joblib.dump(model, model_registry_path)



class FrameworkTorch(Framework):
    def __init__(self):
        self.modules = dict()
        self.modules['catboost_model'] = list(filter(lambda x: re.search('Classifier|Regressor', x), import_module('catboost').__all__))

        self.models = list()
        for model_set in self.modules.values():
            self.models.extend(model_set)

    def get_model_class(self, supported_framework, module_name, model_name):
        model_class = getattr(import_module(supported_framework), model_name)
        return model_class

    def train(self, model, dataset):
        X = dataset.loc[:, dataset.columns != 'target']
        y = dataset.loc[:, 'target'].ravel()
        model.fit(X, y, silent=True)
        return model

    def predict(self, model, X):
        return model.predict(X).squeeze()

    def upload(self, model_registry_path):
        return joblib.load(model_registry_path)

    def save_insidemodel(self, model, mlops_path, saving_name):
        saving_name = saving_name + '.joblib'
        model_registry_saving_path = os.path.join(mlops_path, saving_name)
        joblib.dump(model, model_registry_saving_path)

        training_info_detail = dict()
        training_info_detail['saving_model_name'] = saving_name
        return training_info_detail

    def save_outsidemodel(self, model, model_registry_path, outsidelog_path):
        extension = '.joblib'
        model_registry_path = model_registry_path + extension
        outsidelog = pd.read_csv(outsidelog_path)
        outsidelog.iat[0, 4] = outsidelog.iat[0, 4] + extension
        outsidelog.to_csv(outsidelog_path, index=False)
        return joblib.dump(model, model_registry_path)



class FrameworkTensorflow(Framework):
    def __init__(self):
        self.modules = dict()
        self.modules['catboost_model'] = list(filter(lambda x: re.search('Classifier|Regressor', x), import_module('catboost').__all__))

        self.models = list()
        for model_set in self.modules.values():
            self.models.extend(model_set)

    def get_model_class(self, supported_framework, module_name, model_name):
        model_class = getattr(import_module(supported_framework), model_name)
        return model_class

    def train(self, model, dataset):
        X = dataset.loc[:, dataset.columns != 'target']
        y = dataset.loc[:, 'target'].ravel()
        model.fit(X, y, silent=True)
        return model

    def predict(self, model, X):
        return model.predict(X).squeeze()

    def upload(self, model_registry_path):
        return joblib.load(model_registry_path)

    def save_insidemodel(self, model, mlops_path, saving_name):
        saving_name = saving_name + '.joblib'
        model_registry_saving_path = os.path.join(mlops_path, saving_name)
        joblib.dump(model, model_registry_saving_path)

        training_info_detail = dict()
        training_info_detail['saving_model_name'] = saving_name
        return training_info_detail

    def save_outsidemodel(self, model, model_registry_path, outsidelog_path):
        extension = '.joblib'
        model_registry_path = model_registry_path + extension
        outsidelog = pd.read_csv(outsidelog_path)
        outsidelog.iat[0, 4] = outsidelog.iat[0, 4] + extension
        outsidelog.to_csv(outsidelog_path, index=False)
        return joblib.dump(model, model_registry_path)



