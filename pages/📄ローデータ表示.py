from pathlib import Path

import pandas as pd
import streamlit as st


# constant values
DATA_DIR = "data"
YOMMA_DATA = "yomma.json"


# display title and description
st.title("📄ローデータ表示")
st.write("入力されたままのデータが見られます")


# read data
current_file_path = Path(__file__)
yomma_data_path = current_file_path.parent.parent / DATA_DIR / YOMMA_DATA
df = pd.read_json(yomma_data_path)


# display data
st.dataframe(df)