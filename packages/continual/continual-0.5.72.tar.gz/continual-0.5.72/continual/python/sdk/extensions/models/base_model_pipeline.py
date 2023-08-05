from abc import ABC, abstractmethod


class BaseModelPipeline(ABC):
    """
    Abstract Base Class for all pipelines
    """

    @abstractmethod
    def train(self):
        """
        Train model, log a model
        version state, and a model artifact
        """
        pass

    @abstractmethod
    def predict(self):
        """
        Use a trained model to make batch predictions
        on some given data. Log the batch prediction
        state and write the batch predictions to the
        data store
        """
        pass
