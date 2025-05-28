from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn,threading, webbrowser
import pickle
import os
from utils import load_or_train_model, live_scores, answer_faq, PlayerFeatureHistory, get_role_stats
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from difflib import get_close_matches
from collections import defaultdict
import numpy as np
# Constants
DATA_DIR = "./data/cricsheet"
MODEL_PATH = "./model.pkl"
INDEX_FILE = "./index.html"
#these pointed files are main files now few files which i initllay deeleted will be added later after training the 
# Load model
print("⏳ Training / loading ML model …")
MODEL, PLAYER_LOOKUP, PLAYER_ROLES = load_or_train_model(DATA_DIR, MODEL_PATH)
print("✅ Model loaded successfully!")
app = FastAPI()

# Serve index.html
@app.get("/", response_class=HTMLResponse)
async def serve_index():
    return FileResponse(INDEX_FILE)

# Static file mount (if you want to serve CSS/JS separately later)
app.mount("/static", StaticFiles(directory="."), name="static")

# Allow same-origin JS fetch
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Can restrict if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    query: str

from fastapi.responses import JSONResponse
import json

@app.get("/leaderboard")
def leaderboard():
    try:
        with open("leaderboard.json", "r") as f:
            data = json.load(f)
        return JSONResponse(content=data)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/chat")
async def chat(query: Query):
    text = query.query.lower()
    
    # FAQs
    faq_response = answer_faq(text)
    if faq_response:
        return {"response": faq_response}
    
    if "leaderboard" in text:
        try:
            with open("leaderboard.json", "r") as f:
                leaderboard_data = json.load(f)
            return {"response": "Leaderboard loaded successfully!"}
        except Exception as e:
            return {"response": f"Error loading leaderboard: {str(e)}"}

    # Live scores
    if "live" in text or "score" in text:
        return {"response": live_scores()}

    # Recommendations
    if "recommend" in text or "suggest" in text:
        if "bat" in text:
            role = "batsman"
        elif "bowl" in text:
            role = "bowler"
        else:
            role = None

        candidates = [(name, pf) for name, pf in PLAYER_LOOKUP.items()
                      if role is None or PLAYER_ROLES.get(name) == role]

        if not candidates:
            return {"response": f"No {role or 'players'} found in data."}

        scored = [(name, MODEL.predict([pf.to_vector()])[0]) for name, pf in candidates]
        top = sorted(scored, key=lambda x: x[1], reverse=True)[:5]
        top_names = [f"{i+1}. {name} ({score:.2f} pts)" for i, (name, score) in enumerate(top)]
        return {"response": "Top players:\n" + "\n".join(top_names)}

    return {"response": "🤖 I didn't understand that. Try 'recommend batsman' or 'live scores'."}

@app.get("/role-stats")
def role_stats():
    role_avgs = defaultdict(list)
    for player, role in PLAYER_ROLES.items():
        if player in PLAYER_LOOKUP:
            vec = PLAYER_LOOKUP[player].to_vector()
            pred = MODEL.predict([vec])[0]
            role_avgs[role].append(pred)
    return {
        role: round(np.mean(pts), 2) for role, pts in role_avgs.items() if pts
    }


@app.get("/refresh")
def retrain_model():
    global MODEL, PLAYER_LOOKUP, PLAYER_ROLES
    MODEL, PLAYER_LOOKUP, PLAYER_ROLES = load_or_train_model(DATA_DIR, MODEL_PATH)
    return {"message": "Model retrained successfully."}

@app.get("/fuzzy-player")
def fuzzy_search(q: str):
    players = list(PLAYER_LOOKUP.keys())
    matches = get_close_matches(q, players, n=5, cutoff=0.6)
    return {"matches": matches}


# ---------- AUTO-LAUNCH ----------
def open_browser():
    webbrowser.open_new("http://127.0.0.1:8000")
if __name__ == "__main__":
    threading.Timer(1.2, open_browser).start()
    
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=False)
