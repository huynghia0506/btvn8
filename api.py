from fastapi import Body, FastAPI, HTTPException
from law import OPENAI_MODEL, load_law_data, format_law_context, get_openai_ans

app = FastAPI(
    title="API Chatbot - Luật thuế",
    description="Demo đơn giản, phục vụ cho học thuật",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"}

@app.post("/chat")
def chat(    
    question: str = Body(
        ...,
        embed=True,
    )
):
    try:
        tax_law = load_law_data()
        law_context = format_law_context(tax_law)
        answer = get_openai_ans(question, law_context)

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
    except RuntimeError as error:
        raise HTTPException(status_code=500, detail=str(error))

    return {
        "question": question,
        "answer": answer,
        "model": OPENAI_MODEL
    }

