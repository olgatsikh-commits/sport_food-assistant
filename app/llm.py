from typing import List, Dict, Optional, Type
from pydantic import BaseModel
from gigachat import GigaChat
from gigachat.models import (
    Chat,
    Function,
    FunctionParameters,
    Messages,
    MessagesRole,
)

from app.config import settings


def llm_call(
    dialog: List[Dict[str, str]],
    structure: Optional[Type[BaseModel]] = None,
    temperature: float = 0.0,
):
    """
    Унифицированная обёртка над GigaChat.

    :param dialog: список сообщений [{'role': 'system'|'user'|'assistant', 'content': str}]
    :param structure: Pydantic-схема для структурной генерации (опционально)
    :param temperature: температура генерации
    :return: строка (если structure=None) или dict (если structure задана)
    """
    client = GigaChat(
        credentials=settings.GIGACHAT_KEY,
        verify_ssl_certs=False,
        scope=settings.GIGACHAT_SCOPE,
        model=settings.GIGACHAT_MODEL,
    )

    roles_dict = {
        "system": MessagesRole.SYSTEM,
        "user": MessagesRole.USER,
        "assistant": MessagesRole.ASSISTANT,
    }

    gigachat_messages = [
        Messages(role=roles_dict[m["role"]], content=m["content"])
        for m in dialog
    ]

    if structure:
        schema = structure.model_json_schema()
        answer_function = Function(
            name="llm_answer",
            description="Используй эту функцию для формирования ответа пользователю",
            parameters=FunctionParameters(
                type=schema["type"],
                properties=schema["properties"],
                required=schema.get("required", []),
            ),
        )
        chat = Chat(
            messages=gigachat_messages,
            temperature=temperature,
            max_tokens=1024,
            functions=[answer_function],
            function_call=answer_function,
        )
        response = client.chat(chat).choices[0]

        assert response.finish_reason == "function_call", (
            "GigaChat не вернул объект функции. "
            "Попробуйте ещё раз или перепишите промпт."
        )
        return response.message.function_call.arguments

    chat = Chat(
        messages=gigachat_messages,
        temperature=temperature,
        max_tokens=1024,
    )
    return client.chat(chat).choices[0].message.content