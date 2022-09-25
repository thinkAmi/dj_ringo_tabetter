FROM python:3.10.7-slim

# Djangoアプリの8080番ポートを公開するおしらせ
EXPOSE 8080

# 必要なライブラリをインストール
# 実行時に `debconf: delaying package configuration, since apt-utils is not installed` が出るが、無視してよさそう
RUN apt-get update \
    && apt-get install -y --no-install-recommends sqlite3 \
    && apt-get -y clean \
    && rm -rf /var/lib/apt/lists/*

# Download the static build of Litestream directly into the path & make it executable.
# This is done in the builder and copied as the chmod doubles the size.
# ref: https://github.com/steren/litestream-cloud-run-example/blob/main/Dockerfile
ADD https://github.com/benbjohnson/litestream/releases/download/v0.3.9/litestream-v0.3.9-linux-amd64-static.tar.gz /tmp/litestream.tar.gz
RUN tar -C /usr/local/bin -xzf /tmp/litestream.tar.gz

# working directoryの設定
WORKDIR /app

# リポジトリのファイルをコピー
COPY . /app

# パッケージインストール
RUN pip install --no-cache-dir -r requirements.txt

# Copy Litestream configuration file & startup script.
COPY ./litestream.yml /etc/litestream.yml
COPY ./run.sh /app/run.sh

#CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]
CMD ["/bin/bash", "/app/run.sh"]
