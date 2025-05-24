# fantasy_cricket_chatbot.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

from utils import parse_cricsheet_data, get_recommendation, scrape_live_stats

# === App Setup ===
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = "data/cricsheet"
MATCHES = parse_cricsheet_data(DATA_DIR)  # Preload match data

class UserQuery(BaseModel):
    query: str

# === API Routes ===
@app.post("/chat")
async def chat_with_bot(query: UserQuery):
    q = query.query.lower()

    if "recommend" in q or "pick" in q:
        return {"response": get_recommendation(MATCHES, q)}

    elif "live" in q or "score" in q:
        return {"response": scrape_live_stats()}

    elif "how does scoring work" in q:
        return {"response": "Scoring: 1 run = 1 pt, 4 = +1, 6 = +2, wicket = 25 pts, catch = 8 pts, run out/stumping = 12 pts."}

    else:
        return {"response": "Try asking something like 'Recommend a batsman' or 'Show live score'."}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
