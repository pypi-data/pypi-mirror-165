from ..logging_system import logger
from .model_frameworks import *

from functools import wraps
from importlib import import_module
import os
import re
from datetime import datetime
from shutil import copyfile
from copy import deepcopy
import numpy as np
import pandas as pd
import joblib

from sklearn.metrics import cohen_kappa_score, jaccard_score, accuracy_score, balanced_accuracy_score, recall_score, precision_score, matthews_corrcoef, f1_score, fbeta_score, classification_report
from sklearn.metrics import explained_variance_score, max_error, mean_absolute_error, mean_squared_error, mean_squared_log_error, median_absolute_error, r2_score, mean_poisson_deviance, mean_gamma_deviance, mean_absolute_percentage_error
saving_time_format = '%Y%m%d_%H%M%S_%f'


class PredictResult:
    class CLSEvaluation:
        def __init__(self, *args, **kwargs):
            self.pr_args = args
            self.pr_kwargs = kwargs

        def __call__(self, func):
            @wraps(func)
            def evaluation(mlops_obj, *args, **kwargs):
                y_true, y_pred = func(mlops_obj, *args, **kwargs)
                metric = self.cls_evaluation(y_true, y_pred)
                metric = metric.rename(index={0:mlops_obj._model_name}).reset_index().rename(columns={'index':'model_name'})
                metric['t_end_time'] = mlops_obj._t_identifier

                if 'verbose' in kwargs.keys():
                    if kwargs['verbose']:
                        print(classification_report(y_true, y_pred))
                return metric
            return evaluation
        
        def cls_evaluation(self, y_true, y_pred):
            comparison = pd.DataFrame({'y_true':y_true, 'y_pred':y_pred})

            metric = dict()
            metric['cohen_kappa_score'] = [ cohen_kappa_score(comparison['y_true'], comparison['y_pred'], weights=None) ]
            metric['cohen_kappa_score_with_linear_weight'] = [cohen_kappa_score(comparison['y_true'], comparison['y_pred'], weights='linear')]
            metric['cohen_kappa_score_with_quadratic_weight'] = [cohen_kappa_score(comparison['y_true'], comparison['y_pred'], weights='quadratic')]
            metric['jaccard_score_with_micro_average'] = [jaccard_score(comparison['y_true'], comparison['y_pred'], average='micro')]
            metric['jaccard_score_with_macro_average'] = [jaccard_score(comparison['y_true'], comparison['y_pred'], average='macro')]
            metric['jaccard_score_with_weighted_average'] = [jaccard_score(comparison['y_true'], comparison['y_pred'], average='weighted')]
            metric['accuracy'] = [accuracy_score(comparison['y_true'], comparison['y_pred'], normalize=True)]
            metric['balanced_accuracy_score'] = [balanced_accuracy_score(comparison['y_true'], comparison['y_pred'])]
            metric['precision_with_micro_average'] = [precision_score(comparison['y_true'], comparison['y_pred'], average='micro')]
            metric['precision_with_macro_average'] = [precision_score(comparison['y_true'], comparison['y_pred'], average='macro')]
            metric['precision_with_weighted_average'] = [precision_score(comparison['y_true'], comparison['y_pred'], average='weighted')]
            metric['recall_with_micro_average'] = [recall_score(comparison['y_true'], comparison['y_pred'], average='micro')]
            metric['recall_with_macro_average'] = [recall_score(comparison['y_true'], comparison['y_pred'], average='macro')]
            metric['recall_with_weighted_average'] = [recall_score(comparison['y_true'], comparison['y_pred'], average='weighted')]
            metric['f1_with_micro_average'] = [f1_score(comparison['y_true'], comparison['y_pred'], average='micro')]
            metric['f1_with_macro_average'] = [f1_score(comparison['y_true'], comparison['y_pred'], average='macro')]
            metric['f1_with_weighted_average'] = [f1_score(comparison['y_true'], comparison['y_pred'], average='weighted')]
            metric['fbeta1_score_with_micro_average'] = [fbeta_score(comparison['y_true'], comparison['y_pred'], beta=1, average='micro')]
            metric['fbeta1_score_with_macro_average'] = [fbeta_score(comparison['y_true'], comparison['y_pred'], beta=1, average='macro')]
            metric['fbeta1_score_with_weighted_average'] = [fbeta_score(comparison['y_true'], comparison['y_pred'], beta=1, average='weighted')]
            metric['fbeta2_score_with_micro_average'] = [fbeta_score(comparison['y_true'], comparison['y_pred'], beta=2, average='micro')]
            metric['fbeta2_score_with_macro_average'] = [fbeta_score(comparison['y_true'], comparison['y_pred'], beta=2, average='macro')]
            metric['fbeta2_score_with_weighted_average'] = [fbeta_score(comparison['y_true'], comparison['y_pred'], beta=2, average='weighted')]
            metric['matthews_corrcoef'] = [matthews_corrcoef(comparison['y_true'], comparison['y_pred'])]
            metric = pd.DataFrame(data=metric)

            return metric

    class REGEvaluation:
        def __init__(self, *args, **kwargs):
            self.pr_args = args
            self.pr_kwargs = kwargs

        def __call__(self, func):
            @wraps(func)
            def evaluation(mlops_obj, *args, **kwargs):
                y_true, y_pred = func(mlops_obj, *args, **kwargs)
                metric = self.reg_evaluation(y_true, y_pred)
                metric = metric.rename(index={0:mlops_obj._model_name}).reset_index().rename(columns={'index':'model_name'})
                metric['t_end_time'] = mlops_obj._t_identifier
                return metric
            return evaluation
        
        def reg_evaluation(self, y_true, y_pred):
            comparison = pd.DataFrame({'y_true':y_true, 'y_pred':y_pred})
            metric = dict()
            metric['explained_cariance_score'] = [explained_variance_score(comparison['y_true'], comparison['y_pred'])]
            metric['max_error'] = [max_error(comparison['y_true'], comparison['y_pred'])]
            metric['mean_absolute_error'] = [mean_absolute_error(comparison['y_true'], comparison['y_pred'])]
            metric['mean_squared_error'] = [mean_squared_error(comparison['y_true'], comparison['y_pred'])]
            metric['median_absolute_error'] = [median_absolute_error(comparison['y_true'], comparison['y_pred'])]
            metric['r2_score'] = [r2_score(comparison['y_true'], comparison['y_pred'])]
            metric['mean_absolute_percentage_error'] = [mean_absolute_percentage_error(comparison['y_true'], comparison['y_pred'])]
            metric = pd.DataFrame(data=metric)
            return metric

    class CLSPrediction:
        def __init__(self, *args, **kwargs):
            self.pr_args = args
            self.pr_kwargs = kwargs

        def __call__(self, func):
            @wraps(func)
            def prediction(mlops_obj, *args, **kwargs):
                y_true, y_pred = func(mlops_obj, *args, **kwargs)
                if kwargs['verbose']:
                    print(classification_report(y_true, y_pred))
                return y_true, y_pred
            return prediction

    class REGPrediction:
        def __init__(self, *args, **kwargs):
            self.pr_args = args
            self.pr_kwargs = kwargs

        def __call__(self, func):
            @wraps(func)
            def prediction(mlops_obj, *args, **kwargs):
                return func(mlops_obj, *args, **kwargs)
            return prediction
        
    class CLSVisualization:
        def __init__(self, *args, **kwargs):
            self.pr_args = args
            self.pr_kwargs = kwargs

        def __call__(self, func):
            @wraps(func)
            def visualization(mlops_obj, *args, **kwargs):
                y_true, y_pred = func(mlops_obj, *args, **kwargs)
                if kwargs['verbose']:
                    print(classification_report(y_true, y_pred))
                return y_true, y_pred
            return visualization

    class REGVisualization:
        def __init__(self, *args, **kwargs):
            self.pr_args = args
            self.pr_kwargs = kwargs

        def __call__(self, func):
            @wraps(func)
            def visualization(mlops_obj, *args, **kwargs):
                return func(mlops_obj, *args, **kwargs)
            return visualization


