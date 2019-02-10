import os
import yaml
from dj_ringo_tabetter.settings import BASE_DIR


class Apple:
    def __init__(self):
        self.cultivars = self.load_cultivars()

    def load_cultivars(self) -> dict:
        """ プロジェクト直下にあるapples.yamlから品種名を取得する """
        with open(os.path.join(BASE_DIR, 'apples.yaml'), 'r', encoding='utf-8') as f:
            cultivars = yaml.load(f)
        return cultivars

    def get_color(self, cultivar: str) -> str:
        """ 品種名に紐づく色名を取得する """
        result = [x for x in self.cultivars if x['Name'] == cultivar]
        # 基本的に重複は無い前提
        return result[0]['Color']
