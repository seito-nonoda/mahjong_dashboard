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
NO = "No"


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
    score_record = {DATE: row[DATE], PLACE: row[PLACE]}
    # create columns of all users
    for user_name in user_list:
        score_record[user_name] = None
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
df_score_table_date = df_score_table_yomma[df_score_table_yomma[DATE] == selected_date]
## add No
df_score_table_date[NO] = pd.RangeIndex(start=1, stop=len(df_score_table_date) + 1)
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


# display place
place = df_score_table_date.iloc[0][PLACE]
st.text(f"場所：{place}")


# display score table
## render table
columns_to_show = [NO] + users_to_show
st.dataframe(df_score_table_date[columns_to_show], hide_index=True)


# display total table
st.text("合計スコア")
## calculate sum of each player's score
total = df_score_table_date[users_to_show].sum()
df_total = pd.DataFrame([total], columns=df_score_table_date.columns)
st.dataframe(df_total[users_to_show], hide_index=True)
