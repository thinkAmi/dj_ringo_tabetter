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
- Windows7 x64
- Python 3.4.3 x86
- PostgreSQL 9.4.4 x64
- IntelliJ IDEA 14.1.4

　
# 使用しているPythonパッケージと目的
- DjangoでJinja2テンプレートを使うため
 - Django 1.8.4
 - Jinja2 2.8
 - django-jinja 1.4.1
- りんご品種を書いたYAMLファイルを読み込むため
 - PyYAML 3.11
- Heroku Postgresのため
 - dj-database-url 0.3.0
 - psycopg2 2.6.1
- TwitterAPI用
 - tweepy 3.4.0
- ローカルでのTwitter API Keyの設定用
 - django-dotenv 1.3.0
   - Herokuでは環境変数へ設定
- Twitterのcreated_atにTimezoneを持たせるため
 - pytz 2015.4
- Herokuでの動作用
  - gunicorn 19.3.0
    - gunicornはWindowsでは動作しないので、Heroku上のみ
  - whitenoise 2.0.3

　
# セットアップ
1. git clone
2. `heroku create <your application name>`
3. `git push heroku master`
4. `heroku config:set USER_ID=<user_id> TWITTER_CONSUMER_KEY=<your_key> TWITTER_CONSUMER_SECRET=<your_secret>`
5. `heroku run python manage.py migrate`
6. Heroku Schedulerを追加、`python manage.py gather_tweets`と設定

　
# ライセンス
MIT

　
# ブログ記事
- [Python + Django + Highcharts + Herokuで食べたリンゴの割合をグラフ化してみた - メモ的な思考的な](http://thinkami.hatenablog.com/entry/2015/08/26/055717)


　
# 過去に作った似たようなもの
- Ruby版
 - [thinkAmi/ringo-tabetter · GitHub](https://github.com/thinkAmi/ringo-tabetter)
- C#版
 - [thinkAmi/RingoTabetter · GitHub](https://github.com/thinkAmi/RingoTabetter)
 - [thinkAmi/RingoTabetterApi · GitHub](https://github.com/thinkAmi/RingoTabetterApi)
