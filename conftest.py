import pytest


def pytest_addoption(parser):
    parser.addoption('--slack', action='store_true',
                     help='Slack APIを使ったテストを実行する(要: Slackの設定')
    parser.addoption('--twitter', action='store', type=int,
                     help='Twitterのテストを実行する(要: Twitterの設定)。値は取得を開始する status_id。'
                     '最新の status_id だとテストがコケるので、3ツイートよりも前の status_id をセットする'
                     )


@pytest.fixture(scope='session')
def slack(request):
    enable_slack_api_test = request.config.getoption('--slack')
    if not enable_slack_api_test:
        pytest.skip()
    return enable_slack_api_test


@pytest.fixture(scope='session')
def twitter(request):
    status_id = request.config.getoption('--twitter')
    if not status_id:
        pytest.skip()
    return status_id