class MLTrigger(PredictResult):
    def __init__(self):
        self.sklearn = FrameworkSklearn()
        self.xgboost = FrameworkXgboost()
        self.lightgbm = FrameworkLightgbm()
        self.catboost = FrameworkCatboost()
        self.supported_frameworks = ['sklearn', 'xgboost', 'lightgbm', 'catboost']

    def preprocessing(self, entry_points=None):
        if entry_points is None:
            self._user_preprocessors = self._user_datasets

        # User Interfaces for Dataset
        if isinstance(self._user_preprocessors, tuple):
            if len(self._user_preprocessors) == 2 and isinstance(self._user_preprocessors[1], str):
                # mlops.dataset = (dataset, 'dataset_comment')  >>>  [(dataset, 'dataset_comment')]
                self._user_preprocessors = [self._user_preprocessors]
        if not isinstance(self._user_preprocessors, (list, tuple)):
            # mlops.dataset = dataset  >>>  [dataset]
            self._user_preprocessors = [self._user_preprocessors]
        
        user_datasets = list() 
        self.preprocessing_information = list()
        for idx_preprocessor, preprocessor in enumerate(self._user_preprocessors):
            if isinstance(preprocessor, tuple):
                if len(preprocessor) == 1:
                    # >>> [(dataset0, ), (dataset1, ), (dataset2, ), ...]
                    preprocessor, d_comment = (preprocessor[0], None)
                elif len(preprocessor) == 2:
                    # >>> [(dataset0, 'dataset0_comment'), (dataset1, 'dataset1_comment'), (dataset2, 'dataset2_comment'), ...]
                    preprocessor, d_comment = preprocessor
                else:
                    raise TypeError('TypeError')
            else:
                # >>> [dataset0, dataset1, dataset2, ...]
                d_comment = None
            
            if not isinstance(preprocessor, pd.DataFrame):
                dataset = preprocessor()
                idx_dataset = idx_preprocessor
            else:
                dataset = preprocessor
                idx_dataset = idx_preprocessor

            assert isinstance(dataset, pd.DataFrame), f'Your dataset{idx_dataset} must be type of the pandas.core.frame.DataFrame.'
            assert 'target' in dataset.columns, f"Your dataset{idx_dataset} must include one 'target' column."
            saving_time = datetime.today().strftime(saving_time_format)
            dataset_name = f'{dataset.columns.name}.csv' if dataset.columns.name else f'dataset{idx_dataset}.csv'
            dataset_saving_name = saving_time + '-' + dataset_name
            saving_path = os.path.join(self.core['FS'].path, dataset_saving_name)

            dataset.to_csv(saving_path, index=False)
            user_datasets.append(dataset)
            if entry_points:
                self.preprocessing_information.append((idx_dataset, dataset_saving_name, saving_time, d_comment, entry_points[idx_dataset]))
            else:
                self.preprocessing_information.append((idx_dataset, dataset_saving_name, saving_time, d_comment, entry_points))

        self._user_datasets = user_datasets
        self._dataset = user_datasets[-1] # last dataset
        return self._dataset.copy()

    def learning(self, entry_points=None):
        self._user_dataset_names = list() 
        self._user_model_names = list() 

        # User Interfaces for Model
        if isinstance(self._user_models, tuple):
            if len(self._user_models) == 2 and isinstance(self._user_models[1], str):
                # mlops.model = (model, 'model_comment')  >>>  [(model, 'model_comment')]
                self._user_models = [self._user_models]
        if not isinstance(self._user_models, (list, tuple)):
            # mlops.model = model  >>>  [model]
            self._user_models = [self._user_models]

        self.training_information = dict()
        self.training_information['L1'] = list() # for self._user_models

        for idx_model, user_model in enumerate(self._user_models):
            if isinstance(user_model, tuple):
                if len(user_model) == 1:
                    # >>> [(model0, ), (model1, ), (model2, ), ...]
                    user_model = user_model[0]
                if len(user_model) == 2:
                    # >>> [(model0, 'model0_comment'), (model1, 'model1_comment'), (model2, 'model2_comment'), ...]
                    user_model, t_comment = user_model
            else:
                # >>> [model0, model1, model2, ...]
                t_comment = None
            
            for idx_dataset, dataset in enumerate(self._user_datasets):
                if entry_points: 
                    if idx_model == idx_dataset:
                        pass
                    else:
                        continue

                # define self._user_dataset_names
                if idx_model == 0:
                    self._user_dataset_names.append(dataset.columns.name)

                _break_l1 = False
                _break_l2 = False
                # Requires optimization on code
                for supported_framework in self.supported_frameworks:
                    for module_name, models in getattr(self, supported_framework).modules.items():
                        for model_name in models:
                            if isinstance(user_model, getattr(self, supported_framework).get_model_class(supported_framework, module_name, model_name)):
                                framework_name = supported_framework
                                framework = getattr(self, framework_name)
                                
                                # training job
                                trainingjob_start_time = datetime.today().strftime(saving_time_format)
                                if not entry_points:
                                    model = framework.train(user_model, dataset)
                                else:
                                    # entrypoint
                                    self.entry_point = list(self._user_entry_points.values())[idx_model]
                                    model = self.entry_point.train(user_model, dataset)

                                trainingjob_end_time = datetime.today().strftime(saving_time_format)
                                saving_name = trainingjob_end_time + '-' + f'{model_name}'
                                training_info_detail = framework.save_insidemodel(model, mlops_path=self.core['MR'].path, saving_name=saving_name)
                                training_info_detail['training_start_time'] = trainingjob_start_time
                                training_info_detail['training_end_time'] = trainingjob_end_time
                                training_info_detail['t_comment'] = t_comment
                                _break_l1 = True
                                break
                        if _break_l1:
                            _break_l2 = True
                            break
                    if _break_l2:
                        self._dataset_idx = idx_dataset
                        self._dataset = dataset
                        self._model = model
                        self._model_name = model_name
                        self._model_idx = idx_model
                        self._framework = framework
                        self._framework_name = framework_name
                        self._t_identifier =  trainingjob_end_time # training identifier for model and dataset <=> self._training_info_detail['training_end_time']
                        self._training_info_detail = training_info_detail
                        break
                self.training_information['L1'].append((
                    self._model_idx, self._dataset_idx, self._model_name, self._framework_name, 
                    deepcopy(self._model), self._framework, 
                    self._training_info_detail['training_start_time'], 
                    self._training_info_detail['training_end_time'], 
                    self._training_info_detail['saving_model_name'],
                    self._training_info_detail['t_comment'],
                    ))
            self._user_model_names.append(model_name)

        info_train = pd.DataFrame(
                data=list(map(lambda x: (x[0], x[1], x[2], x[3], x[6], x[7], x[8], x[9]), self.training_information['L1'])), 
                columns=self._insidelog_entities['train'])
        info_dataset = pd.DataFrame(
                data=self.preprocessing_information, 
                columns=self._insidelog_entities['preprocessing'])

        self.inside_board = pd.merge(info_train, info_dataset, how='left', on='d_idx')
        self.inside_board['from'] = 'inside'
        mlops_log = self.inside_board.copy()

        logging_history = list(filter(lambda x: re.search(self._insidelog_name[:-4], x), self.core['MS'].listdir()))
        logging_path = os.path.join(self.core['MS'].path, self._insidelog_name)
        if bool(len(logging_history)):
            mlops_log = mlops_log.append(pd.read_csv(logging_path), ignore_index=True)
        self.insidelog = mlops_log
        self.insidelog.to_csv(logging_path, index=False)
        self._model = self.training_information['L1'][-1][4] # last model
        return deepcopy(self._model)

    def predictionX(self, X=None):
        # case: prediction
        if X is None:
            # prediction()
            X = self._dataset.loc[:, self._dataset.columns != 'target']
        elif isinstance(X, slice):
            # prediction(slice(10))
            X = self._dataset.loc[X, self._dataset.columns != 'target']
        return self._framework.predict(self._model, X)
    
    def predictionXy(self, dataset=None):
        # case: inference
        if dataset is None:
            # inference()
            X = self._dataset.loc[:, self._dataset.columns != 'target']
            y = self._dataset.loc[:, self._dataset.columns == 'target']
        elif isinstance(dataset, slice):
            # inference(slice(10))
            X = self._dataset.loc[dataset, self._dataset.columns != 'target']
            y = self._dataset.loc[dataset, self._dataset.columns == 'target']
        else:
            # inference(dataset)
            X = dataset.loc[:, dataset.columns != 'target']
            y = dataset.loc[:, dataset.columns == 'target']

        y_true = y.values.squeeze()
        y_pred = self._framework.predict(self._model, X)
        return y_true, y_pred

    @PredictResult.CLSEvaluation(description='classification evaluation')
    def cls_evaluation(self, dataset, verbose=False):
        return self.predictionXy(dataset)

    @PredictResult.REGEvaluation(description='regression evaluation')
    def reg_evaluation(self, dataset, verbose=False):
        return self.predictionXy(dataset)

    @PredictResult.CLSPrediction(description='classification prediction')
    def cls_prediction(self, dataset, verbose=False):
        return self.predictionXy(dataset)

    @PredictResult.REGPrediction(description='regression prediction')
    def reg_prediction(self, dataset, verbose=False):
        return self.predictionXy(dataset)

    @PredictResult.CLSVisualization(description='classification visualization')
    def cls_visualization(self, dataset, verbose=False):
        return self.predictionXy(dataset)

    @PredictResult.REGVisualization(description='regression visualization')
    def reg_visualization(self, dataset, verbose=False):
        return self.predictionXy(dataset)

    def get_model(self, model_registry_path):
        return self._framework.upload(model_registry_path)
    
    def put_model(self, model, model_registry_path):
        outsidelog_path = os.path.join(self.core['MS'].path, self._outsidelog_name)
        return self._framework.save_outsidemodel(model, model_registry_path, outsidelog_path)


