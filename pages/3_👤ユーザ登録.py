import uuid

import streamlit as st

from util import datetime, db_client, dialogs
from util.auth_utils import check_authentication

# Check authentication
check_authentication()


# constant values
## document name
USER_TABLE = "users"
## column name
ID = "id"
DISPLAY_NAME = "display_name"
REGISTER_NAME = "register_name"
ROLE = "role"
CREATED = "created_at"
UPDATED = "updated_at"
## others
USER_JP = "ユーザ"

# methods
def register_user(record):
    users_ref = db.collection(USER_TABLE)

    id = str(uuid.uuid4())
    record_ref = users_ref.document(id)

    record_ref.set(record)

    return


# create db client
db = db_client.create_db_client()


# display title and description
st.title(f"👤ユーザ登録")


# input register name
description_register_name = """
### 登録名
- 登録名はシステムの内部でのみ使用され、他のユーザには公開されません。
- 登録名は後から変更することはできません。
"""
st.markdown(description_register_name)
register_name = st.text_input("登録名", placeholder="山田　太郎")


# input display name
description_display_name = """
### 表示名
- 表示名はスコア表等で表示される際の名前です。
- 表示名は後から変更することが可能です。
"""
st.markdown(description_display_name)
display_name = st.text_input("表示名", placeholder="やまちゃん")


# register user
if register_name and display_name:
    record = {
        DISPLAY_NAME: display_name,
        REGISTER_NAME: register_name,
        ROLE: "user",
        CREATED: datetime.retrieve_date_today(),
        UPDATED: datetime.retrieve_date_today(),
    }
    if st.button(f"{USER_JP}登録"):
        st.session_state.display_confirmation = True


# display notification dialog
if "display_confirmation" not in st.session_state:
    st.session_state.display_confirmation = False

if "display_notification" not in st.session_state:
    st.session_state.display_notification = False

if st.session_state.display_confirmation:
    dialogs.confirm_registration(USER_JP, register_user, record)

if st.session_state.display_notification:
    dialogs.notify_registration(USER_JP)
