from dataclasses import dataclass
from typing import List, Optional
from .schema.request import BatchRequest, BatchRequestBody, BatchRequestMessage, BatchRequestMessage, BatchRequestId
from .utils import mmh3_64, uuid64

@dataclass
class BasicGen:
    model: str
    system_prompt: str

    def _generate_body(self, user_message: str) -> BatchRequestBody:
        return BatchRequestBody(
            model=self.model,
            messages=[
                BatchRequestMessage(role="system", content=self.system_prompt),
                BatchRequestMessage(role="user", content=user_message)
            ],
        )

    def generate(self, user_messages: List[str], namespace: Optional[str] = None) -> List[BatchRequest]:
        if namespace is None:
            namespace = f"req_{uuid64()}"
        return [
            BatchRequest(
                custom_id=BatchRequestId(namespace=namespace, index=i, content_hash=mmh3_64(user_message)),
                method="POST",
                url="/v1/chat/completions",
                body=self._generate_body(user_message)
            )
            for i, user_message in enumerate(user_messages)
        ]