from pydantic import BaseModel, Field
from typing import Optional
from .utils import KeyValues
from .model import ModelProviders, ModelEndpoints


class TrialResponse(BaseModel):
    id: str = Field(
        title="Trial ID",
        description="Unique ID of trial to reference in subsequent log calls.",
    )
    model_config_id: str = Field(
        title="Model config ID",
        description="Unique ID of the model config associated to the trial.",
    )
    experiment_id: str = Field(
        title="Experiment",
        description="Unique ID of the experiment the trial belongs to.",
    )
    model_config_name: Optional[str] = Field(
        title="Model config name",
    )
    model: str = Field(
        title="Instance of model used",
        description="What instance of model was used for the generation?"
        "e.g. text-davinci-002. ",
    )
    prompt_template: Optional[str] = Field(
        title="Prompt template",
        description="Prompt template that incorporated your specified inputs to form "
        "your final request to the model.",
    )
    parameters: Optional[KeyValues] = Field(
        title="Model parameters",
        description="The hyper-parameter settings that along with your model source "
        "and prompt template (if provided) will uniquely determine a model"
        " configuration on Humanloop. For example, the temperature setting.",
    )
    provider: Optional[ModelProviders] = Field(
        title="Model provider",
        description="The company who is hosting the target model.",
    )
    endpoint: Optional[ModelEndpoints] = Field(
        title="Provider endpoint",
        description="Which of the providers model endpoints to use."
        "For example Complete or Edit. ",
    )