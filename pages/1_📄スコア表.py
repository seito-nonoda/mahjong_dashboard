import pandas as pd
import streamlit as st

from models.users import get_all_users
from models.yomma_scores import get_all_yomma_scores
from util.auth_utils import check_authentication

# Check authentication
check_authentication()


# constant values
## column name
ID = "id"
DISPLAY_NAME = "display_name"
DATE = "date"
PLACE = "place"
DATE_JP = "日付"
PLACE_JP = "場所"


# read data
df_user = pd.DataFrame(get_all_users())
df_yomma_score = pd.DataFrame(get_all_yomma_scores())


# create user list
user_list = df_user[DISPLAY_NAME].to_list()


# create score table dataframe
## define dictionary
player_score_dict_4 = {}
for i in range(4):
    key = "player" + str(i + 1)
    value = "score" + str(i + 1)
    player_score_dict_4[key] = value
## create dataframe
score_records = []
for _, row in df_yomma_score.iterrows():
    score_record = {DATE_JP: row[DATE], PLACE_JP: row[PLACE]}
    # create columns of all users
    for user in user_list:
        score_record[user] = None
    # set scores of parts of users
    for player, score in player_score_dict_4.items():
        player_name = df_user.loc[df_user[ID] == row[player], DISPLAY_NAME].tolist()[0]
        score = row[score]
        score_record[player_name] = score

    score_records.append(score_record)
df_score_table_yomma = pd.DataFrame(score_records)


# display title and description
st.title("📄スコア表")


# select date
date_options = df_yomma_score[DATE].drop_duplicates().sort_values(ascending=False)
selected_date = st.selectbox("日付選択", date_options)
## retrive scores of selected date
df_score_table_date = df_score_table_yomma[
    df_score_table_yomma[DATE_JP] == selected_date
]
## retrive players with any score
columns_with_any_data = df_score_table_date.columns[
    df_score_table_date.notna().any()
].tolist()
users_to_show_default = [
    player for player in columns_with_any_data if player in user_list
]


# select user
users_to_show = st.multiselect(
    "表示する人を選択", options=user_list, default=users_to_show_default
)


# display table
## calculate sum of each player's score
total = df_score_table_date[users_to_show].sum()
total = pd.DataFrame([total], columns=df_score_table_date.columns)
total.loc[0, PLACE_JP] = "合計スコア"
df_score_table_date = pd.concat([df_score_table_date, total])
## render table
columns_to_show = [PLACE_JP] + users_to_show
st.dataframe(df_score_table_date[columns_to_show], hide_index=True)
