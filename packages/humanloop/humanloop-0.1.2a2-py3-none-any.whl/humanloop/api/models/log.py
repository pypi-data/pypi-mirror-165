import datetime
from typing import List, Optional, Union

from pydantic import BaseModel, Field, validator

from .model import ModelProviders, ModelEndpoints
from .utils import RootBaseModel, KeyValues


class Feedback(BaseModel):
    group: str
    label: Optional[str] = Field(
        title="Label",
        description="A categorical label to characterize the type of feedback."
        "Only one of label or text should be provided for each feedback.",
    )
    text: Optional[str] = Field(
        title="Text",
        description="Text feedback. Can be used to record model corrections from "
        "your users. Only one of label or text should be provided "
        "for each feedback.",
    )
    log_id: Optional[str] = Field(
        title="Log ID",
        description="id to associate the feedback to a previously logged datapoint."
        "When providing instant feedback as part of the hl.log(...) call "
        "you don't need to provide a log_id.",
    )
    source: Optional[str] = Field(
        title="Source",
        description="A unique to who/what provided the feedback. "
        "For example a unique user reference.",
    )

    created_at: Optional[datetime.datetime] = Field(
        title="Created at",
        description="Timestamp for when the feedback was created. "
        "If not provided, the time the call was made will be used "
        "as a timestamp.",
    )

    @validator("text")
    def check_label_or_text(cls, v, values):
        if values["label"] is not None and v:
            raise ValueError(
                "Only one of label or text should be provided "
                "for each instance of feedback."
            )
        return v


class ListFeedbackRequest(RootBaseModel):
    __root__: Union[Feedback, List[Feedback]]


class Log(BaseModel):
    project: str = Field(
        title="Project name",
        description="Unique project name. If it does not exist, a new project will "
        "be created.",
    )
    inputs: KeyValues = Field(
        title="Model input data",
        description="List of name, value pairs for the inputs used by your prompt "
        "template, or directly by your model.",
    )
    output: str = Field(
        title="Model output",
        description="Generated output from your model for the provided inputs, or your "
        "corrected generation.",
    )
    model: Optional[str] = Field(
        title="Type of model used",
        description="What model type was used for the generation? e.g. text-davinci-002. "
        "This can be null if the generation is user provided",
    )
    prompt_template: Optional[str] = Field(
        title="Prompt template",
        description="Prompt template that incorporated your specified inputs to form "
        "your final request to the model.",
    )
    source: str = Field(
        title="Source of generation",
        description="What was used to generate the output? e.g. gpt-3. "
        "In the case of logging corrections, or Human generated examples, the source "
        "can be set as a unique user reference.",
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
    metadata: Optional[KeyValues] = Field(
        title="Metadata",
        description="Any additional metadata that you would like to log for reference.",
    )
    feedback: Optional[Union[Feedback, List[Feedback]]] = Field(
        title="Feedback labels",
        description="Optional parameter to provide feedback with your logged datapoint.",
    )
    created_at: Optional[datetime.datetime] = Field(
        title="Created at",
        description="Timestamp for when the log was created. "
        "If not provided, the time the log call was made will be used "
        "as a timestamp.",
    )


class ListLogRequest(RootBaseModel):
    __root__: Union[Log, List[Log]]


class LogResponse(BaseModel):
    id: str


class ListLogResponse(RootBaseModel):
    __root__: Union[LogResponse, List[LogResponse]]
