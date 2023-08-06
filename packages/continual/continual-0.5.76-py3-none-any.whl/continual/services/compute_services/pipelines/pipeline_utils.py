import importlib

from continual.python.sdk.extensions.models.base_model_pipeline import BaseModelPipeline
from continual.python.sdk.client import Client

CONTINUAL_AUTOGLUON_PIPELINE_MODULE = "continual.python.engine.auto_classification_regression.continual_autogluon_pipeline"
CONTINUAL_AUTOGLUON_PIPELINE_CLASS = "ContinualAutogluonPipeline"
DEFAULT_PIPELINES = {
    "AutoClassificationRegression": {
        "module": CONTINUAL_AUTOGLUON_PIPELINE_MODULE,
        "class": CONTINUAL_AUTOGLUON_PIPELINE_CLASS,
    }
}


def get_pipeline(client: Client, pipeline_id: str = None) -> BaseModelPipeline:
    """
    Install load and instantiate the class for the custom pipeline
    """
    if not pipeline_id:
        pipeline_module = importlib.import_module(CONTINUAL_AUTOGLUON_PIPELINE_MODULE)
        pipeline_class = getattr(
            pipeline_module, CONTINUAL_AUTOGLUON_PIPELINE_CLASS, None
        )
        return pipeline_class

    elif pipeline_id in DEFAULT_PIPELINES:
        pipeline_module = importlib.import_module(
            DEFAULT_PIPELINES[pipeline_id]["module"]
        )
        pipeline_class = getattr(
            pipeline_module, DEFAULT_PIPELINES[pipeline_id]["class"], None
        )
        return pipeline_class

    else:
        # Use SDK to download extension
        client.extensions.install(id=pipeline_id)

        pipeline_extension = client.extensions.get(id=pipeline_id)

        # Import pipeline class using extension metadata
        pipeline_module = importlib.import_module(pipeline_extension.module_name)
        pipeline_class = getattr(pipeline_module, pipeline_extension.class_name, None)

        return pipeline_class
