from typing import List, Dict, Optional, Type
import json
from pydantic import BaseModel
from gigachat import GigaChat
from gigachat.models import Chat, Function, FunctionParameters, Messages, MessagesRole

from app.config import settings

def llm_call(dialog: List[Dict[str, str]], structure: Optional[Type[BaseModel]] = None, temperature: float = 0.0):
    client = GigaChat(
        access_token=settings.GIGACHAT_KEY,
        base_url=settings.GIGACHAT_BASE_URL,
        model=settings.GIGACHAT_MODEL,
        verify_ssl_certs=False,
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
        
        print("=== ОТЛАДКА GIGACHAT ===")
        print("Finish reason:", response.finish_reason)
        print("Content:", repr(response.message.content))
        print("Function call:", response.message.function_call)
        print("========================")
        
        if response.finish_reason == "function_call" and response.message.function_call:
            return response.message.function_call.arguments
        
        content = response.message.content
        if content:
            try:
                start = content.find('{')
                end = content.rfind('}') + 1
                if start != -1 and end != 0:
                    json_str = content[start:end]
                    return json.loads(json_str)
                return json.loads(content)
            except Exception as e:
                raise ValueError(f"Не JSON. Ответ: {content}. Ошибка: {e}")
        raise ValueError("Пустой ответ.")

    chat = Chat(
        messages=gigachat_messages,
        temperature=temperature,
        max_tokens=1024,
    )
    response = client.chat(chat).choices[0]
    return response.message.content