import streamlit_authenticator as stauth

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Hash a credential")
    parser.add_argument("password", type=str, help="The password to hash")
    args = parser.parse_args()

    print(stauth.Hasher.hash(args.password))
