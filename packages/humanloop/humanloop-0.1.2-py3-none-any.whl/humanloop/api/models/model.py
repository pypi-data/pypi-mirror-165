from enum import Enum
from pydantic import Field, BaseModel
from typing import Optional, Dict, List, Any
import datetime
from .utils import KeyValues


class ModelProviders(Enum):
    """Supported model providers."""

    openai = "OpenAI"
    ai21 = "AI21"
    mock = "Mock"


class ModelEndpoints(Enum):
    """Supported model endpoints."""

    complete = "Complete"
    edit = "Edit"


class ModelConfig(BaseModel):
    name: Optional[str] = Field(
        title="Config name",
        description="A friendly display name for config. If not provided a name "
        "will be generated.",
    )
    project: str = Field(
        title="Project name",
        description="Unique project name. If it does not exist, a new project will "
        "be created.",
    )
    experiment: Optional[str] = Field(
        title="Experiment tag",
        description="Include a model configuration in an experiment group. "
        "Experiment groups are used for A/B testing and optimizing "
        "hyper-parameters.",
    )
    model: str = Field(
        title="Type of model used",
        description="What model type was used for the generation? e.g. text-davinci-002. "
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
        " configuration on Humanloop. For example the temperature setting.",
    )
    provider: Optional[ModelProviders] = Field(
        title="Model provider",
        description="The company who is hosting the target model.",
        default=ModelProviders.openai,
    )
    endpoint: Optional[ModelEndpoints] = Field(
        title="Provider endpoint",
        description="Which of the providers model endpoints to use. "
        "For example Complete or Edit. ",
        default=ModelEndpoints.complete,
    )


class ModelConfigResponse(BaseModel):
    id: str
    display_name: str
    model_name: str
    prompt_template: Optional[str]
    parameters: Optional[dict]
    provider: Optional[ModelProviders]
    endpoint: Optional[ModelEndpoints]
    experiment_id: Optional[str]
    created_at: datetime.datetime


class ModelGenerate(BaseModel):
    project: str = Field(
        title="Project name",
        description="Unique project name. If it does not exist, a new project will "
        "be created.",
    )
    experiment_id: Optional[str] = Field(
        title="ID of experiment",
        description="If an experiment ID is provided a model configuration will be "
        "sampled from the experiments active model configurations. ",
    )
    model_config_id: Optional[str] = Field(
        title="Model config ID",
        description="Unique ID of a registered model_config. "
        "This gives you explicit control over which model configuration to use.",
    )
    inputs: KeyValues = Field(
        title="Model input data",
        description="List of name, value pairs for the inputs used by your prompt "
        "template, or directly by your model.",
    )
    source: str = Field(
        title="Source",
        description="What was source of the model used for this generation?"
        "e.g. website-landing-page",
    )
    metadata: Optional[KeyValues] = Field(
        title="Metadata",
        description="Any additional metadata that you would like to log for reference.",
    )
    provider_api_keys: Optional[Dict[ModelProviders, str]] = Field(
        title="Provider API Key",
        description="API keys required each provider to make API calls. These API keys"
        "are NOT stored by Humanloop.",
    )
    parameters: Optional[KeyValues] = Field(
        title="Model parameters",
        description="The hyper-parameter settings that along with your model source "
        "and prompt template (if provided) will uniquely determine a model"
        " configuration on Humanloop. For example, the temperature setting."
        "This is used only if an existing experiment_id or model_config_id "
        "are not provided.",
    )
    model: Optional[str] = Field(
        title="Model instance used",
        description="What model instance was used for the generation? "
        "e.g. text-davinci-002. "
        "This is used only if an existing experiment_id or model_config_id "
        "are not provided.",
    )
    prompt_template: Optional[str] = Field(
        title="Prompt template",
        description="Prompt template that incorporated your specified inputs to form "
        "your final request to the model. "
        "NB: Input variables within the prompt template should be specified "
        "with syntax: {{INPUT_NAME}}."
        "This is used only if an existing experiment_id or model_config_id "
        "are not provided.",
    )
    provider: Optional[ModelProviders] = Field(
        title="Model provider",
        description="The company who is hosting the target model."
        "This is used only if an existing experiment_id or model_config_id "
        "are not provided.",
        default=ModelProviders.openai,
    )
    endpoint: Optional[ModelEndpoints] = Field(
        title="Provider endpoint",
        description="Which of the providers model endpoints to use. "
        "For example Complete or Edit. "
        "This is used only if an existing experiment_id or model_config_id "
        "are not provided.",
        default=ModelEndpoints.complete,
    )


class LogResponse(BaseModel):
    id: str = Field(
        title="Log id",
        description="Unique id for model output logged to Humanloop."
        "Use this when recording feedback later.",
    )
    output: str = Field(
        title="Provider output text",
        description="Output text returned from the provider model.",
    )


class ModelGenerateResponse(BaseModel):
    logs: List[LogResponse]
    model_config: Optional[ModelConfigResponse] = Field(
        title="Model configuration",
        description="The model configuration used to call the provider model.",
    )
    inputs: KeyValues = Field(
        title="Inputs",
        description="The inputs passed to the provider model to produce the outputs.",
    )
    provider_response: Any = Field(
        title="Provider response",
        description="The full raw response provided by the provider.",
    )
    prompt: str = Field(
        title="Prompt",
        description="The prompt is the prompt template populated with the inputs."
        "This is what is used by the provider model to produce an output.",
    )

