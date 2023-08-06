from ..logging_system import logger

import numpy
import pandas
from datetime import datetime
from sklearn.metrics import cohen_kappa_score, jaccard_score, accuracy_score, balanced_accuracy_score, recall_score, precision_score, matthews_corrcoef, f1_score, fbeta_score, classification_report
from sklearn.metrics import explained_variance_score, max_error, mean_absolute_error, mean_squared_error, mean_squared_log_error, median_absolute_error, r2_score, mean_poisson_deviance, mean_gamma_deviance, mean_absolute_percentage_error

class BinaryClassification:
    @classmethod
    def evaluation(cls, y_true, y_pred, y_prob=None):
        assert isinstance(y_true, (pandas.DataFrame, pandas.Series, numpy.ndarray))
        assert isinstance(y_pred, (pandas.DataFrame, pandas.Series, numpy.ndarray))
        y_true = numpy.array(y_true).squeeze()
        y_pred = numpy.array(y_pred).squeeze()

        if y_prob is not None:
            assert isinstance(y_prob, (pandas.DataFrame, pandas.Series, numpy.ndarray))
            y_prob = numpy.array(y_prob).squeeze()

        evaluation = dict(evaluation_time=datetime.now())
        comparison = pandas.DataFrame({'y_true':y_true, 'y_pred':y_pred})
        metric = dict()
        
        metric['count']           = [comparison['y_true'].shape[0]]
        metric['numclass']        = [comparison['y_true'].unique().shape[0]]
        metric['true']            = [(comparison['y_true'] == 1).sum()]
        metric['false']           = [(comparison['y_true'] == 0).sum()]
        metric['positive']        = [(comparison['y_pred'] == 1).sum()]
        metric['negative']        = [(comparison['y_pred'] == 0).sum()]
        metric['true_positive']   = [((comparison['y_true'] == 1)&(comparison['y_pred'] == 1)).sum()]
        metric['true_negative']   = [((comparison['y_true'] == 0)&(comparison['y_pred'] == 0)).sum()]
        metric['false_positive']  = [((comparison['y_true'] == 0)&(comparison['y_pred'] == 1)).sum()]
        metric['falese_negative'] = [((comparison['y_true'] == 1)&(comparison['y_pred'] == 0)).sum()]
        metric['cohen_kappa_score'] = [ cohen_kappa_score(comparison['y_true'], comparison['y_pred'], weights=None) ]
        metric['cohen_kappa_score_with_linear_weight'] = [cohen_kappa_score(comparison['y_true'], comparison['y_pred'], weights='linear')]
        metric['cohen_kappa_score_with_quadratic_weight'] = [cohen_kappa_score(comparison['y_true'], comparison['y_pred'], weights='quadratic')]
        metric['jaccard_score_with_micro_average'] = [jaccard_score(comparison['y_true'], comparison['y_pred'], average='micro')]
        metric['jaccard_score_with_weighted_average'] = [jaccard_score(comparison['y_true'], comparison['y_pred'], average='weighted')]
        metric['accuracy'] = [accuracy_score(comparison['y_true'], comparison['y_pred'], normalize=True)]
        metric['balanced_accuracy_score'] = [balanced_accuracy_score(comparison['y_true'], comparison['y_pred'])]
        metric['precision_with_micro_average'] = [precision_score(comparison['y_true'], comparison['y_pred'], average='micro')]
        metric['precision_with_weighted_average'] = [precision_score(comparison['y_true'], comparison['y_pred'], average='weighted')]
        metric['recall_with_micro_average'] = [recall_score(comparison['y_true'], comparison['y_pred'], average='micro')]
        metric['recall_with_weighted_average'] = [recall_score(comparison['y_true'], comparison['y_pred'], average='weighted')]
        metric['f1_with_micro_average'] = [f1_score(comparison['y_true'], comparison['y_pred'], average='micro')]
        metric['f1_with_weighted_average'] = [f1_score(comparison['y_true'], comparison['y_pred'], average='weighted')]
        metric['fbeta1_score_with_micro_average'] = [fbeta_score(comparison['y_true'], comparison['y_pred'], beta=1, average='micro')]
        metric['fbeta1_score_with_weighted_average'] = [fbeta_score(comparison['y_true'], comparison['y_pred'], beta=1, average='weighted')]
        metric['fbeta2_score_with_micro_average'] = [fbeta_score(comparison['y_true'], comparison['y_pred'], beta=2, average='micro')]
        metric['fbeta2_score_with_weighted_average'] = [fbeta_score(comparison['y_true'], comparison['y_pred'], beta=2, average='weighted')]
        metric['matthews_corrcoef'] = [matthews_corrcoef(comparison['y_true'], comparison['y_pred'])]
        evaluation.update(metric)
        
        # AUC Display
        if y_prob is not None:
            import matplotlib.pyplot as plt
            from sklearn.metrics import confusion_matrix, classification_report
            from sklearn.metrics import roc_curve, precision_recall_curve, auc

            confusion_matrix = confusion_matrix(y_true, y_pred)
            recall = confusion_matrix[1, 1]/(confusion_matrix[1, 0]+confusion_matrix[1, 1])
            fallout = confusion_matrix[0, 1]/(confusion_matrix[0, 0]+confusion_matrix[0, 1])
            precision = confusion_matrix[0, 0]/(confusion_matrix[0, 0]+confusion_matrix[1, 0])
            fpr, tpr1, thresholds1 = roc_curve(y_true, y_prob[:,1])
            ppv, tpr2, thresholds2 = precision_recall_curve(y_true, y_prob[:,1])

            # visualization
            logger['mlops'].info(f'ROC AUC:{auc(fpr, tpr1)}, PR AUC:{auc(tpr2, ppv)}')
            #print(classification_report(y_true, y_pred, target_names=['down', 'up']))
            plt.figure(figsize=(30, 5))

            ax0 = plt.subplot2grid((1,2), (0,0))
            ax1 = plt.subplot2grid((1,2), (0,1))

            ax0.plot(fpr, tpr1, 'ko-') # X-axis(fpr): fall-out / y-axis(tpr): recall
            ax0.plot([fallout], [recall], 'ko', ms=10)
            ax0.plot([0, 1], [0, 1], 'k--')
            ax0.set_xlabel('Fall-Out')
            ax0.set_ylabel('Recall')
            ax0.set_title('ROC AUC')
            ax0.grid(True)

            ax1.plot(tpr2, ppv, 'ko-') # X-axis(tpr): recall / y-axis(ppv): precision
            ax1.plot([recall], [precision], 'ko', ms=10)
            ax1.plot([0, 1], [1, 0], 'k--')
            ax1.set_xlabel('Recall')
            ax1.set_ylabel('Precision')
            ax1.set_title('PR AUC')
            ax1.grid(True)

            plt.tight_layout()

        return pandas.DataFrame(data=evaluation)
        

