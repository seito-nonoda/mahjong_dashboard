import streamlit as st

from util.auth_utils import get_authenticator

# Create authenticator object
authenticator = get_authenticator()

authentication_status = st.session_state.get("authentication_status")

if not authentication_status:
    # Render login widget
    authenticator.login()

    if authentication_status is False:
        st.error("ユーザー名またはパスワードが間違っています")
    elif authentication_status is None:
        st.warning("ユーザー名とパスワードを入力してください")
    st.stop()

st.title("麻雀結果集計ツール")
description = """
### 麻雀の結果を登録、表示するツールです
 機能一覧
- 📄スコア表
  - スコア表の形式で結果を見ることができます
- ✏️スコア入力
  - スコアを入力することができます
- 👤ユーザ登録
  - ユーザを登録することができます
"""
st.markdown(description)

# Show logout button
authenticator.logout("ログアウト")
