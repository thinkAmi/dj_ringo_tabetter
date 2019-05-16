# dj_ringo_tabetter


以下の機能を持った、Djangoアプリです。

- Twitterの指定したユーザに対して、`[リンゴ]`で始まるツイートに含まれるリンゴ名を集計し、データベースへと保存
- データベースに保存されいてる集計情報をJSONの形で返すAPI
- JSON APIの結果をHighchartsでグラフ表示

　  
ツイートは、先頭に`[リンゴ]`があり、品種名を `` ` ``(バッククォート)で囲んであるものが対象となります。以下がその例です。

```
[リンゴ]今日は `シナノゴールド` を食べた。シャリシャリしていておいしかった。
```

　  
また、Herokuへデプロイしてあります。  
[りんごたべたー](http://ringo-tabetter.herokuapp.com/hc/total)

　
# 開発環境
- Mac
- Python 3.7.2
  - Django 2.2.1
- PostgreSQL 10.6

また、パッケージの一括アップデートは、 `pip-review` を使用しています。GitHubのセキュリティアラートへの対応のためです。  
https://github.com/jgonggrijp/pip-review

```
# アップデートがあるかを確認
$ pip-review

# 自動で更新
$ pip-review --auto
```


　  
# セットアップ
1. git clone
2. `heroku create <your application name>`
3. `git push heroku master`
4. `heroku config:set USER_ID=<your twitter id> TWITTER_CONSUMER_KEY=<your consumer key> TWITTER_CONSUMER_SECRET=<your consumer secret>`
5. `heroku config:set SLACK_TOKEN=<your slack token> SLACK_CHANNEL=<your slack channel, example: ringo-tabetter>`
6. `heroku run python manage.py migrate`
7. Heroku Schedulerを追加、`python manage.py gather_tweets`と設定

　  

# 開発環境DBのセットアップ(Docker使用)

```
# デフォルトのポート 5432はすでに使われているので、別のポート(19876)をDocker上の 5432 につなげる
$ docker run --name ringo_pg -p 19876:5432 -e POSTGRES_USER=ringo -e POSTGRES_PASSWORD=postgres -d postgres:10.6

# コンテナ起動
docker start ringo_pg

# データベースを作成
psql -U ringo -W -p 19876 -h localhost -c "CREATE DATABASE ringo_tabetter_py;"
```

　  

# テスト

```
$ python -m pytest
```

　  
# ライセンス
MIT

　  
# ブログ記事
- [Python + Django + Highcharts + Herokuで食べたリンゴの割合をグラフ化してみた - メモ的な思考的な](http://thinkami.hatenablog.com/entry/2015/08/26/055717)
- [Python3.4 & Django1.8な個人アプリを、Python3.7 & Django 2.1 へとアップデートした - メモ的な思考的な](https://thinkami.hatenablog.com/entry/2019/02/15/003051)

　
# 過去に作った似たようなもの
- Ruby版
 - [thinkAmi/ringo-tabetter · GitHub](https://github.com/thinkAmi/ringo-tabetter)
- C#版
 - [thinkAmi/RingoTabetter · GitHub](https://github.com/thinkAmi/RingoTabetter)
 - [thinkAmi/RingoTabetterApi · GitHub](https://github.com/thinkAmi/RingoTabetterApi)
