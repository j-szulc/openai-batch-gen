from typing import ClassVar, Dict, List, Literal, Optional, Union
from pydantic import BaseModel, Field, field_serializer, field_validator
from datetime import datetime
import re


class BatchRequest(BaseModel):
    """
    Schema for individual requests in a batch input JSONL file.
    
    Each line in the JSONL file should be a JSON object conforming to this schema.
    """
    
    # Required fields
    custom_id: "BatchRequestId" = Field(
        description="A unique identifier for this request. Used to match responses to requests.",
    )
    
    method: Literal["POST"] = Field(
        default="POST",
        description="HTTP method for the request. Currently only POST is supported."
    )
    
    url: str = Field(
        default="/v1/chat/completions",
        description="The OpenAI API endpoint to call."
    )
    
    # Optional fields
    headers: Optional[Dict[str, str]] = Field(
        default=None,
        description="HTTP headers to include with the request."
    )
    
    body: "BatchRequestBody" = Field(
        default=None,
        description="Request body as a JSON object."
    )
    
    @field_serializer('custom_id')
    def serialize_custom_id(self, v: "BatchRequestId", _info) -> str:
        return v.to_str()


class BatchRequestId(BaseModel):
    NAMESPACE_REGEX : ClassVar[str] = r"[a-zA-Z0-9\-_]+"
    INDEX_REGEX : ClassVar[str] = r"[0-9]+"
    CONTENT_HASH_REGEX : ClassVar[str] = r"[a-zA-Z0-9\-]+"
    REGEX : ClassVar[str] = f"^(?P<namespace>{NAMESPACE_REGEX})_(?P<index>{INDEX_REGEX})_(?P<content_hash>{CONTENT_HASH_REGEX})$"

    namespace: str
    index: int
    content_hash: str

    def to_str(self) -> str:
        result = f"{self.namespace}_{self.index}_{self.content_hash}"
        if len(result) > 64:
            raise ValueError(f"Custom ID is too long: {result}")
        return result

    @classmethod
    def from_str(cls, s: str) -> "BatchRequestId":
        match = re.match(cls.REGEX, s)
        if not match:
            raise ValueError(f"Invalid custom_id format: {s}. Expected format: {cls.REGEX}")
        return cls(**match.groupdict())

    @field_validator('namespace')
    def validate_namespace(cls, v):
        if not re.match(cls.NAMESPACE_REGEX, v):
            raise ValueError(f"Invalid namespace format: {v}. Expected format: {cls.NAMESPACE_REGEX}")
        return v
    
    @field_validator('content_hash')
    def validate_content_hash(cls, v):
        if not re.match(cls.CONTENT_HASH_REGEX, v):
            raise ValueError(f"Invalid content hash format: {v}. Expected format: {cls.CONTENT_HASH_REGEX}")
        return v

class BatchRequestBody(BaseModel):
    """
    Schema for the request body in a batch input request.
    
    This represents the structure of the 'body' field in BatchRequest.
    """
    
    # Required fields
    model: str = Field(
        description="The model to use for the completion request."
    )
    
    messages: List["BatchRequestMessage"] = Field(
        description="A list of messages comprising the conversation so far.",
        min_items=1
    )
    
    # Optional fields
    temperature: Optional[float] = Field(
        default=None,
        description="Controls randomness: Lowering results in less random completions.",
        ge=0.0,
        le=2.0
    )
    
    top_p: Optional[float] = Field(
        default=None,
        description="Controls diversity via nucleus sampling: 0.5 means half of all likelihood-weighted options are considered.",
        ge=0.0,
        le=1.0
    )
    
    n: Optional[int] = Field(
        default=None,
        description="How many completions to generate for each prompt.",
        ge=1,
        le=128
    )
    
    stream: Optional[bool] = Field(
        default=False,
        description="Whether to stream back partial progress."
    )
    
    stop: Optional[Union[str, List[str]]] = Field(
        default=None,
        description="Up to 4 sequences where the API will stop generating further tokens."
    )
    
    max_tokens: Optional[int] = Field(
        default=None,
        description="The maximum number of tokens to generate.",
        ge=1
    )
    
    presence_penalty: Optional[float] = Field(
        default=None,
        description="Number between -2.0 and 2.0. Positive values penalize new tokens based on whether they appear in the text so far.",
        ge=-2.0,
        le=2.0
    )
    
    frequency_penalty: Optional[float] = Field(
        default=None,
        description="Number between -2.0 and 2.0. Positive values penalize new tokens based on their existing frequency in the text so far.",
        ge=-2.0,
        le=2.0
    )

    max_completion_tokens: Optional[int] = Field(
        default=None,
        description="The maximum number of tokens to generate.",
        ge=1
    )
    
    logit_bias: Optional[Dict[str, float]] = Field(
        default=None,
        description="Modify the likelihood of specified tokens appearing in the completion."
    )
    
    user: Optional[str] = Field(
        default=None,
        description="A unique identifier representing your end-user."
    )

class BatchRequestMessage(BaseModel):
    """
    Schema for individual messages within a batch input request.
    
    This represents the structure of each message in the 'messages' list of BatchRequestBody.
    """
    
    # Required fields
    role: Literal["system", "user", "assistant"] = Field(
        description="The role of the author of this message."
    )
    
    content: str = Field(
        description="The contents of the message.",
        min_length=1
    )
    
    # Optional fields
    name: Optional[str] = Field(
        default=None,
        description="The name of the author of this message. May contain a-z, A-Z, 0-9, and underscores, with a maximum length of 64 characters."
    )
    
    # Unimplemented!
    #
    # function_call: Optional[Dict[str, Any]] = Field(
    #     default=None,
    #     description="The name and arguments of a function that should be called, as generated by the model."
    # )
    
    # tool_calls: Optional[List[Dict[str, Any]]] = Field(
    #     default=None,
    #     description="The tool calls generated by the model, such as function calls."
    # )
    
    @field_validator('name')
    def validate_name(cls, v):
        """Validate name format if provided."""
        if v is not None:
            if len(v) > 64:
                raise ValueError('Name must be 64 characters or less')
            if not v.replace('_', '').isalnum():
                raise ValueError('Name must contain only alphanumeric characters and underscores')
        return v
    
    @field_validator('content')
    def validate_content(cls, v):
        """Validate content is not empty."""
        if not v or not v.strip():
            raise ValueError('Content cannot be empty or whitespace only')
        return v.strip()



