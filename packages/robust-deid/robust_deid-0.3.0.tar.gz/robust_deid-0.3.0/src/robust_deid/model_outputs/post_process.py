import numpy as np
from typing import Sequence, Tuple, Any, Optional, Union, List

from scipy.special import softmax


class Process(object):
    """
    Process the output of the model forward pass. The forward pass will return the predictions
    (e.g the logits), labels if present. We process the output and return the processed
    values based on the application.
    """

    def __init__(self, label_list: Sequence[str], ignore_label: int = -100, token_ignore_label: str = 'NA'):
        """
        Initialize the variables

        Args:
            label_list (Sequence[str]): A label list where the position corresponds to a particular label. For example
            position 0 will correspond to B-DATE etc.
            ignore_label (int, defaults to `-100`): Use this value for padded tokens and any tokens that should not be
            involved in the backward pass.
            token_ignore_label (str, defaults to `NA`): This indicates tokens added for context and that should not be
            part of the backward pass or the final output.
        """

        self._label_list = label_list
        self._ignore_label = ignore_label
        self._token_ignore_label = token_ignore_label

    def filter_by_dataset_labels(
            self,
            dataset_lists: Sequence[Sequence[Any]],
            dataset_labels: Sequence[Sequence[str]]
    ) -> Sequence[Sequence[Any]]:
        """
        Filter any dataset list based on the dataset labels. Remove elements in the
        dataset lists where the corresponding dataset label is the token_ignore_label
        which by default has the value 'NA'.

        Args:
            dataset_lists (Sequence[Sequence[Any]]): A sequence of data to be filtered
            dataset_labels (Sequence[Sequence[str]]): The corresponding list that is used to filter that dataset list.
            This list should contain the token ignore label.

        Returns:
            (Sequence[Sequence[Any]]): The filtered dataset list.
        """

        return [
            [dataset_item for (dataset_item, label) in zip(dataset_list, labels) if label != self._token_ignore_label]
            for dataset_list, labels in zip(dataset_lists, dataset_labels)
        ]

    def get_true_logits(
            self,
            model_predictions: Sequence[Sequence[Sequence[float]]],
            model_labels: Sequence[Sequence[float]]
    ) -> Sequence[Sequence[Sequence[float]]]:
        """
        Filter and return the prediction logits. Remove elements in the model_predictions
        where the corresponding dataset label is the ignore_label which by default has the value '-100'.

        Args:
            model_predictions (Sequence[Sequence[Sequence[float]]]): The predictions made by the model
            model_labels (Sequence[Sequence[float]]): The labels for the model. This list should contain the ignore
            label.

        Returns:
            (Sequence[Sequence[Sequence[float]]]): The prediction logits of the model.
        """

        return [
            [
                prediction.tolist() for (prediction, label) in zip(predictions, labels)
                if label != self._ignore_label
            ] for predictions, labels in zip(model_predictions, model_labels)
        ]

    def get_true_predictions(
            self,
            model_predictions: Sequence[Sequence[int]],
            model_labels: Sequence[Sequence[int]]
    ) -> Sequence[Sequence[str]]:
        """
        Filter, return and map the predictions. Remove elements in the model_predictions
        where the corresponding model label is the ignore_label which by default has
        the value '-100'. Map the predictions (e.g 0, 1, ...) from indexes back to string
        (e.g B-DATE, B-AGE, ...)

        Args:
            model_predictions (Sequence[Sequence[int]]): The predictions made by the model
            model_labels (Sequence[Sequence[int]]): The labels for the model. This list should contain the ignore
            label.

        Returns:
            (Sequence[Sequence[int]]): The predictions of the model.
        """

        return [
            [
                self._label_list[prediction] for (prediction, label) in zip(predictions, labels)
                if label != self._ignore_label
            ] for predictions, labels in zip(model_predictions, model_labels)
        ]

    def get_true_labels(self, model_labels: Sequence[Sequence[int]]) -> Sequence[Sequence[str]]:
        """
        Filter, return and map the labels. Remove elements in the model_labels
        where the corresponding model label is the ignore_label which by default has
        the value '-100'. Map the labels (e.g 0, 1, ...) from indexes back to string
        (e.g B-DATE, B-AGE, ...).

        Args:
            model_labels (Sequence[Sequence[int]]): The labels for the model. This list should contain the ignore
            label.

        Returns:
            (Sequence[Sequence[str]]): The labels of the model.
        """

        return [
            [
                self._label_list[label] for label in labels
                if label != self._ignore_label
            ] for labels in model_labels
        ]

    def modify_predictions(
            self,
            model_predictions: Sequence[Sequence[Sequence[float]]],
            model_labels: Sequence[Sequence[int]]
    ):
        """
        Function to make any changes to the type or format of the predictions.

        Args:
            model_predictions (Sequence[Sequence[Sequence[float]]]): The predictions made by the model.
            model_labels (Sequence[Sequence[int]]): The labels for the model. This list should contain the ignore
            label.
        """

        raise NotImplementedError('Use subclass method')

    def get_predictions(self, model_predictions: Sequence[Sequence[Sequence[float]]]):
        """
        Function to process the model predictions (the logits/scores specifically) and return the model
        predictions - i.e. return the actual ner tag indexes the model predicted.

        Args:
            model_predictions (Sequence[Sequence[Sequence[float]]]): The numerical predictions made by the model.
        """

        raise NotImplementedError('Use subclass method')

    def __get_predictions_and_labels(
            self,
            model_predictions: Sequence[Sequence[int]],
            model_labels: Sequence[Sequence[int]]
    ) -> Tuple[Sequence[Sequence[str]], Sequence[Sequence[str]]]:
        """
        Decode the predictions and labels so that the evaluation function and prediction
        functions can use them accordingly. The predictions and labels are numbers (ids)
        of the labels, these will be converted back to the NER tags (B-AGE, I-DATE etc) using
        the label_list. In this function we just take the argmax of the logits (scores) of the predictions
        Also remove the predictions and labels on the subword and context tokens

        Args:
            model_predictions (Sequence[Sequence[int]]): The predicted NER indexes.
            model_labels (Sequence[Sequence[int]]): Gold standard label indexes.

        Returns:
            true_predictions (Sequence[Sequence[str]]): The predicted NER tags
            true_labels (Sequence[Sequence[str]]): The gold standard NER tags
        """

        # Remove ignored index (special tokens)
        true_predictions = self.get_true_predictions(
            model_predictions=model_predictions, model_labels=model_labels
        )

        true_labels = self.get_true_labels(
            model_labels=model_labels
        )

        return true_predictions, true_labels

    def decode(
            self,
            model_predictions: Sequence[Sequence[Sequence[float]]],
            model_labels: Sequence[Sequence[int]]
    ) -> Tuple[Sequence[Sequence[str]], Sequence[Sequence[str]]]:
        """
        Decode the predictions and labels so that the evaluation function and prediction
        functions can use them accordingly. The predictions and labels are numbers (ids)
        of the labels, these will be converted back to the NER tags (B-AGE, I-DATE etc) using
        the label_list. In this function we just take the argmax of the logits (scores) of the predictions.
        Also remove the predictions and labels on the subword and context tokens.

        Args:
            model_predictions (Sequence[Sequence[Sequence[float]]]): The logits (scores for each tag)
            returned by the model.
            model_labels (Sequence[Sequence[int]]): Gold standard labels.

        Returns:
            true_predictions (Sequence[Sequence[str]]): The predicted NER tags.
            true_labels (Sequence[Sequence[str]]): The gold standard NER tags.
        """

        model_predictions = self.modify_predictions(model_predictions=model_predictions, model_labels=model_labels)
        model_predictions = self.get_predictions(model_predictions=model_predictions)
        return self.__get_predictions_and_labels(model_predictions=model_predictions, model_labels=model_labels)


