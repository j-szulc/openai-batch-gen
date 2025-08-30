from __future__ import annotations

from typing import Any, List

from pydantic import BaseModel, Field, field_validator
from .request import BatchRequestMessage, BatchRequestId

class BatchResponseChoice(BaseModel):
    index: int
    message: BatchRequestMessage
    logprobs: Any
    finish_reason: str


class PromptTokensDetails(BaseModel):
    cached_tokens: int
    audio_tokens: int

class CompletionTokensDetails(BaseModel):
    reasoning_tokens: int
    audio_tokens: int
    accepted_prediction_tokens: int
    rejected_prediction_tokens: int


class BatchResponseUsage(BaseModel):
    input_tokens: int = Field(alias="prompt_tokens")
    completion_tokens: int = Field(alias="completion_tokens")
    total_tokens: int
    prompt_tokens_details: PromptTokensDetails
    completion_tokens_details: CompletionTokensDetails


class BatchResponseBody(BaseModel):
    id: str
    object: str
    created: int
    model: str
    choices: List[BatchResponseChoice]
    usage: BatchResponseUsage
    service_tier: str
    system_fingerprint: str


class BatchResponseInner(BaseModel):
    status_code: int
    request_id: str
    body: BatchResponseBody


class BatchResponse(BaseModel):
    id: str
    custom_id: BatchRequestId
    response: BatchResponseInner
    error: Any

    @field_validator('custom_id', mode="before")
    def validate_custom_id(cls, v):
        return BatchRequestId.from_str(v)
