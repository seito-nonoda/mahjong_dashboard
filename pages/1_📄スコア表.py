import pandas as pd
import streamlit as st

from util import db_client


# constant values
## path
DATA_DIR_NAME = "data"
USER_DATA = "users.csv"
YOMMA_DATA = "yomma.csv"
## document name
USER_TABLE = "users"
SCORE_TABLE = "yomma_scores"
## column name
ID = "id"
DISPLAY_NAME = "display_name"
DATE = "date"
DATE_JP = "日付"


# create db client
db = db_client.create_db_client()


# read data
## user data
users = db.collection(USER_TABLE).stream()
users_array = []
for user in users:
    dict = user.to_dict()
    dict[ID] = user.id
    users_array.append(dict)

df_user = pd.DataFrame(users_array)
## score data
yomma_scores = db.collection(SCORE_TABLE).stream()
scores_array = []
for score in yomma_scores:
    dict = score.to_dict()
    dict[ID] = score.id
    scores_array.append(dict)

df_yomma_score = pd.DataFrame(scores_array)
df_yomma = pd.DataFrame(df_yomma_score)


# create user list
user_list = df_user[DISPLAY_NAME].to_list()


# create score table dataframe
## define dictionary
player_score_dict_4 = {}
for i in range(4):
    key = "player" + str(i+1)
    value = "score" + str(i+1)
    player_score_dict_4[key] = value
## create dataframe
score_records = []
for _, row in df_yomma.iterrows():
    score_record = {
        DATE_JP: row[DATE],
    }
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


# select user
users_to_show = st.multiselect('表示する人を選択', options=user_list, default=user_list)


# select date
date_options = df_yomma[DATE].drop_duplicates().sort_values(ascending=False)
selected_date = st.selectbox("日付選択", date_options)


# display table
columns_to_show = [DATE_JP] + users_to_show
df_score_table_date = df_score_table_yomma[df_score_table_yomma[DATE_JP] == selected_date]
st.dataframe(df_score_table_date[columns_to_show], hide_index=True)