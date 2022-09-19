FROM python:3.10.7-slim

# Djangoアプリの8000番ポートを公開するおしらせ
EXPOSE 8000

# 必要なライブラリをインストール
# 実行時に `debconf: delaying package configuration, since apt-utils is not installed` が出るが、無視してよさそう
RUN apt-get update \
    && apt-get install -y --no-install-recommends sqlite3 \
    && apt-get -y clean \
    && rm -rf /var/lib/apt/lists/*

# working directoryの設定
WORKDIR /app

# リポジトリのファイルをコピー
COPY . /app

# パッケージインストール
RUN pip install --no-cache-dir -r requirements.txt

# 起動
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