class MultiClassification:
    @classmethod
    def evaluation(cls, y_true, y_pred, y_prob=None):
        assert isinstance(y_true, (pandas.DataFrame, pandas.Series, numpy.ndarray))
        assert isinstance(y_pred, (pandas.DataFrame, pandas.Series, numpy.ndarray))
        y_true = numpy.array(y_true).squeeze()
        y_pred = numpy.array(y_pred).squeeze()

        if y_prob is not None:
            assert isinstance(y_prob, (pandas.DataFrame, pandas.Series, numpy.ndarray))
            y_prob = numpy.array(y_prob).squeeze()

        evaluation = dict(evaluation_time=datetime.now())
        comparison = pandas.DataFrame({'y_true':y_true, 'y_pred':y_pred})
        metric = dict()
        
        metric['count']           = [comparison['y_true'].shape[0]]
        metric['numclass']        = [comparison['y_true'].unique().shape[0]]
        for idx, class_instance in enumerate(sorted(comparison['y_true'].unique())):
            metric[f'num_true_ci{idx}']        = [(comparison['y_true'] == class_instance).sum()]
            metric[f'num_pred_ci{idx}']        = [(comparison['y_pred'] == class_instance).sum()]
            metric[f'true_positive_ci{idx}']   = [((comparison['y_true'] == class_instance)&(comparison['y_pred'] == class_instance)).sum()]
            metric[f'true_negative_ci{idx}']   = [((comparison['y_true'] == class_instance)&(comparison['y_pred'] != class_instance)).sum()]
            metric[f'false_positive_ci{idx}']  = [((comparison['y_true'] != class_instance)&(comparison['y_pred'] == class_instance)).sum()]
            metric[f'falese_negative_ci{idx}'] = [((comparison['y_true'] == class_instance)&(comparison['y_pred'] != class_instance)).sum()]
            metric[f'accuarcy_{idx}']  = [(metric[f'true_positive_ci{idx}']+metric[f'true_negative_ci{idx}'])/(metric[f'true_positive_ci{idx}']+metric[f'true_negative_ci{idx}']+metric[f'false_positive_ci{idx}']+metric[f'falese_negative_ci{idx}'])]
            metric[f'recall_{idx}']    = [(metric[f'true_positive_ci{idx}'])/(metric[f'true_positive_ci{idx}']+metric[f'true_negative_ci{idx}'])]
            metric[f'precision_{idx}'] = [(metric[f'true_positive_ci{idx}'])/(metric[f'true_positive_ci{idx}']+metric[f'false_positive_ci{idx}'])]
            metric[f'f1_{idx}']        = [(2*metric[f'precision_{idx}']*metric[f'recall_{idx}'])/(metric[f'precision_{idx}']+metric[f'recall_{idx}'])]

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
        evaluation.update(metric)
        
        # AUC Display
        if y_prob is not None:
            import matplotlib.pyplot as plt
            from sklearn.metrics import confusion_matrix, classification_report
            from sklearn.metrics import roc_curve, precision_recall_curve, auc

            def multiclass_roc_curve(y_true, y_prob):
                import numpy as np
                from sklearn.metrics import roc_curve, auc
                from sklearn.preprocessing import label_binarize
                y_enco = label_binarize(y_true, np.sort(np.unique(y_true)).tolist())

                fpr = dict()
                tpr = dict()
                thr = dict()
                auc_ = dict()
                for class_idx in range(np.unique(y_true).shape[0]):
                    fpr[class_idx], tpr[class_idx], thr[class_idx] = roc_curve(y_enco[:, class_idx], y_prob[:, class_idx])
                    auc_[class_idx] = auc(fpr[class_idx], tpr[class_idx])
                return fpr, tpr, thr, auc_

            def multiclass_pr_curve(y_true, y_prob):
                import numpy as np
                from sklearn.metrics import precision_recall_curve, auc
                from sklearn.preprocessing import label_binarize
                y_enco = label_binarize(y_true, np.sort(np.unique(y_true)).tolist())

                ppv = dict()
                tpr = dict()
                thr = dict()
                auc_ = dict()
                for class_idx in range(np.unique(y_true).shape[0]):
                    ppv[class_idx], tpr[class_idx], thr[class_idx] = precision_recall_curve(y_enco[:, class_idx], y_prob[:, class_idx])
                    auc_[class_idx] = auc(tpr[class_idx], ppv[class_idx])
                return ppv, tpr, thr, auc_

            fpr, tpr1, thr1, auc1 = multiclass_roc_curve(y_true, y_prob)
            ppv, tpr2, thr2, auc2 = multiclass_pr_curve(y_true, y_prob)

            # visualization
            plt.figure(figsize=(30, 5))
            ax0 = plt.subplot2grid((1,2), (0,0))
            ax1 = plt.subplot2grid((1,2), (0,1))
            for class_idx in range(numpy.unique(y_true).shape[0]):
                ax0.plot(fpr[class_idx], tpr1[class_idx], 'o-', ms=5, label=str(class_idx) + f' | {round(auc1[class_idx], 2)}')
                ax1.plot(tpr2[class_idx], ppv[class_idx], 'o-', ms=5, label=str(class_idx) + f' | {round(auc2[class_idx], 2)}')

            ax0.plot([0, 1], [0, 1], 'k--')
            ax0.set_xlabel('Fall-Out')
            ax0.set_ylabel('Recall')
            ax0.grid(True)
            ax0.legend()
            ax1.plot([0, 1], [1, 0], 'k--')
            ax1.set_xlabel('Recall')
            ax1.set_ylabel('Precision')
            ax1.grid(True)
            ax1.legend()

            plt.tight_layout()

        return pandas.DataFrame(data=evaluation)

