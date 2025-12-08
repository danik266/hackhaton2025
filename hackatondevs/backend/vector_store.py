import os

# Простейший "поисковый" вектор
DOCUMENTS = []
METADATAS = []

def load_documents():
    global DOCUMENTS, METADATAS
    path = os.path.join("data", "knowledge.txt")
    if not os.path.exists(path):
        raise FileNotFoundError(f"{path} не найден")

    with open(path, encoding="utf-8") as f:
        text = f.read()

    # Разбиваем текст на абзацы
    paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
    DOCUMENTS = [[p] for p in paragraphs]
    METADATAS = [["knowledge.txt"] for _ in paragraphs]

# Поиск по тексту
def search_vectorstore(query):
    # Очень простая "поиск-по-ключевым словам"
    results = []
    for doc in DOCUMENTS:
        if query.lower() in doc[0].lower():
            results.append(doc)
    if not results:
        results = [["Информация не найдена в базе."]]
    return {"documents": results, "metadatas": [["knowledge.txt"] for _ in results]}
