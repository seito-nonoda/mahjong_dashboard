import uuid
from typing import Sequence, TypedDict

from util import db_client

YOMMA_SCORE_TABLE = "yomma_scores"

def get_yomma_scores_collection():
    db = db_client.get_db_client()
    return db.collection(YOMMA_SCORE_TABLE)

def get_yomma_score_document(user_id: str):
    users_ref = get_yomma_scores_collection()
    return users_ref.document(user_id)

class YommaScoreData(TypedDict):
    date: str
    place:str
    player1: str
    score1: float
    player2: str
    score2: float
    player3: str
    score3: float
    player4: str
    score4: float
    rate: float
    created_at: str
    updated_at: str

class YommaScore(YommaScoreData):
    id: str

# methods
def register_yomma_scores(records: Sequence[YommaScoreData]):
    db = db_client.get_db_client()
    batch = db.batch()
    for record in records:
        id = str(uuid.uuid4())
        record_ref = db.collection(YOMMA_SCORE_TABLE).document(id)
        batch.set(record_ref, dict(record))

    batch.commit()
    return

def get_all_yomma_scores() -> list[YommaScore]:
    yomma_scores_ref = get_yomma_scores_collection()
    scores = yomma_scores_ref.stream()
    scores_array: list[YommaScore] = []
    for score in scores:
        dict = score.to_dict()
        dict["id"] = score.id
        scores_array.append(dict)
    return scores_array
