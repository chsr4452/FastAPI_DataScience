"""Testing SQLAlchemy Helper Functions"""

import pytest
from datetime import date

import CRUD
from database import SessionLocal

# use a test date of 4/1/2024 to test the min_last_changed_date filter
test_date = date(2024, 4, 1)

@pytest.fixture(scope="function")
def db_session():
    """Create a new database session for each test."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_get_player(db_session):
    """Test that the get_player function returns the correct player."""
    player = CRUD.get_player(db_session, player_id = 1001)
    assert player.player_id == 1001

def test_get_players(db_session):
    """Test that the get_players function returns the correct players."""
    players = CRUD.get_players(db_session, skip = 0, limit = 10000,
                               min_last_changed_date = test_date)
    assert len(players) == 1018

def test_get_player_by_name(db_session):
    """ Test that the get_player_by_name function returns the correct player."""
    players = CRUD.get_players(db_session, first_name = 'Bryce', last_name = 'Young')
    assert len(players) == 1
    assert players[0].player_id == 2009

def test_get_all_performances(db_session):
    """ Test that the count of performances in the database is correct."""
    performances = CRUD.get_performances(db_session, skip = 0, limit = 18000)
    assert len(performances) == 17306

def test_get_new_performances(db_session):
    """ Test that the count of new performances in the database is correct."""
    performances = CRUD.get_performances(db_session, skip = 0, limit = 18000,
                                         min_last_changed_date = test_date)
def test_get_player_count(db_session):
    player_count = CRUD.get_player_count(db_session)
    assert player_count == 1018