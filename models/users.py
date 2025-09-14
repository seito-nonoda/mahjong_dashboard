import uuid
from typing import TypedDict

from util import db_client

USER_TABLE = "users"

def get_users_collection():
    db = db_client.get_db_client()
    return db.collection(USER_TABLE)

def get_user_document(user_id: str):
    users_col = get_users_collection()
    return users_col.document(user_id)

class UserData(TypedDict):
    display_name: str
    register_name: str
    role: str
    created_at: str
    updated_at: str

class User(UserData):
    id: str

# methods
def register_user(record: UserData) -> None:
    new_user_id = str(uuid.uuid4())
    user_doc = get_user_document(new_user_id)

    user_doc.set(dict(record))


def get_all_users() -> list[User]:
    users_col = get_users_collection()
    user_docs = users_col.stream()
    users_array: list[User] = []
    for doc in user_docs:
        user = User(**doc.to_dict(), id=doc.id)
        users_array.append(user)
    return users_array
