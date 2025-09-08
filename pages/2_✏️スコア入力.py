import uuid

import pandas as pd
import streamlit as st

from util import datetime, db_client, dialogs
from util.auth_utils import check_authentication

# Check authentication
check_authentication()


# constant values
## document name
USER_TABLE = "users"
SCORE_TABLE = "yomma_scores"
## column name
ID = "id"
DISPLAY_NAME = "display_name"
PLACE = "place"
DATE = "date"
RATE = "rate"
CREATED = "created_at"
UPDATED = "updated_at"
DATE_JP = "日付"
YEAR = "年"
MONTH = "月"
DAY = "日"
## place options
PLACE_LIST = [
    "麻雀ZOO",
    "旅行先",
    "野々田家"
]
## others
PLAYER = "player"
SCORE = "score"
SCORE_JP = "スコア"
NUM_PLAYER = 4


# methods
def register_yomma_record(records):
    batch = db.batch()
    for record in records:
        id = str(uuid.uuid4())
        record_ref = db.collection(SCORE_TABLE).document(id)
        batch.set(record_ref, record)

    batch.commit()
    return


def validate_sum_of_scores(score_array):
    non_zero_index = [i for i, row in enumerate(score_array) if abs(sum(row)) > 0.01]
    return non_zero_index


# create db client
db = db_client.create_db_client()


# read user data
users = db.collection(USER_TABLE).stream()
users_array = []
for user in users:
    dict = user.to_dict()
    dict[ID] = user.id
    users_array.append(dict)

df_user = pd.DataFrame(users_array)

# create user list
user_list = df_user[DISPLAY_NAME].to_list()


# display title and description
st.title(f"✏️{SCORE_JP}入力")


# input date
date_input = st.date_input("日付").strftime('%Y/%m/%d')


# input place
place_input = st.selectbox('場所', PLACE_LIST, index=None, placeholder="場所を選択")


# input rate
rate_input = st.number_input("レート", value=0.3, step=0.1, format="%.1f")


# input users
st.write("ユーザ入力")

player_array = [PLAYER + str(i+1) for i in range(NUM_PLAYER)]
player_dict = {}
user_option = {}
for key in player_array:
    player_dict[key] = [""]
    user_option[key] =  st.column_config.SelectboxColumn(options=user_list)

df_player = pd.DataFrame(player_dict)
df_input_user = st.data_editor(df_player,
    num_rows="fixed",
    column_config=user_option,
    hide_index=True
)


# validation of user input
input_user_array = df_input_user.iloc[0].tolist()
num_user_input = len([input for input in input_user_array if input != ""])
is_user_set = num_user_input == NUM_PLAYER
is_duplicated = len(input_user_array) != len(set(input_user_array))


# input scores
st.write(f"{SCORE_JP}入力")

input_score_array = None
if is_user_set:
    if is_duplicated:
        st.write("ユーザに重複があります")
    else:
        # create score dataframe
        score_dict = {}
        for user in input_user_array:
            score_dict[user] = []

        df_score = pd.DataFrame(score_dict)
        input_score_array = st.data_editor(df_score,
            num_rows="dynamic",
        ).values.tolist()
else:
    st.write("ユーザを入力してください")


# register scores
score_array = [SCORE + str(i+1) for i in range(NUM_PLAYER)]
records = []
if input_score_array is not None:
    if st.button(f"{SCORE_JP}登録"):
        # TODO: 場所が選択されていないときに確認する
        validation_result = validate_sum_of_scores(input_score_array)
        validation_OK = len(validation_result) == 0
        if validation_OK:
            for score_row in input_score_array:
                record = {
                    PLACE: place_input,
                    DATE: date_input,
                    RATE: rate_input,
                    CREATED: datetime.retrieve_date_today(),
                    UPDATED: datetime.retrieve_date_today(),
                }
                for i, player in enumerate(player_array):
                    record[player] = df_user.loc[df_user[DISPLAY_NAME] == input_user_array[i], ID].tolist()[0]
                for i, score in enumerate(score_array):
                    record[score] = score_row[i]

                records.append(record)
            st.session_state.display_confirmation = True
        else:
            st.session_state.validation_result = validation_result
            st.session_state.display_validation_error = True


# display dialog
if "display_confirmation" not in st.session_state:
    st.session_state.display_confirmation = False

if "display_notification" not in st.session_state:
    st.session_state.display_notification = False

if "display_validation_error" not in st.session_state:
    st.session_state.display_validation_error = False

if st.session_state.display_confirmation:
    dialogs.confirm_registration(SCORE_JP, register_yomma_record, records)

if st.session_state.display_notification:
    dialogs.notify_registration(SCORE_JP)

if st.session_state.display_validation_error:
    dialogs.notify_validation_error(st.session_state.validation_result)
