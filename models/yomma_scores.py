import uuid
from typing import Sequence, TypedDict

from util import db_client

YOMMA_SCORE_TABLE = "yomma_scores"

def get_yomma_scores_collection():
    db = db_client.get_db_client()
    return db.collection(YOMMA_SCORE_TABLE)

def get_yomma_score_document(user_id: str):
    yomma_score_col = get_yomma_scores_collection()
    return yomma_score_col.document(user_id)

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
    col = get_yomma_scores_collection()
    batch = db.batch()
    for record in records:
        new_id = str(uuid.uuid4())
        doc = col.document(new_id)
        batch.set(doc, dict(record))

    batch.commit()
    return

def get_all_yomma_scores() -> list[YommaScore]:
    yomma_scores_col = get_yomma_scores_collection()
    yomma_score_docs = yomma_scores_col.stream()
    scores_array: list[YommaScore] = []
    for doc in yomma_score_docs:
        yomma_score = YommaScore(**doc.to_dict(), id=doc.id)
        scores_array.append(yomma_score)
    return scores_array
