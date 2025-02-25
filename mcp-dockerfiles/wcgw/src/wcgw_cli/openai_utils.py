from typing import cast

from openai.types.chat import (
    ChatCompletionAssistantMessageParam,
    ChatCompletionMessage,
    ChatCompletionMessageParam,
    ParsedChatCompletionMessage,
)
from tokenizers import Tokenizer  # type: ignore[import-untyped]

from wcgw.client.common import CostData, History


def get_input_cost(
    cost_map: CostData, enc: Tokenizer, history: History
) -> tuple[float, int]:
    input_tokens = 0
    for msg in history:
        content = msg["content"]
        refusal = msg.get("refusal")
        if isinstance(content, list):
            for part in content:
                if "text" in part:
                    input_tokens += len(enc.encode(part["text"]))
        elif content is None:
            if refusal is None:
                raise ValueError("Expected content or refusal to be present")
            input_tokens += len(enc.encode(str(refusal)))
        elif not isinstance(content, str):
            raise ValueError(f"Expected content to be string, got {type(content)}")
        else:
            input_tokens += len(enc.encode(content))
    cost = input_tokens * cost_map.cost_per_1m_input_tokens / 1_000_000
    return cost, input_tokens


def get_output_cost(
    cost_map: CostData,
    enc: Tokenizer,
    item: ChatCompletionMessage | ChatCompletionMessageParam,
) -> tuple[float, int]:
    if isinstance(item, ChatCompletionMessage):
        content = item.content
        if not isinstance(content, str):
            raise ValueError(f"Expected content to be string, got {type(content)}")
    else:
        if not isinstance(item["content"], str):
            raise ValueError(
                f"Expected content to be string, got {type(item['content'])}"
            )
        content = item["content"]
        if item["role"] == "tool":
            return 0, 0
    output_tokens = len(enc.encode(content))

    if "tool_calls" in item:
        item = cast(ChatCompletionAssistantMessageParam, item)
        toolcalls = item["tool_calls"]
        for tool_call in toolcalls or []:
            output_tokens += len(enc.encode(tool_call["function"]["arguments"]))
    elif isinstance(item, ParsedChatCompletionMessage):
        if item.tool_calls:
            for tool_callf in item.tool_calls:
                output_tokens += len(enc.encode(tool_callf.function.arguments))

    cost = output_tokens * cost_map.cost_per_1m_output_tokens / 1_000_000
    return cost, output_tokens
