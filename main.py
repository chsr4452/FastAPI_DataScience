""" FastAPI program"""

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import date

import CRUD, schemas
from database import SessionLocal


api_description = """
This API provides read-only access to info from the SportsWorldCentral
(SWC) Fantasy Football API.
The endpoints are grouped into the following categories:

## Analytics
Get information about the health of the API and counts of leagues, teams,
and players.

## Player
You can get a list of NFL players, or search for an individual player by
player_id.

## Scoring
You can get a list of NFL player performances, including the fantasy points
they scored using SWC league scoring.

## Membership
Get information about all the SWC fantasy football leagues and the teams in them.
"""

title = "SportsWorldCentral Fantasy Football API"
app = FastAPI(description=api_description, title = title, version = "Alpha")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", tags = ["analytics"])
def read_root():
    return {"message": "API health check successful"}

@app.get("/v0/players", response_model = list[schemas.Player], tags = ["player"])
def read_players(skip:int = Query(0, description = "The number of items to skip at the beginning of API call."), limit:int = Query(100, description = "The maximum number of items to return in the API call."),
                 minimum_last_changed_date:date = Query(None, description = "The minimum last_changed_date of players to return in the API call."),
                 first_name:str = Query(None, description = "The first name of the player to return in the API call."),
                 last_name:str = Query(None, description = "The last name of the player to return in the API call."),
                 db: Session = Depends(get_db)):
    players = CRUD.get_players(db, skip=skip, limit = limit, min_last_changed_date=minimum_last_changed_date,
                               first_name = first_name, last_name = last_name)
    return players

@app.get("/v0/players/{player_id}", response_model = schemas.Player,
         summary = "Get one player using the Player ID, which is internal to SWC",
         description = "This endpoint is used to get information about a single player. The Player ID is internal to SWC and is not the same as the player's unique ID.",
         response_description = "A single player object",
         operation_id= "get_player_by_id",
         tags = ["player"])
def read_player(player_id:int, db: Session = Depends(get_db)):
    player = CRUD.get_player(db, player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player

@app.get("/v0/performances", response_model = list[schemas.Performance], tags = ["scoring"])
def read_performances(skip:int = 0, limit:int = 100,
                      minimum_last_changed_date:date = None,
                      db: Session = Depends(get_db)):
    performances = CRUD.get_performances(db, skip=skip, limit=limit, min_last_changed_date=minimum_last_changed_date)
    return performances

@app.get("/v0/leagues/{league_id}", response_model = schemas.League, tags = ["membership"])
def read_league(league_id:int, db: Session = Depends(get_db)):
    league = CRUD.get_league(db, league_id=league_id)
    if not league:
        raise HTTPException(status_code=404, detail="League not found")
    return league

@app.get("/v0/leagues/", response_model = list[schemas.League], tags = ["membership"])
def read_leagues(skip:int = 0, limit:int = 100,
                 min_last_changed_date:date = None,
                 league_name:str = None,
                 db: Session = Depends(get_db)):
    leagues = CRUD.get_leagues(db, skip=skip, limit=limit,
                               min_last_changed_date=min_last_changed_date,
                               league_name=league_name)
    return leagues

@app.get("/v0/teams/", response_model=list[schemas.Team], tags = ["membership"])
def read_teams(skip:int = 0, limit:int = 100,
               min_last_changed_date:date = None,
               team_name:str = None,
               league_id:int = None,
               db: Session = Depends(get_db)):
    teams = CRUD.get_teams(db, skip=skip, limit=limit,
                           min_last_changed_date=min_last_changed_date,
                           team_name=team_name,
                           league_id=league_id)
    return teams

@app.get("/v0/counts/", response_model=schemas.Counts, tags = ["analytics"])
def read_counts(db:Session = Depends(get_db)):
    counts = schemas.Counts(league_count = CRUD.get_league_count(db),
                            team_count = CRUD.get_team_count(db),
                            player_count = CRUD.get_player_count(db))
    return counts

@app.get("/v0/test/", tags = ["test"])
def read_test():

    return {"message": "Test Successful."}
