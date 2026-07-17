from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel, Field, field_validator, ConfigDict
from .request import BatchRequestMessage, BatchRequestId

class BaseModelWithExtra(BaseModel):
    model_config = ConfigDict(
        extra='allow',
    )

class BatchResponseChoice(BaseModelWithExtra):
    index: int
    message: BatchRequestMessage
    logprobs: Any
    finish_reason: str


class PromptTokensDetails(BaseModelWithExtra):
    cached_tokens: int
    audio_tokens: int

class CompletionTokensDetails(BaseModelWithExtra):
    reasoning_tokens: int
    audio_tokens: int
    accepted_prediction_tokens: int
    rejected_prediction_tokens: int


class BatchResponseUsage(BaseModelWithExtra):
    input_tokens: Optional[int] = Field(alias="prompt_tokens", default=None)
    completion_tokens: Optional[int] = Field(alias="completion_tokens", default=None)
    total_tokens: Optional[int] = Field(default=None)
    prompt_tokens_details: Optional[PromptTokensDetails] = Field(default=None)
    completion_tokens_details: Optional[CompletionTokensDetails] = Field(default=None)


class BatchResponseBody(BaseModelWithExtra):
    id: str
    object: str
    created: int
    model: str
    choices: List[BatchResponseChoice]
    usage: Optional[BatchResponseUsage] = Field(default=None)
    service_tier: Optional[str] = None
    system_fingerprint: Optional[str] = None


class BatchResponseInner(BaseModelWithExtra):
    status_code: int
    request_id: str
    body: BatchResponseBody


class BatchResponse(BaseModelWithExtra):
    id: str
    custom_id: BatchRequestId
    response: BatchResponseInner
    error: Any

    @field_validator('custom_id', mode="before")
    def validate_custom_id(cls, v):
        return BatchRequestId.from_str(v)
