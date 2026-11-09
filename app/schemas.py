from pydantic import BaseModel, Field
from typing import Literal


class RoutingFormat(BaseModel):
    """Роутинг: определяем интент и сразу query для API."""
    intent: Literal["food", "sport", "general"] = Field(
        description=(
            "food — вопрос о продуктах, калориях, БЖУ; "
            "sport — об упражнениях, тренировках, мышцах; "
            "general — всё остальное (ЗОЖ, мотивация, режим)"
        )
    )
    query: str = Field(
        default="",
        description=(
            "Для food — название продукта НА АНГЛИЙСКОМ (например, 'banana'). "
            "Для sport — группа мышц НА АНГЛИЙСКОМ (например, 'chest'). "
            "Для general — пустая строка."
        )
    )