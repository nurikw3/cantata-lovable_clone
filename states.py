from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


_strict = ConfigDict(extra="forbid")


class File(BaseModel):
    model_config = _strict

    path: str = Field(description="The path to the file to be created or modified")
    purpose: str = Field(description="The purpose of the file")


class Plan(BaseModel):
    model_config = _strict

    name: str = Field(description="The name of app to be built")
    description: str = Field(
        description="A one-line description of the app to be built"
    )
    techstack: str = Field(description="The tech stack to be used")
    features: list[str] = Field(description="A list of features the app should have")
    files: list[File] = Field(description="A list of files to be created")


class ImplementationTask(BaseModel):
    model_config = _strict

    filepath: str = Field(description="The path to the file to be modified")
    task_description: str = Field(
        description="A detailed description of the task to be performed"
    )


class TaskPlan(BaseModel):
    model_config = _strict

    implementation_steps: list[ImplementationTask] = Field(
        description="A list of steps to be taken to implement the task"
    )


class CoderState(BaseModel):
    model_config = _strict

    task_plan: TaskPlan = Field(description="The plan for the task to be implemented")
    current_step_idx: int = Field(0, description="The index of the current step")
    current_file_content: Optional[str] = Field(
        None, description="The content of the file currently being edited"
    )
