from fastapi import FastAPI
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Emotional AI Orchestrator")

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Emotional AI orchestrator running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)))