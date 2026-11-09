import re
import requests


# ============================================================
# Инструмент 1: Open Food Facts (питание)
# ============================================================

OFF_SEARCH_URL = "https://world.openfoodfacts.org/cgi/search.pl"


def get_food_info(product_name: str, max_results: int = 3) -> str:
    """
    Получает информацию о продукте из Open Food Facts:
    калорийность, белки, жиры, углеводы.
    """
    params = {
        "search_terms": product_name,
        "search_simple": 1,
        "action": "process",
        "json": 1,
        "page_size": max_results,
        "fields": "product_name,brands,nutriments,quantity",
    }
    headers = {"User-Agent": "SportNutritionAgent/1.0"}

    try:
        resp = requests.get(
            OFF_SEARCH_URL, params=params, headers=headers, timeout=10
        )
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        return f"Не удалось получить данные о продукте «{product_name}»: {e}"

    products = data.get("products", [])
    if not products:
        return f"Продукт «{product_name}» не найден в Open Food Facts."

    lines = [f"Результаты поиска по запросу «{product_name}»:"]
    for i, p in enumerate(products, 1):
        name = p.get("product_name") or "без названия"
        brand = p.get("brands") or "бренд не указан"
        qty = p.get("quantity") or "—"
        nutr = p.get("nutriments", {})

        kcal = nutr.get("energy-kcal_100g")
        protein = nutr.get("proteins_100g")
        fat = nutr.get("fat_100g")
        carbs = nutr.get("carbohydrates_100g")

        lines.append(
            f"{i}. {name} ({brand}, {qty})\n"
            f"   На 100 г: калории={kcal} ккал, "
            f"белки={protein} г, жиры={fat} г, углеводы={carbs} г"
        )

    return "\n".join(lines)


# ============================================================
# Инструмент 2: wger (спорт/упражнения)
# ============================================================

WGER_EXERCISE_URL = "https://wger.de/api/v2/exerciseinfo/"


def get_exercises(muscle_or_type: str = "", limit: int = 3) -> str:
    """
    Получает список упражнений из wger API.
    """
    params = {"limit": limit, "language": 2}  # language=2 — английский
    headers = {"User-Agent": "SportNutritionAgent/1.0"}

    try:
        resp = requests.get(
            WGER_EXERCISE_URL, params=params, headers=headers, timeout=10
        )
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        return f"Не удалось получить упражнения: {e}"

    results = data.get("results", [])
    if not results:
        return "Упражнения не найдены."

    lines = [f"Упражнения по запросу «{muscle_or_type or 'любые'}»:"]
    for i, ex in enumerate(results, 1):
        translations = ex.get("translations", [])
        name = "без названия"
        description = ""
        for t in translations:
            if t.get("language") == 2:  # английский
                name = t.get("name", name)
                description = t.get("description", "")
                break
        if name == "без названия" and translations:
            name = translations[0].get("name", name)

        muscles = ex.get("muscles", [])
        muscle_names = ", ".join(m.get("name", "") for m in muscles) or "—"

        description = re.sub(r"<[^>]+>", "", description)[:300]

        lines.append(
            f"{i}. {name}\n"
            f"   Мышцы: {muscle_names}\n"
            f"   Описание: {description}..."
        )

    return "\n".join(lines)