# 動作環境
- OS: Windows 11
- Python: 3.9.13

# 構築手順
## python周り
```sh
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
```
## データベース回り
本アプリはFirebaseのCloud Firestoreを利用している。
そのため、Cloud Firestoreのプロジェクトを構築する必要がある。
（自分でコレクションを作成する必要はない）


# 実行手順
## 起動したPCからのみアクセスする場合
### シークレット設定
#### .streamlit/secrets.toml
.streamlit/secrets.sample.tomlをコピーして、.streamlit/secrets.tomlを作成し、各項目を設定する。
passwordはハッシュ化したものを設定する。
##### ハッシュ化ツール
`python scripts/hash_password.py <password>`
#### firestoreのシークレット
secret/の下にCloud Firestoreから取得したシークレット(jsonファイル)を置く。
元から格納しているsecret-template.jsonは削除する。
### 起動コマンド
```sh
source .venv/Scripts/activate
streamlit run トップ.py
```
http://localhost:8501
にアクセスすると表示される。

## 同じネットワーク内の他の機器からもアクセスできるようにする場合
### シークレット設定
#### .streamlit/secrets.toml
.streamlit/secrets.sample.tomlをコピーして、.streamlit/secrets.tomlを作成し、各項目を設定する。
passwordはハッシュ化したものを設定する。
##### ハッシュ化ツール
`python scripts/hash_password.py <password>`
#### firestoreのシークレット
secret/の下にCloud Firestoreから取得したシークレット(jsonファイル)を置く。
元から格納しているsecret-template.jsonは削除する。
### 起動コマンド
```sh
source .venv/Scripts/activate
streamlit run トップ.py --server.address 0.0.0.0
```
ファイアウォールは8501を受信できるようにしておく。

http://<ip_address>:8501にアクセスすると表示される。  
<ip_address>は起動したPCのIPアドレス。

## streamlit上でデプロイする場合
### シークレット設定
アプリを作成後、シークレットの内容をアプリのSettingsに設定する。
### 起動コマンド
起動はstreamlit側で自動で行われる。
