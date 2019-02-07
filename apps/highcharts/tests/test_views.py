class TestTotal:
    """ total() のテスト"""

    def test_clientでアクセス(self, client):
        actual = client.get('/hc/total')
        assert actual.status_code == 200


class TestTotalByMonth:
    """ total_by_month() のテスト """

    def test_clientでアクセス(self, client):
        actual = client.get('/hc/total-by-month')
        assert actual.status_code == 200