class ArgmaxProcess(Process):
    """
    Process the output of the model forward pass. Given the model logits (numerical prediction scores)
    we return the prediction of the model as the entity with the highest numerical score.
    """

    def __init__(self, label_list: Sequence[str], ignore_label: int = -100, token_ignore_label: str = 'NA'):
        """
        Initialize the variables

        Args:
            label_list (Sequence[str]): A label list where the position corresponds to a particular label. For example
            position 0 will correspond to B-DATE etc.
            ignore_label (int, defaults to `-100`): Use this value for padded tokens and any tokens that should not be
            involved in the backward pass.
            token_ignore_label (str, defaults to `NA`): This indicates tokens added for context and that should not be
            part of the backward pass or the final output.
        """

        super().__init__(label_list=label_list, ignore_label=ignore_label, token_ignore_label=token_ignore_label)

    def get_predictions(self, model_predictions: Sequence[Sequence[Sequence[float]]]) -> Sequence[Sequence[int]]:
        """
        Function to process the model predictions (the logits/scores specifically) and return the model
        predictions - i.e. return the actual ner tag indexes the model predicted. The index of the entity
        with the highest numerical score is returned as the prediction.

        Args:
            model_predictions (Sequence[Sequence[Sequence[float]]]): The numerical predictions made by the model.

        Returns:
            (Sequence[Sequence[int]]): The predicted NER indexes.
        """

        return np.argmax(model_predictions, axis=2)

    def modify_predictions(
            self,
            model_predictions: Sequence[Sequence[Sequence[float]]],
            model_labels: Sequence[Sequence[int]]
    ) -> Sequence[Sequence[Sequence[float]]]:
        """
        Function to make any changes to the type or format of the predictions.
        Return the predictions as is.

        Args:
            model_predictions (Sequence[Sequence[Sequence[float]]]): The predictions made by the model.
            model_labels (Sequence[Sequence[int]]): The labels for the model. This list should contain the ignore
            label.

        Returns:
            (Sequence[Sequence[Sequence[float]]]): The predictions as is (un-modified).
        """

        return model_predictions


