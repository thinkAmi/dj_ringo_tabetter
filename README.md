# dj_ringo_tabetter


以下の機能を持った、Djangoアプリです。

- Twitterの指定したユーザに対して、`[リンゴ]`で始まるツイートに含まれるリンゴ名を集計し、データベースへと保存
- データベースに保存されいてる集計情報をJSONの形で返すAPI
- JSON APIの結果をHighchartsでグラフ表示

　  
ツイートは、先頭に`[リンゴ]`があり、品種名を `` ` ``(バッククォート)で囲んであるものが対象となります。以下がその例です。

```
[リンゴ]今日は `シナノゴールド` を食べた。シャリシャリしていておいしかった。
```

　  
また、Google Cloud の Cloud Run (+ カスタムドメイン) へデプロイしてあります。  
[りんごたべたー](https://ringo-tabetter.thinkami.dev/hc/total)

　
# 開発環境
- WSL2 Ubuntu 22.04.1 LTS
- Python 3.10.7
  - Django 4.4.1
- SQLite

また、パッケージの一括アップデートは、 `pip-review` を使用しています。GitHubのセキュリティアラートへの対応のためです。  
https://github.com/jgonggrijp/pip-review

```
# アップデートがあるかを確認
$ pip-review

# 自動で更新
$ pip-review --auto
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
- [WSL2 + Ubuntu 22.04.1 LTS上のDjangoアプリを、JetBrains Gateway + PyCharmにて開発し、Herokuにpushできるようにしてみた - メモ的な思考的な](https://thinkami.hatenablog.com/entry/2022/09/11/220335)
- [Python3.7 & Django 2.1 な個人アプリを Python 3.10 & Django 4.1 へとアップデートした - メモ的な思考的な](https://thinkami.hatenablog.com/entry/2022/09/14/215942)
- [WSL2 + Ubuntu 22.04.1 な環境上のDockerへ、既存のDjangoアプリを載せてみた - メモ的な思考的な](https://thinkami.hatenablog.com/entry/2022/09/19/205521)
- [Tweepyをアップデートしたタイミングで、使用するTwitter APIを v1.1 から v2 に切り替えてみた - メモ的な思考的な](https://thinkami.hatenablog.com/entry/2022/09/24/121753)
- [Djangoアプリを、Coogle Cloud の Cloud Run + Cloud Storage + Litestream な環境で動かしてみた - メモ的な思考的な](https://thinkami.hatenablog.com/entry/2022/09/25/224406)
- [Python + Django + Highcharts + Coogle Cloud Cloud Run + Cloud Storage + Litestream で食べたリンゴの割合をグラフ化してみた - メモ的な思考的な](https://thinkami.hatenablog.com/entry/2022/11/10/231010)

　
# 過去に作った似たようなもの

- Ruby版
   - [thinkAmi/ringo-tabetter · GitHub](https://github.com/thinkAmi/ringo-tabetter)
- C#版
   - [thinkAmi/RingoTabetter · GitHub](https://github.com/thinkAmi/RingoTabetter)
   - [thinkAmi/RingoTabetterApi · GitHub](https://github.com/thinkAmi/RingoTabetterApi)
