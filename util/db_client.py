from pathlib import Path

import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st


SECRET_DIR = "secret"


def create_db_client():
    # authorization
    secret_path = Path(SECRET_DIR)
    secret_file = None
    for file in secret_path.iterdir():
        if file.is_file():
            secret_file = file.name

    if secret_file is None:
        # retrieve secret from streamlit settings
        firebase_creds = st.secrets["firebase_service_account"]
        firebase_creds_dict = dict(firebase_creds)
        cred = credentials.Certificate(firebase_creds_dict)

    else:
        # retrieve secret from local file
        secret_path = secret_path / secret_file
        cred = credentials.Certificate(str(secret_path))

    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)

    # create db client
    db = firestore.client()

    return db
