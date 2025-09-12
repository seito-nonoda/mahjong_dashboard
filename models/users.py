import uuid
from typing import TypedDict

from util import db_client

USER_TABLE = "users"

def get_users_collection():
    db = db_client.get_db_client()
    return db.collection(USER_TABLE)

def get_user_document(user_id: str):
    users_ref = get_users_collection()
    return users_ref.document(user_id)

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
    id = str(uuid.uuid4())
    user_ref = get_user_document(id)

    user_ref.set(dict(record))


def get_all_users() -> list[User]:
    users_ref = get_users_collection()
    users = users_ref.stream()
    users_array: list[User] = []
    for user in users:
        dict = user.to_dict()
        dict["id"] = user.id
        users_array.append(dict)
    return users_array
