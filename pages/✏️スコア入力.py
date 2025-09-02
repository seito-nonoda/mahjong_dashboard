import csv
from pathlib import Path
import uuid

import pandas as pd
import streamlit as st

from util import datetime, dialogs


# constant values
## path
DATA_DIR_NAME = "data"
USER_DATA = "users.csv"
YOMMA_DATA = "yomma.csv"
## column name
ID = "id"
DISPLAY_NAME = "display_name"
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
SCORE = "スコア"
NUM_PLAYER = 4


# methods
def register_yomma_record(records):
    print(records)
    output_path = data_dir / YOMMA_DATA
    with open(output_path,  "a", newline="", encoding="utf-8")as f:
        writer = csv.writer(f)
        writer.writerows(records)
    return


# read data
data_dir =  Path(__file__).parent.parent / DATA_DIR_NAME
## user data
user_data_path = data_dir / USER_DATA
df_user = pd.read_csv(user_data_path)


# create user list
user_list = df_user[DISPLAY_NAME].to_list()


# display title and description
st.title(f"✏️{SCORE}入力")


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
df_input_user = st.data_editor(df_player, num_rows="fixed", column_config=user_option, hide_index=True)


# validation of user input
input_user_array = df_input_user.iloc[0].tolist()
num_user_input = len([input for input in input_user_array if input != ""])
is_user_set = num_user_input == NUM_PLAYER
is_duplicated = len(input_user_array) != len(set(input_user_array))


# input scores
st.write(f"{SCORE}入力")

df_input_score = None
if is_user_set:
    if is_duplicated:
        st.write("ユーザに重複があります")
    else:
        # create score dataframe
        score_dict = {}
        for user in input_user_array:
            score_dict[user] = []

        df_score = pd.DataFrame(score_dict)
        df_input_score = st.data_editor(df_score, num_rows="dynamic").values.tolist()
else:
    st.write("ユーザを入力してください")


# register scores
if df_input_score is not None:
    # TODO: validation of scores
    if st.button(f"{SCORE}登録"):
        id = str(uuid.uuid4())
        input_userid_array = [df_user.loc[df_user[DISPLAY_NAME] == user, ID].tolist()[0] for user in input_user_array]
        created_date = datetime.retrieve_date_today()
        records = [
            [id] +
            input_userid_array +
            score +
            [place_input] +
            [date_input] +
            [rate_input] +
            [created_date] +
            [""] for score in df_input_score
        ]
        dialogs.confirm_registration(SCORE, register_yomma_record, records)
