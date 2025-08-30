# 動作環境
- OS: Windows 11
- Python: 3.9.13

# 構築手順
```sh
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
```

# 実行手順
## 起動したPCからのみアクセスする場合
```sh
source .venv/Scripts/activate
streamlit run main.py
```
http://localhost:8501にアクセスすると表示される。

## 同じネットワーク内の他の機器からもアクセスできるようにする場合
```sh
source .venv/Scripts/activate
streamlit run main.py --server.address 0.0.0.0
```
ファイアウォールは8501を受信できるようにしておく。

http://<ip_address>:8501にアクセスすると表示される。  
ip_addressは起動したPCのIPアドレス。