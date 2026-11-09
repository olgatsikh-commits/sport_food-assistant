from app.llm import llm_call
from app.schemas import RoutingFormat
from app.state import AgentState
from app.tools import get_food_info, get_exercises


ROUTER_PROMPT = """Ты — спортивный и nutritional ассистент.

Определи категорию запроса:
- food — вопросы о продуктах, калориях, БЖУ, питании
- sport — вопросы об упражнениях, тренировках, мышцах
- general — всё остальное (ЗОЖ, мотивация, режим)

Верни JSON:
- intent: food / sport / general
- query: для food — название продукта на английском (например, "banana");
         для sport — группа мышц на английском (например, "chest");
         для general — пустая строка
"""


def router_node(state: AgentState) -> dict:
    """GigaChat определяет интент и query для API."""
    dialog = [
        {"role": "system", "content": ROUTER_PROMPT},
        {"role": "user", "content": state["user_input"]},
    ]
    result = llm_call(dialog, structure=RoutingFormat)
    return {
        "intent": result["intent"],
        "query": result.get("query", ""),
    }


def food_node(state: AgentState) -> dict:
    """Open Food Facts — КБЖУ продукта."""
    query = state.get("query") or state["user_input"]
    return {"tool_result": get_food_info(query)}


def sport_node(state: AgentState) -> dict:
    """wger — упражнения."""
    query = state.get("query") or ""
    return {"tool_result": get_exercises(query)}


def response_node(state: AgentState) -> dict:
    """GigaChat формирует финальный ответ."""
    tool_result = state.get("tool_result", "")

    system_prompt = (
        "Ты — Sport & Nutrition Assistant. Отвечай кратко, "
        "по делу, на русском языке."
    )
    user_prompt = state["user_input"]
    if tool_result:
        user_prompt += f"\n\nДанные из API:\n{tool_result}"

    dialog = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    answer = llm_call(dialog)

    history = state.get("history", []) + [
        {"role": "user", "content": state["user_input"]},
        {"role": "assistant", "content": answer},
    ]

    return {
        "answer": answer,
        "history": history,
    }