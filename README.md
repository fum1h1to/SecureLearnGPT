# SecureLearnGPT
ChatGPTを用いた情報セキュリティトレーニングツール

# 開発環境の準備
下記のコマンドを順番に実行

1. Pythonの仮想環境の構築
    ```
    python -m venv venv
    ```

2. 仮想環境の有効化
    開発環境がLinux, Macの場合
    ```
    source venv/bin/activate
    ```

    開発環境がWindowsの場合
    ```
    .\venv\Scripts\activate
    ```

    ※WindowsでGit Bashを使用している場合
    ```
    source venv/Scripts/activate
    ```

3. モジュールのインストール
    ```
    pip install -r requirements.txt
    ```

4. アプリの軌道
    ```
    python server.py
    ```