import typer

from continual.python.cli import utils
from continual.python.sdk.client import Client

from typing import List
from rich.console import Console
from continual.services.compute_services.pipelines.batchprediction.batch_prediction_runner import (
    BatchPredictionRunner,
)

from continual.services.compute_services.pipelines.training.training_runner import (
    TrainingPipelineRunner,
)

app = typer.Typer(help="Provides tools and processes for extension development.")


@app.command("run")
@utils.exit_on_error
def run(
    project: str = typer.Option(None, help="Project ID."),
    environment: str = typer.Option(None, "--env", help="Environment ID."),
    model: str = typer.Argument(..., help="ID for the model to run locally"),
    paths: List[str] = typer.Option(
        None,
        "--paths",
        exists=True,
        dir_okay=True,
        help="Paths to YAML files or directories.",
    ),
    train: bool = typer.Option(False, "--train", help="Runs training if set."),
    trained_model_version: str = typer.Option(
        None,
        "--model-version",
        help="Trained model version name if only running batchprediction",
    ),
    batchpredict: bool = typer.Option(
        False, "--batchpredict", help="Runs batchprediction if set."
    ),
    to_json: bool = typer.Option(
        False, "--json", help="Show full JSON representation."
    ),
):
    """Run local training and batchprediction.

    Command will execute the following steps:
    * Push all YAMLS in `path`, creating any models, featuresets and extensions
    * If --train is specified, run training using the model pipeline specified in the YAML for the model `model_id`.
    * If --batchpredict is specified, run prediction using the model pipeline specified in the YAML for the model `model_id`.
    """

    project, environment = utils.get_project_and_environment(project, environment)
    client = Client(project=utils.get_environment_name(project, environment))
    model_version_name = None

    # Step 1 push without training
    if paths:
        changes = client.changes.push(paths=paths, train_none=True)
        changes.wait(timeout=3600)

    # Step 2, if train is specified create a local model version
    if train:
        try:
            local_model_version = client.models.create_local_dev_model_version(id=model)
            model_version_name = local_model_version.name

            client.set_logging_resource(resource=model_version_name)
            console = Console()
            if to_json:
                console.print(local_model_version.to_dict())
            else:
                typer.secho(
                    "Created model version %s \n" % (model_version_name),
                    fg="blue",
                )

            TrainingPipelineRunner(
                client=client,
                model_version_name=model_version_name,
            ).run()
        except Exception as e:
            typer.secho(
                f"Training failed with exception: {str(e)} \n",
                fg="red",
            )
    else:
        model_version_name = trained_model_version

    if batchpredict:
        if not model_version_name:
            typer.secho(
                "Error: Local batchprediction requires --train to be set OR --model-version to specified.",
                fg="red",
            )
            return
        try:
            local_batch_prediction = client.models.create_local_dev_batch_prediction(
                id=model, model_version_name=model_version_name
            )
            client.set_logging_resource(resource=local_batch_prediction.name)

            console = Console()
            if to_json:
                console.print(local_batch_prediction.to_dict())
            else:
                typer.secho(
                    "Created batch prediction %s \n" % (local_batch_prediction.name),
                    fg="blue",
                )
            BatchPredictionRunner(
                client=client,
                batch_prediction_name=local_batch_prediction.name,
            ).run()
        except Exception as e:
            typer.secho(
                f"Batchprediction failed with exception: {str(e)} \n",
                fg="red",
            )