class MultiLabelClassification:
    def __init__(self, y_true, y_pred, y_prob=None):
        pass

class ScalarRegression:
    @classmethod
    def evaluation(cls, y_true, y_pred):
        assert isinstance(y_true, (pandas.DataFrame, pandas.Series, numpy.ndarray))
        assert isinstance(y_pred, (pandas.DataFrame, pandas.Series, numpy.ndarray))
        
        evaluation_time=datetime.now()
        y_true = numpy.array(y_true).squeeze()
        y_pred = numpy.array(y_pred).squeeze()

        evaluation = dict(evaluation_time=evaluation_time)
        comparison = pandas.DataFrame({'y_true':y_true, 'y_pred':y_pred})
        metric = dict()

        metric['count']              = [comparison['y_true'].shape[0]]
        metric['true_min']           = [comparison['y_true'].min()]
        metric['true_25%']           = [numpy.percentile(comparison['y_true'], 25, axis=0)]
        metric['true_50%']           = [numpy.percentile(comparison['y_true'], 50, axis=0)]
        metric['true_75%']           = [numpy.percentile(comparison['y_true'], 75, axis=0)]
        metric['true_max']           = [comparison['y_true'].max()]
        metric['true_mean']          = [comparison['y_true'].mean()]
        metric['true_std']           = [comparison['y_true'].std()]
        metric['pred_min']           = [comparison['y_pred'].min()]
        metric['pred_25%']           = [numpy.percentile(comparison['y_pred'], 25, axis=0)]
        metric['pred_50%']           = [numpy.percentile(comparison['y_pred'], 50, axis=0)]
        metric['pred_75%']           = [numpy.percentile(comparison['y_pred'], 75, axis=0)]
        metric['pred_max']           = [comparison['y_pred'].max()]
        metric['pred_mean']          = [comparison['y_pred'].mean()]
        metric['pred_std']           = [comparison['y_pred'].std()]
        metric['min_diff']           = [(comparison['y_true'].min() - comparison['y_pred'].min())]
        metric['25%_diff']           = [numpy.percentile(comparison['y_true'] - comparison['y_pred'], 25, axis=0)]
        metric['50%_diff']           = [numpy.percentile(comparison['y_true'] - comparison['y_pred'], 50, axis=0)]
        metric['75%_diff']           = [numpy.percentile(comparison['y_true'] - comparison['y_pred'], 75, axis=0)]
        metric['max_diff']           = [(comparison['y_true'].max() - comparison['y_pred'].max())]
        metric['mean_diff']          = [(comparison['y_true'].mean() - comparison['y_pred'].mean())]
        metric['std_diff']           = [(comparison['y_true'].std() - comparison['y_pred'].std())]
        metric['min_rate']           = [(comparison['y_pred'].min() / comparison['y_true'].min())] if (comparison['y_true'].min() != 0) else [numpy.nan]
        metric['25%_rate']           = [numpy.percentile(comparison['y_pred'] / comparison['y_true'], 25, axis=0)]
        metric['50%_rate']           = [numpy.percentile(comparison['y_pred'] / comparison['y_true'], 50, axis=0)]
        metric['75%_rate']           = [numpy.percentile(comparison['y_pred'] / comparison['y_true'], 75, axis=0)]
        metric['max_rate']           = [(comparison['y_pred'].max() / comparison['y_true'].max())] if (comparison['y_true'].max() != 0) else [numpy.nan]
        metric['mean_rate']           = [(comparison['y_pred'].mean() / comparison['y_true'].mean())] if (comparison['y_true'].mean() != 0) else [numpy.nan]
        metric['std_rate']           = [(comparison['y_pred'].std() / comparison['y_true'].std())] if (comparison['y_true'].std() != 0) else [numpy.nan]
        metric['explained_cariance_score'] = [explained_variance_score(comparison['y_true'], comparison['y_pred'])]
        metric['max_error'] = [max_error(comparison['y_true'], comparison['y_pred'])]
        metric['mean_absolute_error'] = [mean_absolute_error(comparison['y_true'], comparison['y_pred'])]
        metric['mean_squared_error'] = [mean_squared_error(comparison['y_true'], comparison['y_pred'])]
        metric['median_absolute_error'] = [median_absolute_error(comparison['y_true'], comparison['y_pred'])]
        metric['r2_score'] = [r2_score(comparison['y_true'], comparison['y_pred'])]
        metric['mean_absolute_percentage_error'] = [mean_absolute_percentage_error(comparison['y_true'], comparison['y_pred'])]
        evaluation.update(metric)

        eval_dataframe = pandas.DataFrame(data=evaluation)
        return eval_dataframe


