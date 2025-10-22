from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from nba_api.live.nba.endpoints import scoreboard, boxscore, odds, playbyplay
app = FastAPI()

active_games = set()

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
def todays_games():
    todays_games = get_todays_games()
    return todays_games

@app.get("/todays-games-ids")
def todays_games_ids():
    return get_todays_games_id()

@app.get("/todays-games-boxscores")
def todays_games_boxscores():
    return get_todays_games_boxscore()

def get_todays_games_boxscore():
    gameIds = get_todays_games_id()
    print("Active games:", active_games)

    boxscores = []

    default_stats = {
        "gameStatusText": "Preview",
        "homeScore": 0,
        "homeInBonus": False,
        "homeTimeoutsRemaining": 7,
        "homeTeamAssists": 0,
        "homeTeamRebounds": 0,
        "homeTeamOffensiveRebounds": 0,
        "homeTeamDefensiveRebounds": 0,
        "homeTeamTurnovers": 0,
        "awayScore": 0,
        "awayInBonus": False,
        "awayTimeoutsRemaining": 7,
        "awayTeamAssists": 0,
        "awayTeamRebounds": 0,
        "awayTeamOffensiveRebounds": 0,
        "awayTeamDefensiveRebounds": 0,
        "awayTeamTurnovers": 0,
    }

    for game_id in gameIds:
        game_stats = default_stats.copy() 

        if game_id in active_games:
            current_game = boxscore.BoxScore(game_id).get_dict()["game"]
            home_team = current_game["homeTeam"]
            away_team = current_game["awayTeam"]

            game_stats.update({
                "gameStatusText": current_game["gameStatusText"],
                "homeScore": home_team["score"],
                "homeInBonus": home_team["inBonus"],
                "homeTimeoutsRemaining": home_team["timeoutsRemaining"],
                "homeTeamAssists": home_team["statistics"]["assists"],
                "homeTeamRebounds": home_team["statistics"]["reboundsPersonal"],
                "homeTeamOffensiveRebounds": home_team["statistics"]["reboundsOffensive"],
                "homeTeamDefensiveRebounds": home_team["statistics"]["reboundsDefensive"],
                "homeTeamTurnovers": home_team["statistics"]["turnoversTotal"],
                "awayScore": away_team["score"],
                "awayInBonus": away_team["inBonus"],
                "awayTimeoutsRemaining": away_team["timeoutsRemaining"],
                "awayTeamAssists": away_team["statistics"]["assists"],
                "awayTeamRebounds": away_team["statistics"]["reboundsPersonal"],
                "awayTeamOffensiveRebounds": away_team["statistics"]["reboundsOffensive"],
                "awayTeamDefensiveRebounds": away_team["statistics"]["reboundsDefensive"],
                "awayTeamTurnovers": away_team["statistics"]["turnoversTotal"],
            })

        boxscores.append(game_stats)

    return boxscores


def get_todays_games_id():

    response = scoreboard.ScoreBoard().get_dict()["scoreboard"]["games"]
    games = []

    for i in range(len(response)):
        if response[i]["gameStatus"] != 1:
            active_games.add(response[i]["gameId"])

        games.append(response[i]["gameId"])

    return games

    
def get_todays_games():
    response = scoreboard.ScoreBoard().get_dict()["scoreboard"]["games"]
    games = []

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
            })

    return games


if __name__ == "__main__":
    
    uvicorn.run("main:app", host="0.0.0.0", port=8003, reload=True)