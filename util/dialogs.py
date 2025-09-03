import streamlit as st


# confirm registration
@st.dialog("登録確認")
def confirm_registration(title, func, arg):
    st.write(f"{title}を登録しますか？")

    yes, no = st.columns(2)
    with yes:
        if st.button("はい"):
            func(arg)
            st.session_state.display_confirmation = False
            st.session_state.display_notification = True
            st.rerun()
    with no:
        if st.button("いいえ"):
            st.session_state.display_confirmation = False
            st.rerun()


# notify registration
@st.dialog("登録完了")
def notify_registration(title):
    st.write(f"{title}登録完了")
    st.session_state.display_notification = False
