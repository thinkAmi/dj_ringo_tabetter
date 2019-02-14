import os
from typing import List
from unittest.mock import Mock

import pytest


def _is_lack_of_environment_variables(environment_variable_names: List[str]) -> bool:
    """ 環境変数が不足しているかをチェック

    :param environment_variable_names: 対象の環境名変数リスト
    :return: 不足している場合、True
    """
    for name in environment_variable_names:
        if not os.environ.get(name):
            return True
    return False


class TestSlack:
    """ Slack APIを使ったテスト """
    def test_log(self, slack, capsys):
        from apps.tweets.management.commands.gather_tweets import Command

        if _is_lack_of_environment_variables(['SLACK_TOKEN', 'SLACK_CHANNEL']):
            pytest.skip('必要な環境変数が設定されていません')

        log_text = "test post"
        sut = Command()
        sut.log(log_text)  # この時点でSlackに「test post」と投稿される

        actual = capsys.readouterr()
        assert actual.out == f"{log_text}\n", "標準出力へは改行コード付で出力されること"


class TestTwitter:
    """ Twitter APIを使ったテスト """
    def test_gather_tweets(self, twitter):
        from apps.tweets.management.commands import gather_tweets

        if _is_lack_of_environment_variables(['USER_ID', 'TWITTER_CONSUMER_KEY', 'TWITTER_CONSUMER_SECRET']):
            pytest.skip('必要な環境変数が設定されていません')

        gather_tweets.TWEET_COUNT = 3  # テストで200件は多いので、差し替える

        sut = gather_tweets.Command()
        sut.last_search = Mock()
        sut.last_search.prev_since_id = twitter  # コマンドラインから与えた status_id で検索

        actual = sut.gather_tweets()
        assert len(actual) == 3

        assert actual[0].id > actual[1].id > actual[2].id, "idの降順に並んでいること"
