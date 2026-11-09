from typing_extensions import TypedDict
from typing import List


class AgentState(TypedDict, total=False):
    user_input: str
    intent: str          # food / sport / general
    query: str           # для API
    tool_result: str     # сырые данные
    answer: str          # финальный ответ
    history: List[dict]  # история диалога