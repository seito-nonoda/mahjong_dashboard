from pathlib import Path

import pandas as pd
import streamlit as st


# constant values
## path
DATA_DIR_NAME = "data"
USER_DATA = "users.json"
YOMMA_DATA = "yomma.json"
## column name
ID = "id"
DISPLAY_NAME = "display_name"
DATE = "date"
DATE_JP = "日付"
## dictonary


# methods



# read data
data_dir =  Path(__file__).parent.parent / DATA_DIR_NAME
## user data
user_data_path = data_dir / USER_DATA
df_user = pd.read_json(user_data_path)
## score data
yomma_data_path = data_dir / YOMMA_DATA
df_yomma = pd.read_json(yomma_data_path)


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
        DATE_JP: row[DATE].strftime("%Y/%m/%d"),
    }
    for player, score in player_score_dict_4.items():
        player_name = df_user.loc[df_user[ID] == row[player], DISPLAY_NAME].tolist()[0]
        score = row[score]
        score_record[player_name] = score

    score_records.append(score_record)
df_score_table_yomma = pd.DataFrame(score_records)


# display title and description
st.title("📄スコア表")
st.write("スコア表が見られます")


# select user
users_to_show = st.multiselect('表示する人を選択', options=user_list, default=user_list)


# display table
columns_to_show = [DATE_JP] + users_to_show
st.dataframe(df_score_table_yomma[columns_to_show], hide_index=True)