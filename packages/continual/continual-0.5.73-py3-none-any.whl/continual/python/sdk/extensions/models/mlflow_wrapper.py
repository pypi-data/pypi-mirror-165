import mlflow.pyfunc
import cloudpickle
from pandas import DataFrame
import os
import numpy as np


class ContinualSavedModel:
    def __init__(self, model, prediction_model):
        self.model = model
        self.prediction_model = prediction_model

    def predict_proba(self, df):
        return self.model.predict_proba(
            df, model=self.prediction_model, as_pandas=False, as_multiclass=False
        )

    def predict(self, df):
        return self.model.predict(df, model=self.prediction_model)


class ContinualSavedModelWrapper(mlflow.pyfunc.PythonModel):
    """
    Class to wrap continual models
    """

    def load_context(self, context):
        """This method is called when loading an MLflow model with pyfunc.load_model(), as soon as the Python Model is constructed.
        Args:
            context: MLflow context where the model artifact is stored.
        """
        file_to_read = open(context.artifacts["continual_model"], "rb")
        os.chdir(context.artifacts["model_files"])
        loaded_object = cloudpickle.load(file_to_read)
        file_to_read.close()
        self.model = loaded_object

    def predict(self, context, model_input):
        """This is an abstract function. We customized it into a method to fetch the FastText model.
        Args:
            context ([type]): MLflow context where the model artifact is stored.
            model_input ([type]): the input data to fit into the model.
        Returns:
            [type]: the loaded model artifact.
        """
        print("context: {}".format(context))
        results_predict = self.model.predict(model_input)
        results_proba = self.model.predict_proba(model_input)

        result_df = DataFrame(
            {
                "predict": results_predict,
                "predict_proba": None,
            }
        )
        result_df.reset_index(inplace=True)
        if isinstance(results_proba, np.ndarray):
            result_df["predict_proba"] = results_proba.tolist()
        else:
            result_df["predict_proba"] = results_proba

        return result_df
