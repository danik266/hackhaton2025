import csv
import os
from .gemini_client import GeminiClient

YOUR_GEMINI_API_KEY = "AIzaSyDRIJY83ST_yLjK7zauDDK3xGg6R-gtGQQ"
gemini = GeminiClient(api_key=YOUR_GEMINI_API_KEY)

def load_knowledge(filename="data/drugs.csv"):
    base_path = os.path.dirname(__file__)
    full_path = os.path.join(base_path, filename)

    knowledge = {}
    with open(full_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            knowledge[row["Название"]] = row
    return knowledge

knowledge = load_knowledge()

def get_answer(user_query: str):
    # ищем релевантные препараты
    relevant_drugs = []
    for name, info in knowledge.items():
        if name.lower() in user_query.lower():
            relevant_drugs.append(info)

    if not relevant_drugs:
        relevant_drugs = list(knowledge.values())  # fallback: все препараты

    context_texts = []
    for info in relevant_drugs:
        context_texts.append(
            f"Название: {info['Название']}\n"
            f"Группа: {info['Группа']}\n"
            f"Инструкция: {info['Инструкция']}\n"
            f"Источник: {info['Источник']}\n"
        )
    context = "\n---\n".join(context_texts)

    prompt = f"""
Используй только этот контекст для ответа на вопрос. Не придумывай ничего. 
Ответ должен быть кратким, понятным, без Markdown, без звездочек.

Контекст:
{context}

Вопрос пользователя: {user_query}

Ответ:
"""

    try:
        response = gemini.generate(prompt)

        # Объединяем текст из parts или candidates
        if isinstance(response, dict):
            if "parts" in response:
                text = "".join([p.get("text", "") for p in response.get("parts", [])])
            elif "candidates" in response:
                text = "".join([p.get("content", "") for p in response.get("candidates", [])])
            else:
                text = str(response)
        else:
            text = str(response)

        return {"answer": text, "sources": [", ".join([d["Источник"] for d in relevant_drugs])]}

    except Exception:
        # fallback: часть инструкции первых 2-3 препаратов
        fallback_texts = []
        for info in relevant_drugs[:3]:
            fallback_texts.append(f"{info['Название']}: {info['Инструкция'][:200]}...")
        return {"answer": "\n".join(fallback_texts), "sources": [", ".join([d["Источник"] for d in relevant_drugs[:3]])]}