class VectorRegression:
    @classmethod
    def evaluation(cls, y_true, y_pred):
        assert isinstance(y_true, (pandas.DataFrame, pandas.Series, numpy.ndarray))
        assert isinstance(y_pred, (pandas.DataFrame, pandas.Series, numpy.ndarray))

        evaluation_time=datetime.now()
        y_true = numpy.array(y_true).squeeze()
        y_pred = numpy.array(y_pred).squeeze()
        
        for idx in range(y_true.shape[1]):
            evaluation = dict(evaluation_time=evaluation_time)
            comparison = pandas.DataFrame({'y_true':y_true[:, idx], 'y_pred':y_pred[:, idx]})
            metric = dict()
            metric['count']              = [comparison['y_true'].shape[0]]
            metric['true_min']           = [comparison['y_true'].min()]
            metric['true_25%']           = [numpy.percentile(comparison['y_true'], 25, axis=0)]
            metric['true_50%']           = [numpy.percentile(comparison['y_true'], 50, axis=0)]
            metric['true_75%']           = [numpy.percentile(comparison['y_true'], 75, axis=0)]
            metric['true_max']           = [comparison['y_true'].max()]
            metric['true_mean']          = [comparison['y_true'].mean()]
            metric['true_std']           = [comparison['y_true'].std()]
            metric['pred_min']           = [comparison['y_pred'].min()]
            metric['pred_25%']           = [numpy.percentile(comparison['y_pred'], 25, axis=0)]
            metric['pred_50%']           = [numpy.percentile(comparison['y_pred'], 50, axis=0)]
            metric['pred_75%']           = [numpy.percentile(comparison['y_pred'], 75, axis=0)]
            metric['pred_max']           = [comparison['y_pred'].max()]
            metric['pred_mean']          = [comparison['y_pred'].mean()]
            metric['pred_std']           = [comparison['y_pred'].std()]
            metric['min_diff']           = [(comparison['y_true'].min() - comparison['y_pred'].min())]
            metric['25%_diff']           = [numpy.percentile(comparison['y_true'] - comparison['y_pred'], 25, axis=0)]
            metric['50%_diff']           = [numpy.percentile(comparison['y_true'] - comparison['y_pred'], 50, axis=0)]
            metric['75%_diff']           = [numpy.percentile(comparison['y_true'] - comparison['y_pred'], 75, axis=0)]
            metric['max_diff']           = [(comparison['y_true'].max() - comparison['y_pred'].max())]
            metric['mean_diff']          = [(comparison['y_true'].mean() - comparison['y_pred'].mean())]
            metric['std_diff']           = [(comparison['y_true'].std() - comparison['y_pred'].std())]
            metric['min_rate']           = [(comparison['y_pred'].min() / comparison['y_true'].min())] if (comparison['y_true'].min() != 0) else [numpy.nan]
            metric['25%_rate']           = [numpy.percentile(comparison['y_pred'] / comparison['y_true'], 25, axis=0)]
            metric['50%_rate']           = [numpy.percentile(comparison['y_pred'] / comparison['y_true'], 50, axis=0)]
            metric['75%_rate']           = [numpy.percentile(comparison['y_pred'] / comparison['y_true'], 75, axis=0)]
            metric['max_rate']           = [(comparison['y_pred'].max() / comparison['y_true'].max())] if (comparison['y_true'].max() != 0) else [numpy.nan]
            metric['mean_rate']           = [(comparison['y_pred'].mean() / comparison['y_true'].mean())] if (comparison['y_true'].mean() != 0) else [numpy.nan]
            metric['std_rate']           = [(comparison['y_pred'].std() / comparison['y_true'].std())] if (comparison['y_true'].std() != 0) else [numpy.nan]
            metric['explained_cariance_score'] = [explained_variance_score(comparison['y_true'], comparison['y_pred'])]
            metric['max_error'] = [max_error(comparison['y_true'], comparison['y_pred'])]
            metric['mean_absolute_error'] = [mean_absolute_error(comparison['y_true'], comparison['y_pred'])]
            metric['mean_squared_error'] = [mean_squared_error(comparison['y_true'], comparison['y_pred'])]
            metric['median_absolute_error'] = [median_absolute_error(comparison['y_true'], comparison['y_pred'])]
            metric['r2_score'] = [r2_score(comparison['y_true'], comparison['y_pred'])]
            metric['mean_absolute_percentage_error'] = [mean_absolute_percentage_error(comparison['y_true'], comparison['y_pred'])]
            evaluation.update(metric)
            eval_dataframe = pandas.DataFrame(data=evaluation) if not 'eval_dataframe' in locals().keys() else pandas.concat([eval_dataframe, pandas.DataFrame(data=evaluation)], axis=0)
        return eval_dataframe


