from graphrag_llm.types import LLMCompletionMessagesParam


def format_messages(messages: "LLMCompletionMessagesParam") -> str:
    """Display chat roles and message bodies with their original line breaks."""
    if isinstance(messages, str):
        return messages
    return "\n\n".join(
        f"[{i}] {message['role']}>\n{message.get('content') or ''}"
        for i, message in enumerate(messages)
    )
