from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from settings_ai.groq_client import ask_groq

app = FastAPI(title="Groq API", version="1.0")

class GroqRequest(BaseModel):
    query: str

class GroqResponse(BaseModel):
    result: str
@app.post("/groq", response_model=GroqResponse)
def run_groq(request: GroqRequest):
    try:
        result = ask_groq(request.query)  
        return GroqResponse(result=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)