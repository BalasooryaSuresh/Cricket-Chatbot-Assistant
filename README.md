# Fantasy Cricket Chatbot

## Overview
The **Fantasy Cricket Chatbot** is a web-based application built with FastAPI that provides fantasy cricket recommendations, live cricket scores, player statistics, and a leaderboard. It uses machine learning (GradientBoostingRegressor) to predict player performance based on historical match data from CricSheet. The frontend is a simple HTML interface, and the backend processes user queries to recommend players, display live scores, and provide role-based statistics.

## Features
- **Player Recommendations**: Suggests top-performing players (batsmen or bowlers) based on historical performance.
- **Live Scores**: Fetches real-time cricket match scores from CricBuzz.
- **Role-wise Statistics**: Displays average points per role (e.g., batsman, bowler).
- **Fuzzy Player Search**: Allows searching for players with approximate name matching.
- **Leaderboard**: Shows the top 10 players by average fantasy points.
- **Model Retraining**: Supports refreshing the ML model with updated data.

## Project Structure
- **`fantasy_cricket_chatbot.py`**: The main FastAPI application file that defines API endpoints, serves the frontend, and handles user queries.
- **`utils.py`**: Contains utility functions for data parsing, model training, live score fetching, and FAQ handling.
- **`index.html`**: The frontend HTML file providing a user interface for interacting with the chatbot.
- **`requirements.txt`**: Lists the Python dependencies required to run the project.
- **`data/cricsheet`**: Directory (not included) where CricSheet YAML files should be placed for model training.
- **`model.pkl`**: Stores the trained ML model, player lookup, and roles (generated after training).
- **`leaderboard.json`**: Stores the leaderboard data (generated after training).
- **`performance_plot.png`**: A plot of model prediction performance (generated after training).

## Prerequisites
- **Python**: Version 3.8 or higher.
- **CricSheet Data**: Download YAML match data from [CricSheet](https://cricsheet.org/) and place it in the `./data/cricsheet` directory.
- **Internet Connection**: Required for fetching live scores from CricBuzz.

## Installation
1. **Clone the Repository** (if applicable) or ensure all provided files are in the project directory.
2. **Create a Virtual Environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Prepare Data**:
   - Create a `./data/cricsheet` directory.
   - Download and extract CricSheet YAML files into `./data/cricsheet`.

## Running the Application
1. Run the main script:
   ```bash
   python fantasy_cricket_chatbot.py
   ```
2. The application will start a FastAPI server at `http://127.0.0.1:8000` and automatically open the interface in your default browser.
3. Interact with the chatbot via the web interface or API endpoints.

## Usage
### Web Interface
- **Chat**: Enter queries like "recommend batsman", "live scores", or "how does scoring work" in the chat input box.
- **Role Stats**: View average points for batsmen and bowlers (updates on button click).
- **Fuzzy Search**: Search for players by name with approximate matching.
- **Leaderboard**: View the top 10 players by average fantasy points.
- **Model Refresh**: Retrain the ML model with updated data.

### API Endpoints
- `GET /`: Serves the `index.html` frontend.
- `POST /chat`: Processes user queries (e.g., `{"query": "recommend batsman"}`).
- `GET /leaderboard`: Returns the top 10 players in JSON format.
- `GET /role-stats`: Returns average points per player role.
- `GET /refresh`: Retrains the ML model.
- `GET /fuzzy-player?q=<player_name>`: Returns up to 5 player names matching the query.

### Example Queries
- "Recommend batsman" → Lists top 5 batsmen with predicted fantasy points.
- "Live scores" → Fetches current match scores from CricBuzz.
- "How does scoring work" → Explains the fantasy points system.
- "Leaderboard" → Displays top players from `leaderboard.json`.

## Scoring System
- **Batting**: 1 point per run, +1 for a four, +2 for a six.
- **Bowling**: 25 points per wicket.
- **Fielding**: 8 points for a catch, 12 points for a stumping or run-out.

## Model Details
- **Algorithm**: GradientBoostingRegressor from scikit-learn.
- **Features**: Average and standard deviation of a player's last 10 performances.
- **Data**: CricSheet YAML files containing match deliveries.
- **Output**: Predicted fantasy points for each player.

## Notes
- Ensure the `./data/cricsheet` directory contains valid YAML files for model training.
- The model is trained on startup if `model.pkl` does not exist, which may take time depending on the data size.
- Live scores depend on CricBuzz availability and may fail if the site is down or the structure changes.
- The frontend is basic and can be enhanced with CSS/JavaScript for better styling and interactivity.

## Troubleshooting
- **Model Training Fails**: Check that `./data/cricsheet` contains valid YAML files and that dependencies like `numpy` and `sklearn` are installed.
- **Live Scores Error**: Verify internet connectivity and CricBuzz site availability.
- **CORS Issues**: The CORS middleware allows all origins (`*`), but you can restrict it in `fantasy_cricket_chatbot.py` if needed.

## Future Improvements
- Enhance the frontend with CSS and JavaScript for a better user experience.
- Add support for more complex queries (e.g., team-specific recommendations).
- Implement caching for live scores to reduce API calls.
- Expand the FAQ system with more questions and answers.

## License
This project is provided as-is for educational purposes. Ensure compliance with CricSheet and CricBuzz terms of use for data and API access.
