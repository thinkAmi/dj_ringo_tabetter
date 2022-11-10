#!/bin/sh
set -e

# コンテナ起動時に持っているSQLiteのデータベースファイルは、
# 後続処理でリストアに成功したら削除したいので、リネームしておく
if [ -f /app/ringo.db ]; then
  mv /app/ringo.db /app/ringo.db.bk
fi

# Cloud Storage からリストア
litestream restore -if-replica-exists -config /etc/litestream.yml /app/ringo.db

if [ -f /app/ringo.db ]; then
  # リストアに成功したら、リネームしていたファイルを削除
  echo "---- Restored from Cloud Storage ----"
  rm /app/ringo.db.bk
else
  # 初回起動時にはレプリカが未作成であり、リストアに失敗するので、
  # その場合には、冒頭でリネームしたdbファイルを元の名前に戻す
  echo "---- Failed to restore from Cloud Storage ----"
  mv /app/ringo.db.bk /app/ringo.db
fi

# マイグレーションを実行
python manage.py migrate --settings dj_ringo_tabetter.settings.production

# collect staticを実行
python manage.py collectstatic --noinput --settings dj_ringo_tabetter.settings.production

# レプリケーションしながらDjangoを起動
exec litestream replicate -exec "python manage.py runserver 0.0.0.0:8080 --settings dj_ringo_tabetter.settings.production" -config /etc/litestream.yml