class TabularMLOps(MLTrigger):
    def __init__(self, mlops_bs):
        super(TabularMLOps, self).__init__()
        self.core = mlops_bs.core
        self.__dataset = None
        self.__model = None
        
        # usage with the 'inside_board' definition inside the 'def learning' on the class 'MLTrigger'
        # self.inside_board > self.insidelog
        self._insidelog_name = 'mlops_insidelog.csv'
        self._insidelog_entities = dict() # columns of insidelog
        self._insidelog_entities['preprocessing'] = ['d_idx', 'd_saving_name', 'd_saving_time', 'd_comment'] + ['c_entry_point']
        self._insidelog_entities['train'] = ['t_idx', 'd_idx', 'model_name', 'framework_name', 't_start_time', 't_end_time', 't_saving_name', 't_comment']
        self._insidelog_entities['logtype'] = ['from']
        self._insidelog_columns = self._insidelog_entities['train'] + self._insidelog_entities['preprocessing'][1:] + self._insidelog_entities['logtype']
        
        # usage with the 'appending_board' definition inside the 'def storing_model'
        self._outsidelog_name = 'mlops_outsidelog.csv'
        self._outsidelog_columns = ['t_idx', 'model_name', 'framework_name', 't_end_time', 't_saving_name', 'from', 'comment']

        # usage with the 'self.commitlog' definition inside the 'def codecommit'
        self._commitlog_name = 'mlops_commitlog.csv'
        self._commitlog_columns = self._insidelog_columns

        # usage with the 'self.prediction' definition inside the 'def inference' : self._metric
        self._metriclog0_name = 'mlops_metriclog0.csv'

        # insidelog
        logging_history = list(filter(lambda x: re.search(self._insidelog_name[:-4], x), self.core['MS'].listdir()))
        logging_path = os.path.join(self.core['MS'].path, self._insidelog_name)
        if bool(len(logging_history)):
            self.insidelog = pd.read_csv(logging_path)
        else:
            self.insidelog = pd.DataFrame(columns=self._insidelog_columns)
        
        # outsidelog
        logging_history = list(filter(lambda x: re.search(self._outsidelog_name[:-4], x), self.core['MS'].listdir()))
        logging_path = os.path.join(self.core['MS'].path, self._outsidelog_name)
        if bool(len(logging_history)):
            self.outsidelog = pd.read_csv(logging_path)
        else:
            self.outsidelog = pd.DataFrame(columns=self._outsidelog_columns)
        
        # commitlog
        logging_history = list(filter(lambda x: re.search(self._commitlog_name[:-4], x), self.core['MS'].listdir()))
        logging_path = os.path.join(self.core['MS'].path, self._commitlog_name)
        if bool(len(logging_history)):
            self.commitlog = pd.read_csv(logging_path)
        else:
            self.commitlog = pd.DataFrame(columns=self._commitlog_columns)
        
        # metriclog0
        logging_history = list(filter(lambda x: re.search(self._metriclog0_name[:-4], x), self.core['MS'].listdir()))
        logging_path = os.path.join(self.core['MS'].path, self._metriclog0_name)
        if bool(len(logging_history)):
            self._metric = pd.read_csv(logging_path)


    @property
    def dataset(self):
        return self.__dataset

    @dataset.setter
    def dataset(self, datasets):
        self._user_datasets = datasets
        self.__dataset = self.preprocessing()
    
    @property
    def model(self):
        return self.__model
    
    @model.setter
    def model(self, models):
        self._user_models = models
        self.__model = self.learning()
    
    def prediction(self, X=None):
        return super(TabularMLOps, self).predictionX(X=X)

    def inference(self, dataset=None, comment:str=None, learning_problem_type='cls', mode='evaluation', verbose=True):
        if mode == 'evaluation':
            if dataset is None:
                self._domain_begin = self._dataset.index[0]
                self._domain_end = self._dataset.index[-1]
                self._domain_size = self._dataset.shape[0]
            elif isinstance(dataset, slice):
                self._domain_begin = self._dataset.loc[dataset].index[0]
                self._domain_end = self._dataset.loc[dataset].index[-1]
                if getattr(dataset, 'start') is None:
                    self._domain_size = dataset.stop
                else:
                    if getattr(dataset, 'step') is None:
                        self._domain_size = dataset.stop - dataset.start
                    else:
                        # positive case
                        self._domain_size = int((dataset.stop - dataset.start)/dataset.step) + 1

            else:
                self._domain_begin = dataset.index[0]
                self._domain_end = dataset.index[-1]
                self._domain_size = dataset.shape[0]
            metric = getattr(super(TabularMLOps, self), learning_problem_type+'_evaluation')(dataset=dataset, verbose=verbose)
            raw_metric_columns = metric.columns.tolist()
            metric['e_saving_time'] = [ datetime.today().strftime(saving_time_format) ]
            metric['e_domain_size'] = [ self._domain_size ]
            metric['e_domain_begin'] = [ self._domain_begin ]
            metric['e_domain_end'] = [ self._domain_end ]

            e_type = 'Classification' if learning_problem_type == 'cls' else 'Regression' if learning_problem_type == 'reg' else None
            metric['e_type'] = [ e_type ] 
            metric['e_comment'] = [ comment ]

            if not hasattr(self, '_metric'):
                self._metric = metric.iloc[:0].copy()
            self._metric = metric.append(self._metric)
            self._metric.to_csv(os.path.join(self.core['MS'].path, self._metriclog0_name), index=False)
            
            # reordeing columns in evaluation table
            reordering_column = raw_metric_columns.pop(raw_metric_columns.index('t_end_time'))
            return self._metric.loc[lambda x:x.e_type == e_type, ['e_saving_time'] + raw_metric_columns + ['e_domain_size', 'e_domain_begin', 'e_domain_end', 'e_type', 'e_comment', reordering_column] ].reset_index(drop=True)

        elif mode == 'prediction':
            y_true, y_pred = getattr(super(TabularMLOps, self), learning_problem_type+'_prediction')(dataset=dataset, verbose=verbose)
            return y_true, y_pred

        elif mode == 'visualization':
            return getattr(super(TabularMLOps, self), learning_problem_type+'_visualization')(dataset=dataset, verbose=verbose) # None

        else:
            return

    def training_board(self, log=None):
        if not log:
            # D[self._user_datasets] X D[self._user_models]
            return self.inside_board.copy()
        elif log == 'inside':
            # All history through mlops.dataset, mlops.model
            return self.insidelog.copy()
        elif log == 'outside':
            # All history through mlops.storing_model
            return self.outsidelog.copy()
        elif log == 'commit':
            return self.commitlog.copy()
        elif log == 'metric':
            return self._metric.copy()
        else:
            return self.inside_board.copy()

    def feature_choice(self, idx:int=-1):
        if isinstance(idx, int):
            self._dataset_num = len(self._user_datasets)
            if idx == -1:
                self._dataset_idx = self._dataset_num + idx
            else:
                self._dataset_idx = idx
            self._dataset = self._user_datasets[idx]
            self.__dataset = self._dataset.copy()

        elif isinstance(idx, str):
            saving_dataset_name = idx
            dataset_path = os.path.join(self.core['FS'].path, saving_dataset_name)

            dataset = pd.read_csv(dataset_path)
            dataset.columns.name = saving_dataset_name
            self._dataset = dataset.copy()
            self._dataset_idx = self.insidelog.loc[lambda x: x.d_saving_name == saving_dataset_name, 'd_idx'].iloc[0]
            self.__dataset = self._dataset.copy()

        else:
            return self
        
        # mlops info
        if hasattr(self, '_user_dataset_names'):
            logger['mlops'].info(f'The {self._user_dataset_names[idx]} dataset[{idx}] is selected!' + ' | ' + ', '.join(list(map(lambda x: f'[{str(x[0])}]' + str(x[1]), enumerate(self._user_dataset_names)))))
        else:
            logger['mlops'].info(f'The {self._dataset.columns.name} dataset is selected from feature store!')
        return self

    def model_choice(self, idx:int=-1):

        if isinstance(idx, int):
            self._model_num = len(self._user_models)
            if idx == -1:
                self._model_idx = self._model_num + idx
            else:
                self._model_idx = idx
            self._framework_name = self.inside_board.loc[lambda x: (x.t_idx == self._model_idx)&(x.d_idx == self._dataset_idx), 'framework_name'].item()
            self._model_name = self.inside_board.loc[lambda x: (x.t_idx == self._model_idx)&(x.d_idx == self._dataset_idx), 'model_name'].item()
            self._framework = getattr(self, self._framework_name)
            self._training_info_detail = {
                    'training_start_time': self.inside_board.loc[lambda x: (x.t_idx == self._model_idx)&(x.d_idx == self._dataset_idx), 't_start_time'],
                    'training_end_time': self.inside_board.loc[lambda x: (x.t_idx == self._model_idx)&(x.d_idx == self._dataset_idx), 't_end_time'],
                    'saving_model_name': self.inside_board.loc[lambda x: (x.t_idx == self._model_idx)&(x.d_idx == self._dataset_idx), 't_saving_name']
                    }
            self._model = self.training_information['L1'][self._dataset_num*(self._model_idx) + self._dataset_idx][4]
            self.__model = deepcopy(self._model)

        elif isinstance(idx, str):
            saving_model_name = idx
            insidelog_frame = self.insidelog.loc[lambda x: x.t_saving_name == saving_model_name]
            outsidelog_frame = self.outsidelog.loc[lambda x: x.t_saving_name == saving_model_name]
            if insidelog_frame.shape[0] == 1:
                self._framework_name = insidelog_frame['framework_name'].item()
                self._model_name = insidelog_frame['model_name'].item()
                
                if not insidelog_frame['c_entry_point'].isnull().item():
                    mlops_entry_point = insidelog_frame['c_entry_point'].item()
                    self.entry_point = EntryPoint(os.path.join(self.core['SR'].path, mlops_entry_point), from_source_repo=True)

            elif outsidelog_frame.shape[0] == 1:
                self._framework_name = outsidelog_frame['framework_name'].item()
                self._model_name = outsidelog_frame['model_name'].item()
            self._framework = getattr(self, self._framework_name)
            model_path = os.path.join(self.core['MR'].path, saving_model_name)
            self._model = self.get_model(model_path)
            self.__model = deepcopy(self._model)

        else:
            return self
        
        # mlops info
        if hasattr(self, '_user_model_names'):
            if isinstance(idx, int):
                logger['mlops'].info(f'The {self._user_model_names[idx]} model[{idx}] is selected in mlops!' + ' | ' + ', '.join(list(map(lambda x: f'[{str(x[0])}]' + str(x[1]), enumerate(self._user_model_names)))))
            else:
                logger['mlops'].info(f'The model {idx} is selected in mlops system!' )
        else:
            logger['mlops'].info(f'The {self._model_name} model is selected from model registry in mlops system!')
        return self

    def drawup_dataset(self, name:str):
        # with change of the dataset selection inside mlops (like feature_choice)
        dataset = pd.read_csv(os.path.join(self.core['FS'].path, name))
        dataset.columns.name = name

        logger['mlops'].info(f'The {name} dataset is not yet selected in mlops system!')
        return dataset.copy()

    def drawup_model(self, name:str):
        # with change of the model selection inside mlops (like model_choice)
        insidelog_frame = self.insidelog.loc[lambda x: x.t_saving_name == name]
        outsidelog_frame = self.outsidelog.loc[lambda x: x.t_saving_name == name]
        if insidelog_frame.shape[0] == 1:
            self._framework_name = insidelog_frame['framework_name'].item()
            self._model_name = insidelog_frame['model_name'].item()
        elif outsidelog_frame.shape[0] == 1:
            self._framework_name = outsidelog_frame['framework_name'].item()
            self._model_name = outsidelog_frame['model_name'].item()
        else:
            print('Not matched!')
            return None
        self._framework = getattr(self, self._framework_name)
        model_path = os.path.join(self.core['MR'].path, name)

        logger['mlops'].info(f'The {self._model_name} model is not yet selected in mlops system!')
        return self.get_model(model_path)
 
    def drawup_source(self, name):
        copyfile(os.path.join(self.core['SR'].path, name), name)

    def display_source(self, name):
        source_code_in_source_repository = os.path.join(self.core['SR'].path, name)
        with open(source_code_in_source_repository, 'r') as f:
            print(f.read())

    def storing_model(self, user_model, comment=None):
        """[mlops]MODEL"""
        # self._framework_name
        # self._framework
        # self._model
        # self._model_name

        """[mlops]TRAINING"""
        # self._t_identifier

        framework = None
        framework_name = None

        _break_l1 = False
        _break_l2 = False
        for supported_framework in self.supported_frameworks:
            for module_name, models in getattr(self, supported_framework).modules.items():
                for model_name in models:
                    if isinstance(user_model, getattr(self, supported_framework).get_model_class(supported_framework, module_name, model_name)):
                        framework_name = supported_framework
                        framework = getattr(self, framework_name)
                        user_model_name = model_name

        if not framework_name:
            return
        else:
            self._framework_name = framework_name
            self._framework = framework
            self._model = user_model
            self._model_name = user_model_name

        # saving model with refreshing outsidelog
        saving_time = datetime.today().strftime(saving_time_format); 
        model_registry_path = os.path.join(self.core['MR'].path, saving_time + '-' + self._model_name)
        
        # define mlops training_identifier
        self._t_identifier = saving_time

        # define the outsidelog elements on logfile
        oe_t_idx = self.outsidelog.shape[0]
        oe_model_name = self._model_name
        oe_framework_name = self._framework_name
        oe_t_end_time = saving_time
        oe_t_saving_name = saving_time + '-' + self._model_name
        oe_from = 'outside'
        oe_comment = comment

        appending_board = pd.DataFrame(
                columns=self._outsidelog_columns,
                data=[[oe_t_idx, oe_model_name, oe_framework_name, oe_t_end_time, oe_t_saving_name, oe_from, oe_comment]])
        self.outsidelog = appending_board.append(self.outsidelog, ignore_index=True)
        self.outsidelog.to_csv(os.path.join(self.core['MS'].path, self._outsidelog_name), index=False)
        self.put_model(user_model, model_registry_path)
        self.outsidelog = pd.read_csv(os.path.join(self.core['MS'].path, self._outsidelog_name))
        return self.outsidelog 

    def codecommit(self, entry_points, upload=True):
        """[mlops]DATASET"""
        # self._dataset

        """[mlops]MODEL"""
        # self._framework_name
        # self._framework
        # self._model
        # self._model_name
        
        """[mlops]TRAINING"""
        # self._t_identifier
        
        entry_point_sets = list()
        if isinstance(entry_points, str):
            # >>> entry_points = '*.py'
            entry_point, d_comment, t_comment = (entry_points, None, None)
            entry_point_sets.append((entry_point, d_comment, t_comment))
        elif isinstance(entry_points, (list, tuple)):
            if len(list(filter(lambda x: isinstance(x, str), entry_points))) == len(entry_points):
                if len(list(filter(lambda x: x.endswith('.py') , entry_points))) == len(entry_points):
                    # >>> entry_points = ['*.py', '*.py', '*.py', ...]
                    for entry_point in entry_points:
                        entry_point, d_comment, t_comment = (entry_point, None, None)
                        entry_point_sets.append((entry_point, d_comment, t_comment))
                else:
                    if len(entry_points) == 2:
                        # >>> entry_points = ['*.py', 'comment']
                        entry_point, d_comment, t_comment = (entry_point[0], entry_points[-1], entry_points[-1])
                    elif len(entry_points) >= 3:
                        # >>> entry_points = ['*.py', 'd_comment', 't_comment']
                        entry_point, d_comment, t_comment = (entry_points[0], entry_points[1], entry_points[2])
                    else:
                        raise ValueError('ValueError')
                    entry_point_sets.append((entry_point, d_comment, t_comment))

            elif len(list(filter(lambda x: isinstance(x, (list, tuple)), entry_points))) == len(entry_points):
                # >>> entry_points = [('*.py', )]
                # >>> entry_points = [('*.py', 'comment')]
                # >>> entry_points = [('*.py', 'd_comment', 't_comment')]
                # >>> entry_points = [('code1.py', ), ('code2.py', 'comment2'), ('code3.py', 'd_comment3', 't_comment3')]

                for entry_point in entry_points:
                    if len(entry_point) == 1:
                        # >>> entry_points = [..., ('*.py', ), ...]
                        entry_point, d_comment, t_comment = (entry_point[0], None, None)
                    elif len(entry_point) == 2:
                        # >>> entry_points = [..., ('*.py', 'comment'), ...]
                        entry_point, d_comment, t_comment = (entry_point[0], entry_point[-1], entry_point[-1])
                    elif len(entry_point) >= 3:
                        # >>> entry_points = [..., ('*.py', 'd_comment', 't_comment'), ...]
                        entry_point, d_comment, t_comment = (entry_point[0], entry_point[1], entry_point[2])
                    else:
                        raise ValueError('ValueError')
                    entry_point_sets.append((entry_point, d_comment, t_comment))
            else:
                raise TypeError('TypeError')
        else:
            raise TypeError('TypeError')
        
        self._user_preprocessors = list()
        self._user_models = list()
        self._user_entry_points = dict()
        self._mlops_entry_points = list()
        for entry_point_set in entry_point_sets:
            entry_point, d_comment, t_comment = entry_point_set

            entry_point_obj = EntryPoint(entry_point)

            # reserving code
            reserving_path = os.path.join(self.core['SR'].path, entry_point_obj.mlops_entry_point)
            copyfile(entry_point, reserving_path)
            
            # define user dataset
            preprocessor = entry_point_obj.preprocessing                                   # mlops.entry_point.preprocessing > dataset = *.preprocessing()

            # define user model
            model = entry_point_obj.architecture()                                         # mlops.entry_point.architecture
            
            self._user_preprocessors.append((preprocessor, d_comment))
            self._user_models.append((model, t_comment))
            self._user_entry_points[entry_point_obj.entry_name] = entry_point_obj
            self._mlops_entry_points.append(entry_point_obj.mlops_entry_point)

        self.__dataset = self.preprocessing(entry_points=self._mlops_entry_points)
        self.__model = self.learning(entry_points=self._mlops_entry_points)             # mlops.entry_point.train

        self.commitlog = self.insidelog.loc[self.insidelog['c_entry_point'].dropna().index].reset_index(drop=True)
        self.commitlog.to_csv(os.path.join(self.core['MS'].path, self._commitlog_name), index=False)
        
        return self.commitlog

    def summary(self):
        return

    def feature_store(self):
        return self.core['FS']

    def model_registry(self):
        return self.core['MR']

    def source_repository(self):
        return self.core['SR']

    def metadata_store(self):
        return self.core['MS']

class EntryPoint:
    def __init__(self, entry_point, from_source_repo=False):
        self.entry_name = entry_point[:-3].replace(os.sep, '.') # *.*.*.py > *.*.*
        self.source = import_module(self.entry_name)

        if not from_source_repo:
            self.mlops_entry_point = datetime.today().strftime(saving_time_format) + '-' + entry_point
        else:
            self.mlops_entry_point = os.path.split(entry_point)[1]
        
        # Structured Functions
        assert hasattr(self.source, 'preprocessing') 
        assert hasattr(self.source, 'architecture') 
        assert hasattr(self.source, 'train') 
        self.preprocessing = getattr(self.source, 'preprocessing')  # return datasets
        self.architecture = getattr(self.source, 'architecture')    # return user_models
        self.train = getattr(self.source, 'train')                  # return model

        # Unstructured Functions
        if hasattr(self.source, 'predict'):
            self.predict = getattr(self.source, 'predict')
        if hasattr(self.source, 'evaluate'):
            self.evaluate = getattr(self.source, 'evaluate')            # return metrics
        if hasattr(self.source, 'report'):
            self.report = getattr(self.source, 'report')                # return report



