import numpy as np
from scipy.special import softmax
from sklearn.metrics import precision_recall_curve


class RecallThreshold(object):

    def __init__(self, label_list):
        self._mask = np.zeros((len(label_list)), dtype=bool)
        self._mask[label_list.index('O')] = True

    def __convert_binary_max(self, logits, labels):
        y_true = list()
        y_pred = list()
        for logits, label in zip(logits, labels):
            probabilities = softmax(logits)
            masked_probabilities = np.ma.MaskedArray(data=probabilities, mask=self._mask)
            y_true.append(0 if label == 'O' else 1)
            y_pred.append(masked_probabilities.max())

        return y_true, y_pred

    @staticmethod
    def __get_precision_recall_threshold(y_true, y_pred):
        precisions, recalls, thresholds = precision_recall_curve(y_true, y_pred, pos_label=1)
        thresholds = np.append(thresholds, thresholds[-1])
        return precisions, recalls, thresholds

    @staticmethod
    def __get_threshold_at_recall(precisions, recalls, thresholds, recall_cutoff):
        precision = precisions[recalls > recall_cutoff][-1]
        recall = recalls[recalls > recall_cutoff][-1]
        threshold = thresholds[recalls > recall_cutoff][-1]
        return {'precision': precision, 'recall': recall, 'threshold': threshold}

    def get_threshold_at_recall(self, logits, labels, recall_cutoff):
        y_true, y_pred = self.__convert_binary_max(
            logits, labels
        )
        precisions, recalls, thresholds = self.__get_precision_recall_threshold(y_true=y_true, y_pred=y_pred)
        return self.__get_threshold_at_recall(precisions, recalls, thresholds, recall_cutoff)

    def get_threshold_at_recalls(self, logits, labels, recall_cutoffs):
        y_true, y_pred = self.__convert_binary_max(
            logits, labels
        )
        precisions, recalls, thresholds = self.__get_precision_recall_threshold(y_true=y_true, y_pred=y_pred)
        for recall_cutoff in recall_cutoffs:
            yield self.__get_threshold_at_recall(precisions, recalls, thresholds, recall_cutoff)
