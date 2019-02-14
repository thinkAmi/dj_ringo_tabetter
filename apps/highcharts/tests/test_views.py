import pytest
from django.urls import reverse


class TestViewForHighcharts:
    """ HighchartsのViewテスト """

    @pytest.mark.parametrize('url, expected_status_code', [
        (reverse('highcharts:total'), 200),
        (reverse('highcharts:total_by_month'), 200)
    ])
    def test_it(self, client, url, expected_status_code):
        # 単に parametrize を使いたかっただけ...
        actual = client.get(url)
        assert actual.status_code == expected_status_code
