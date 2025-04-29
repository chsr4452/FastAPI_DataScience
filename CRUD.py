"""SQLAlchemy CRUD"""

from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from datetime import date

import models

def get_player(db: Session, player_id: int):
    return db.query(models.Player).filter(
        models.Player.player_id == player_id).first()
