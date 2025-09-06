import pandas as pd
import streamlit as st

import firebase_admin
from firebase_admin import credentials

from util import db_client


# constant values
## path
DATA_DIR_NAME = "data"
USER_DATA = "users.csv"
YOMMA_DATA = "yomma.csv"
## column name
ID = "id"
DISPLAY_NAME = "display_name"
DATE = "date"
DATE_JP = "日付"


# create database client
cred = credentials.Certificate("path/to/serviceAccountKey.json")
firebase_admin.initialize_app(cred)


# read data
data_dir =  Path(__file__).parent.parent / DATA_DIR_NAME
## user data
user_data_path = data_dir / USER_DATA
df_user = pd.read_csv(user_data_path)
## score data
yomma_data_path = data_dir / YOMMA_DATA
df_yomma = pd.read_csv(yomma_data_path)


# create user list
user_list = df_user[DISPLAY_NAME].to_list()


# create score table dataframe
## define dictionary
player_score_dict_4 = {}
for i in range(4):
    key = "_".join(["player", str(i+1)])
    value = "_".join(["score", str(i+1)])
    player_score_dict_4[key] = value
## create dataframe
score_records = []
for _, row in df_yomma.iterrows():
    score_record = {
        DATE_JP: row[DATE],
    }
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