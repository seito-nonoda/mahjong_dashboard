from pathlib import Path
from typing import Optional

import firebase_admin
import streamlit as st
from firebase_admin import credentials, firestore
from google.cloud import firestore as firestore_gc


db_client: Optional[firestore_gc.Client] = None


def get_db_client() -> firestore_gc.Client:
    global db_client
    if db_client is not None:
        return db_client

    # authorization
    firebase_creds = st.secrets["firebase_service_account"]
    firebase_creds_dict = dict(firebase_creds)
    cred = credentials.Certificate(firebase_creds_dict)

    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)

    # create db client
    db_client = firestore.client()

    return db_client
