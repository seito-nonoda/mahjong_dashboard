import firebase_admin
from firebase_admin import credentials, firestore


def create_db_client():
    # authorization
    cred = credentials.Certificate('secret/mahjong-database-fddd1-firebase-adminsdk-fbsvc-3de35d629a.json')
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)

    # create db client
    db = firestore.client()

    return db
