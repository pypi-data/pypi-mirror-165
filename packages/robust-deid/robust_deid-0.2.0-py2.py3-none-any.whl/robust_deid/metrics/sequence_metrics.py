from .token_evaluation import TokenEvaluation


class SequenceMetrics(object):

    def __init__(
            self,
            post_process,
            ner_types,
            label_list,
            return_entity_level_metrics
    ):
        self._post_process = post_process
        self._ner_types = ner_types
        self._label_list = label_list
        self._return_entity_level_metrics = return_entity_level_metrics

    @staticmethod
    def get_token_metrics(predictions, labels, ner_types, ner_description):
        # Token level metric scores
        token_report = TokenEvaluation.classification_report(
            labels=labels,
            predictions=predictions,
            ner_types=ner_types
        )
        token_report.pop("weighted avg")
        macro_token_score = token_report.pop("macro avg")
        micro_token_score = token_report.pop("micro avg")
        # Extract token level scores for each NER type
        token_scores = {
            type_name.lower(): {
                "precision": score["precision"],
                "recall": score["recall"],
                "f1": score["f1-score"],
                "number": score["support"],
            }
            for type_name, score in token_report.items()
        }
        # Extract micro averaged token level score
        micro_token_overall = {
            'micro_avg' + ner_description: {
                "precision": micro_token_score["precision"],
                "recall": micro_token_score["recall"],
                "f1": micro_token_score["f1-score"]}
        }
        # Extract macro averaged token level score
        macro_token_overall = {
            'macro_avg' + ner_description: {
                "precision": macro_token_score["precision"],
                "recall": macro_token_score["recall"],
                "f1": macro_token_score["f1-score"]}
        }
        return {**token_scores, **micro_token_overall, **macro_token_overall}

    def compute_metrics(self, model_output):

        # Remove ignored index (special tokens)
        model_predictions, model_labels = model_output.predictions, model_output.label_ids
        true_predictions, true_labels = self._post_process.decode(
            model_predictions=model_predictions, model_labels=model_labels
        )

        return self.compute_metrics_from_predictions(true_predictions=true_predictions, true_labels=true_labels)

    def compute_metrics_from_predictions(self, true_predictions, true_labels):

        token_results = self.get_token_metrics(
            predictions=true_predictions,
            labels=true_labels,
            ner_types=self._ner_types,
            ner_description=''
        )
        binary_token_results = self.get_token_metrics(
            predictions=[
                [
                    'O' if prediction == 'O' else prediction[0:2] + 'PHI+' for prediction in predictions
                ] for predictions in true_predictions
            ],
            labels=[
                [
                    'O' if label == 'O' else label[0:2] + 'PHI+' for label in labels
                ] for labels in true_labels
            ],
            ner_types=['PHI+'],
            ner_description='_phi+'
        )
        results = {**token_results, **binary_token_results}

        if self._return_entity_level_metrics:
            # Unpack nested dictionaries
            final_results = {}
            for key, value in results.items():
                if isinstance(value, dict):
                    for n, v in value.items():
                        final_results[f"{key}_{n}"] = v
                else:
                    final_results[key] = value
            return final_results
        else:
            return {
                "precision": results["overall_precision"],
                "recall": results["overall_recall"],
                "f1": results["overall_f1"],
                "accuracy": results["overall_accuracy"],
            }