class ThresholdProcess(Process):
    """
        Process the output of the model forward pass. Given the model logits (numerical prediction scores)
        we return the prediction of the model based on a threshold criteria. We check if the numerical
        score of the outside entity is greater than (1 - threshold), then we return the prediction as the
        outside entity, else we return the highest scoring tag entity.
        """

    def __init__(
            self,
            label_list: Sequence[str],
            recall_threshold: float,
            ignore_label: int = -100,
            token_ignore_label: str = 'NA'
    ):
        """
        Initialize the variables

        Args:
            label_list (Sequence[str]): A label list where the position corresponds to a particular label. For example
            position 0 will correspond to B-DATE etc.
            recall_threshold (float): The threshold criteria value.
            ignore_label (int, defaults to `-100`): Use this value for padded tokens and any tokens that should not be
            involved in the backward pass.
            token_ignore_label (str, defaults to `NA`): This indicates tokens added for context and that should not be
            part of the backward pass or the final output.
        """

        super().__init__(label_list=label_list, ignore_label=ignore_label, token_ignore_label=token_ignore_label)
        self._recall_threshold = recall_threshold
        self._outside_label_index = self._label_list.index('O')
        self._mask = np.zeros((len(self._label_list)), dtype=bool)
        self._mask[self._outside_label_index] = True

    def get_predictions(
            self,
            model_predictions: Sequence[Sequence[Sequence[float]]]
    ) -> Sequence[Optional[Sequence[int]]]:
        """
        Function to process the model predictions (the logits/scores specifically) and return the model
        predictions - i.e. return the actual ner tag indexes the model predicted. The index of the entity
        based on the threshold criteria is returned as the prediction.

        Args:
            model_predictions (Sequence[Sequence[Sequence[float]]]): The numerical predictions made by the model.

        Returns:
            (Sequence[Sequence[int]]): The predicted NER indexes.
        """

        return [
            [self.process_prediction(prediction) if prediction != [] else None for prediction in predictions]
            for predictions in model_predictions
        ]

    def get_masked_array(self, data: Union[List, np.array]) -> np.ma.MaskedArray:
        """
        Mask an array based on the mask position and return the masked array
        as a masked numpy array.

        Args:
            data (Union[List, np.array]): The sequential data to be masked.

        Returns:
            (np.ma.MaskedArray): The masked sequential data.
        """

        return np.ma.MaskedArray(data=data, mask=self._mask)

    def process_prediction(self, prediction: Sequence[float]) -> int:
        """
        Return the predicted NER index based on the threshold criteria.

        Args:
            prediction (Sequence[float]): The numerical predictions/scores at a given token position.

        Returns:
            (int): The predicted NER index.
        """

        softmax_prob = softmax(prediction)
        masked_softmax_prob = self.get_masked_array(data=softmax_prob)
        if masked_softmax_prob.sum() >= self._recall_threshold:
            return masked_softmax_prob.argmax()
        else:
            return self._outside_label_index

    def modify_predictions(
            self,
            model_predictions: Sequence[Sequence[Sequence[float]]],
            model_labels: Sequence[Sequence[int]]
    ) -> Sequence[Sequence[Sequence[float]]]:
        """
        Function to make any changes to the type or format of the predictions.
        We return an empty list for the positions corresponding to the ignore
        label. This is done to avoid unnecessary computing of softmax at these positions.

        Args:
            model_predictions (Sequence[Sequence[Sequence[float]]]): The predictions made by the model.
            model_labels (Sequence[Sequence[int]]): The labels for the model. This list should contain the ignore
            label.

        Returns:
            (Sequence[Sequence[Sequence[float]]]): The predictions with an empty list at ignored label positions.
        """

        return [
            [prediction if label != self._ignore_label else [] for prediction, label in zip(predictions, labels)]
            for predictions, labels in zip(model_predictions, model_labels)
        ]