def classification(y_true, y_pred, y_prob=None):
    assert isinstance(y_true, (pandas.DataFrame, pandas.Series, numpy.ndarray)) 
    assert isinstance(y_pred, (pandas.DataFrame, pandas.Series, numpy.ndarray)) 
    if y_prob is not None:
        assert isinstance(y_prob, (pandas.DataFrame, pandas.Series, numpy.ndarray)) 
    
    if isinstance(y_true, pandas.Series):
        # [for pandas.Series]: Uni-Label classification
        if y_true.unique().shape[0] <= 2:
            # [binary-class] classification
            return BinaryClassification.evaluation(y_true, y_pred, y_prob)
        else:
            # [multi-class] classification
            return MultiClassification.evaluation(y_true, y_pred, y_prob)
    elif isinstance(y_true, pandas.DataFrame):
        # [for pandas.DataFrame]: Uni-Label classification, Multi-Label classification
        if y_true.shape[1] == 1:
            # [Uni-Label] classification
            y_true = y_true.iloc[:, 0]

            if y_true.unique().shape[0] <= 2:
                # [binary-class] classification
                return BinaryClassification.evaluation(y_true, y_pred, y_prob)
            else:
                # [multi-class] classification
                return MultiClassification.evaluation(y_true, y_pred, y_prob)
        else:
            # [Multi-Label] classification
            raise NotImplementedError()
    else:
        if y_true.ndim == 1:
            # [for numpy.ndarray]: Uni-Label classification
            if numpy.unique(y_true).shape[0] <= 2:
                # [binary-class] classification
                return BinaryClassification.evaluation(y_true, y_pred, y_prob)
            else:
                # [multi-class] classification
                return MultiClassification.evaluation(y_true, y_pred, y_prob)
        else:
            # [Uni-Label]: classification
            if y_true.shape[1] == 1:
                # [for numpy.ndarray]: Uni-Label classification
                if numpy.unique(y_true).shape[0] <= 2:
                    # [binary-class] classification
                    return BinaryClassification.evaluation(y_true, y_pred, y_prob)
                else:
                    # [multi-class] classification
                    return MultiClassification.evaluation(y_true, y_pred, y_prob)
            else:
                # [Multi-Label]: classification
                raise NotImplementedError()



def regression(y_true, y_pred):
    assert isinstance(y_true, (pandas.DataFrame, pandas.Series, numpy.ndarray))
    assert isinstance(y_pred, (pandas.DataFrame, pandas.Series, numpy.ndarray))

    if isinstance(y_true, pandas.Series):
        # [for pandas.Series]: Scalar regression
        return ScalarRegression.evaluation(y_true, y_pred)
    elif isinstance(y_true, pandas.DataFrame):
        if y_true.shape[1] == 1:
            # [for pandas.DataFrame]: Scalar regression
            return ScalarRegression.evaluation(y_true, y_pred)
        else:
            # [for pandas.DataFrame]: Vector regression
            return VectorRegression.evaluation(y_true, y_pred)
    else:
        if y_true.ndim == 1:
            # [for numpy.ndarray]: Scalar regression
            return ScalarRegression.evaluation(y_true, y_pred)
        else:
            if y_true.shape[1] == 1:
                # [for numpy.ndarray]: Scalar regression
                return ScalarRegression.evaluation(y_true, y_pred)
            else:
                # [for numpy.ndarray]: Vector regression
                return VectorRegression.evaluation(y_true, y_pred)

