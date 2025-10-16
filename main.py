from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from nba_api.live.nba.endpoints import scoreboard, boxscore, odds, playbyplay
# Create FastAPI instance
app = FastAPI()

todays_games = []

origins = [
    "http://localhost:4203",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/todays-games")
def get_todays_game_ids():
    todays_games = set_todays_games()
    return todays_games
    
def set_todays_games():
    response = scoreboard.ScoreBoard().get_dict()["scoreboard"]["games"]
    games = []
    print(response)

    for i in range(len(response)):
        games.append(
            {
                "gameId": response[i]["gameId"],
                "homeTeam": response[i]["homeTeam"]["teamName"],
                "homeTeamWins":  response[i]["homeTeam"]["wins"],
                "homeTeamLoses": response[i]["homeTeam"]["losses"],
                "awayTeam": response[i]["awayTeam"]["teamName"],
                "awayTeamWins":  response[i]["awayTeam"]["wins"],
                "awayTeamLoses": response[i]["awayTeam"]["losses"],
            }
            )

    return games


if __name__ == "__main__":
    
    uvicorn.run("main:app", host="0.0.0.0", port=8003, reload=True)