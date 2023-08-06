from .evaluation import classification as cls_evaluate
from .evaluation import regression as reg_evaluate
from ..logging_system import logger

import sys
from functools import wraps
from copy import deepcopy
import pandas



class TrainScenario:
    def __init__(self, *args, **kwargs): # args: (, ), kwargs: {objective='for equip'}
        self.args = args
        self.kwargs = kwargs

    def __call__(self, func):
        @wraps(func)
        def trigger(*args, **kwargs): # args: (model,) kwargs: {}
            model = func(*args, **kwargs)
            return model
        return trigger


class Trigger:
    def __init__(self, model):
        self.__initial_memory__ = True
        self.__count__ = 0
        self.__model__ = model
        self.__history__ = list()
        self.__history__.append(deepcopy(model))

    def cls_trigger(self, train, validation, inference=None, predict=lambda x:x, predict_proba=lambda x:x, fit=lambda x:x, target=list(), refresh=False, store=True, note=None):
        if refresh:
            logger['mlops'].info('Your model on the trigger object will be lost all memory during training.')
            self.__model__ = self.__history__[0] # training strart model
            self.__initial_memory__ = True
        else:
            logger['mlops'].info('Your model on the trigger object will be additionally trained on the previous step model.')

        assert isinstance(train, pandas.DataFrame)
        assert isinstance(validation, pandas.DataFrame)
        assert isinstance(inference, pandas.DataFrame) if inference is not None else True
        inference = validation.copy()

        assert isinstance(target, (str, tuple, list))
        assert callable(predict), 'The predict object is Not Callable. It must be type of callable object.'
        assert callable(predict_proba), 'The predict_proba object is Not Callable. It must be type of callable object.'
        assert callable(fit), 'The fit object is Not Callable. It must be type of callable object.'
        assert isinstance(refresh, bool)
        assert isinstance(store, (bool, str))

        model = deepcopy(self.__model__)
        setattr(model, 'fit', fit)
        setattr(model, 'predict', predict)
        setattr(model, 'predict_proba', predict_proba)

        X_train = train[train.columns[~train.columns.isin(target)]]
        y_train = train[train.columns[train.columns.isin(target)]]
        X_validation = validation[validation.columns[~validation.columns.isin(target)]]
        y_validation = validation[validation.columns[validation.columns.isin(target)]]
        X_test = inference[inference.columns[~inference.columns.isin(target)]]
        y_test = inference[inference.columns[inference.columns.isin(target)]]

        model.fit(X_train, y_train)

        y = dict()
        y['train'] = dict()
        y['validation'] = dict()
        y['test'] = dict()

        evaluation_metrics = list()
        for domain in y.keys():
            _X = locals()['X'+ '_' +domain] # X_train, X_validation, X_test
            _y = locals()['y'+ '_' +domain] # y_train, y_validation, y_test

            y[domain]['true'] = _y
            y[domain]['pred'] = model.predict(_X)
            y[domain]['prob'] = model.predict_proba(_X)

            evaluation_metric = cls_evaluate(y[domain]['true'], y[domain]['pred']).copy()
            evaluation_metric.insert(0, 'domain', domain)
            evaluation_metrics.append(evaluation_metric)
        evaluation_metrics = pandas.concat(evaluation_metrics, axis=0).reset_index(drop=True)
        evaluation_metrics.insert(0, 'session', deepcopy(self.__count__))
        evaluation_metrics['initial_memory'] = bool(refresh) if self.__count__ != 0 else self.__initial_memory__
        evaluation_metrics['storing_model'] = bool(store) 

        self.__count__ += 1
        self.__model__ = model
        self.__history__ = self.__history__ + [deepcopy(model)] if store else self.__history__
        evaluation_metrics['history_index'] = len(self.__history__) - 1
        evaluation_metrics['note'] = note

        self.__evaluation__ = pandas.concat([self.__evaluation__, evaluation_metrics], axis=0).reset_index(drop=True) if hasattr(self, '__evaluation__') else evaluation_metrics
        self.__dataset__ = y # only lastest dataset
        return self


    def reg_trigger(self, train, validation, inference=None, predict=lambda x:x, fit=lambda x:x, target=list(), refresh=False, store=True, note=None):
        assert isinstance(train, pandas.DataFrame)
        assert isinstance(validation, pandas.DataFrame)
        assert isinstance(inference, pandas.DataFrame) if inference is not None else True
        inference = validation.copy()

        assert isinstance(target, (str, tuple, list))
        assert callable(predict), 'The predict object is Not Callable. It must be type of callable object.'
        assert callable(fit), 'The fit object is Not Callable. It must be type of callable object.'
        assert isinstance(refresh, bool)
        assert isinstance(store, (bool, str))

        model = deepcopy(self.__model__)
        setattr(model, 'fit', fit)
        setattr(model, 'predict', predict)

        X_train = train[train.columns[~train.columns.isin(target)]]
        y_train = train[train.columns[train.columns.isin(target)]]
        X_validation = validation[validation.columns[~validation.columns.isin(target)]]
        y_validation = validation[validation.columns[validation.columns.isin(target)]]
        X_test = inference[inference.columns[~inference.columns.isin(target)]]
        y_test = inference[inference.columns[inference.columns.isin(target)]]

        model.fit(X_train, y_train)

        y = dict()
        y['train'] = dict()
        y['validation'] = dict()
        y['test'] = dict()

        evaluation_metrics = list()
        for domain in y.keys():
            _X = locals()['X'+ '_' +domain] # X_train, X_validation, X_test
            _y = locals()['y'+ '_' +domain] # y_train, y_validation, y_test

            y[domain]['true'] = _y
            y[domain]['pred'] = model.predict(_X)

            evaluation_metric = reg_evaluate(y[domain]['true'], y[domain]['pred']).copy()
            evaluation_metric.insert(0, 'domain', domain)
            evaluation_metrics.append(evaluation_metric)
        evaluation_metrics = pandas.concat(evaluation_metrics, axis=0).reset_index(drop=True)
        evaluation_metrics.insert(0, 'session', deepcopy(self.__count__))
        evaluation_metrics['initial_memory'] = bool(refresh) if self.__count__ != 0 else self.__initial_memory__
        evaluation_metrics['storing_model'] = bool(store) 

        self.__count__ += 1
        self.__model__ = model
        self.__history__ = self.__history__ + [deepcopy(model)] if store else self.__history__
        evaluation_metrics['history_index'] = len(self.__history__) - 1
        evaluation_metrics['note'] = note

        self.__evaluation__ = pandas.concat([self.__evaluation__, evaluation_metrics], axis=0).reset_index(drop=True) if hasattr(self, '__evaluation__') else evaluation_metrics
        self.__dataset__ = y # only lastest dataset

        return self

    @property
    def model(self):
        return self.__model__

    @property
    def evaluation(self):
        logger['mlops'].info(f'[METRICS]{self.__evaluation__.columns.tolist()}')
        return self.__evaluation__

    @property
    def history(self):
        logger['mlops'].info(f'[MODEL] trigger.history[idx] means stored model, Find the histry_index on the trigger.evaluation.')
        return self.__history__
    
    @property
    def dataset(self):
        return self.__dataset__

    def data_loader(self, domain):
        logger['mlops'].info(f'[MODEL] Only latest dataset is supported.')
        return self.__dataset__[domain]


@TrainScenario()
def equip(model):
    trigger = Trigger(model)
    return trigger

