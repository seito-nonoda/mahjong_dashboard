import streamlit as st


# confirm registration
@st.dialog("登録確認")
def confirm_registration(title, func, arg):
    st.write(f"{title}を登録しますか？")

    yes, no = st.columns(2)
    with yes:
        if st.button("はい"):
            func(arg)
            st.write(f"{title}登録完了")
    with no:
        if st.button("いいえ"):
            st.rerun()
