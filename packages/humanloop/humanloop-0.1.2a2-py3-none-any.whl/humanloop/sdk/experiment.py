from humanloop.api.models.experiment import TrialResponse
from humanloop.sdk.init import _get_client


def trial(experiment_id: str) -> TrialResponse:
    """ Generates a model config according to your experiment to use to execute your model. """
    client = _get_client()
    return client.register(experiment_id)