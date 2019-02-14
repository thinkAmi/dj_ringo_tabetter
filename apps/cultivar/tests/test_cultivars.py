import pytest


class TestApple:
    """ Appleクラスのテスト """

    def test_get_color_品種が存在する場合(self):
        from apps.cultivar.apple import Apple

        sut = Apple()
        sut.cultivars = [
            {'Name': 'シナノゴールド', 'Color': 'Gold'},
            {'Name': 'シナノドルチェ', 'Color': 'Red'},
            {'Name': '王林', 'Color': 'Yellow'},
        ]

        actual = sut.get_color('シナノゴールド')
        assert actual == 'Gold'

    def test_get_color_品種が存在しない場合(self):
        from apps.cultivar.apple import Apple

        sut = Apple()
        sut.cultivars = [
            {'Name': 'シナノゴールド', 'Color': 'Gold'},
            {'Name': 'シナノドルチェ', 'Color': 'Red'},
            {'Name': '王林', 'Color': 'Yellow'},
        ]

        with pytest.raises(IndexError):
            sut.get_color('フジ')
