import logging
from datasets import DatasetDict


class Training(object):
    """
    Class that outlines the functions that can be used to prepare the datasets
    for training and evaluation, and run the training and evaluation of the models
    """

    def __init__(
            self,
            sentence_datasets: DatasetDict,
    ):
        """
        Initialize the huggingface to trainer to None
        Initialize the dataset object that contains the train and eval splits

        Args:
            sentence_datasets (DatasetDict): The dataset object that contains the data for each split (train, val etc)
        """
        self._trainer = None
        self._sentence_datasets = sentence_datasets

    def get_train_dataset(self, max_train_samples):
        if "train" not in self._sentence_datasets:
            raise ValueError("--do_train requires a train dataset")
        train_dataset = self._sentence_datasets["train"]
        if max_train_samples is not None:
            max_train_samples = min(len(train_dataset), max_train_samples)
            train_dataset = train_dataset.select(range(max_train_samples))
        return train_dataset

    def get_eval_dataset(self, max_eval_samples):
        if "validation" not in self._sentence_datasets:
            raise ValueError("--do_eval requires a validation dataset")
        eval_dataset = self._sentence_datasets["validation"]
        if max_eval_samples is not None:
            max_eval_samples = min(len(eval_dataset), max_eval_samples)
            eval_dataset = eval_dataset.select(range(max_eval_samples))
        return eval_dataset

    def get_test_dataset(self, max_test_samples):
        if "test" not in self._sentence_datasets:
            raise ValueError("--do_predict requires a test dataset")
        test_dataset = self._sentence_datasets["test"]
        if max_test_samples is not None:
            max_test_samples = min(len(test_dataset), max_test_samples)
            test_dataset = test_dataset.select(range(max_test_samples))
        return test_dataset

    def set_trainer(self, trainer):
        if self._trainer is None:
            logging.info("Initializing trainer")
        else:
            logging.warning("Trainer already initialized, re-initializing with new trainer")
        self._trainer = trainer

    def run_train(self, train_dataset, resume_from_checkpoint, last_checkpoint):
        checkpoint = None
        if resume_from_checkpoint is not None:
            checkpoint = resume_from_checkpoint
        elif last_checkpoint is not None:
            checkpoint = last_checkpoint
        train_result = self._trainer.train(resume_from_checkpoint=checkpoint)
        self._trainer.save_model()  # Saves the tokenizer too for easy upload
        metrics = train_result.metrics

        metrics["train_samples"] = len(train_dataset)

        self._trainer.log_metrics("train", metrics)
        self._trainer.save_metrics("train", metrics)
        self._trainer.save_state()
        return metrics

    def run_eval(self, eval_dataset):
        logging.info("*** Evaluate ***")
        metrics = self._trainer.evaluate()

        metrics["eval_samples"] = len(eval_dataset)
        self._trainer.log_metrics("eval", metrics)
        self._trainer.save_metrics("eval", metrics)
        return metrics

    def run_predict(self, test_dataset):
        return self._trainer.predict(test_dataset)