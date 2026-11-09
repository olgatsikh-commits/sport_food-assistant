from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.graph import graph


app = FastAPI(title="Sport & Nutrition Assistant")


class ChatRequest(BaseModel):
    message: str
    thread_id: str = "default"


class ChatResponse(BaseModel):
    answer: str
    intent: str
    thread_id: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    config = {"configurable": {"thread_id": req.thread_id}}
    try:
        result = graph.invoke(
            {"user_input": req.message},
            config=config,
        )
    except Exception as e:
        raise HTTPException(500, f"Ошибка агента: {e}")

    return ChatResponse(
        answer=result.get("answer", ""),
        intent=result.get("intent", "unknown"),
        thread_id=req.thread_id,
    )


@app.get("/history/{thread_id}")
def history(thread_id: str):
    config = {"configurable": {"thread_id": thread_id}}
    state = graph.get_state(config)
    if not state or not state.values:
        return {"thread_id": thread_id, "history": []}
    return {
        "thread_id": thread_id,
        "history": state.values.get("history", []),
    }