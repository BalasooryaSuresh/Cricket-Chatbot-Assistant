# 🏏 Fantasy Cricket Chatbot Assistant

A smart, fully open-source conversational assistant that helps users make better Fantasy Cricket decisions using real historical cricket data and live score scraping — all from free sources like [CricSheet](https://cricsheet.org) and Cricbuzz.

---

## 📦 Features

* Conversational chatbot using FastAPI
* Fantasy point recommendations (batting, bowling, fielding)
* Data sourced from free YAML files (CricSheet)
* Live scores scraped from Cricbuzz
* Simple, clean HTML + Tailwind frontend with visual chart support (Chart.js)
* Fully local — no paid APIs or internet dependency once data is downloaded

---

## 📁 Project Structure

```
fantasy-cricket-chatbot/
├── data/
│   └── cricsheet/           # YAML files from cricsheet.org
├── fantasy_cricket_chatbot.py  # FastAPI backend
├── utils.py                    # Data parser, recommender, scraper
├── frontend.html               # Simple browser chat UI
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### 1️⃣ Clone and Set Up Environment

```bash
git clone https://github.com/your-repo/fantasy-cricket-chatbot.git
cd fantasy-cricket-chatbot
python -m venv venv
source venv/bin/activate   # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

### 2️⃣ Download Match Data (YAML)

1. Go to [https://cricsheet.org/downloads/](https://cricsheet.org/downloads/)
2. Download a ZIP like:

   * **All T20 matches (YAML)**
   * **IPL matches (YAML)**
3. Unzip and place `.yaml` files inside `data/cricsheet/`

### 3️⃣ Run the Backend

```bash
uvicorn fantasy_cricket_chatbot:app --reload
```

### 4️⃣ Open the Frontend

Just double-click `frontend.html` or open it in a browser.

You can now chat with:

* "Recommend a batsman"
* "Show live score"
* "How does fantasy scoring work?"

---

## ⚙️ Fantasy Scoring Rules

| Event              | Points |
| ------------------ | ------ |
| Run                | +1     |
| Four               | +1     |
| Six                | +2     |
| Wicket             | +25    |
| Catch              | +8     |
| Stumping / Run Out | +12    |

---

## 📊 Chart Integration

If the bot's reply includes fantasy scores like:

```
- Player: 420 fantasy points
```

it will automatically plot a bar chart below the chat using Chart.js.

---

## 🧪 Example Commands

* `Recommend a batsman`
* `Show live score`
* `How does scoring work?`

---

## 🤝 Contributions

Want to add filters, team builder, or player-vs-player comparisons? Fork it and PR away!

---

## 🛡️ License

MIT — free to use and modify with attribution.
