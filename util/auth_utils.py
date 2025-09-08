import streamlit as st
import streamlit_authenticator as stauth


def get_authenticator() -> stauth.Authenticate:
    return stauth.Authenticate(
        {
            "usernames": {
                st.secrets["auth"]["username"]: {
                    "email": "test@example.com",
                    "name": "Test User",
                    "password": st.secrets["auth"]["password"],
                }
            }
        },
        st.secrets["auth"]["cookie_name"],
        st.secrets["auth"]["cookie_key"],
        st.secrets["auth"]["cookie_expiry_days"],
        None,
    )


def check_authentication() -> None:
    authenticator = get_authenticator()
    authenticator.login("unrendered")

    """
    認証状態を確認し、認証されていない場合はメインページにリダイレクトする
    """

    if st.session_state.get("authentication_status") is False:
        st.error("認証に失敗しています。メインページからログインしてください。")
        st.stop()
    elif st.session_state.get("authentication_status") is None:
        st.error("認証されていません。メインページからログインしてください。")
        st.stop()
