import os
import yaml
from django.conf import settings


class Apple:
    def __init__(self):
        self.cultivars = self.load_cultivars()

    def load_cultivars(self) -> dict:
        """ プロジェクト直下にあるapples.yamlから品種名を取得する """
        with open(os.path.join(settings.BASE_DIR, 'apples.yaml'), 'r', encoding='utf-8') as f:
            cultivars = yaml.safe_load(f)
        return cultivars

    def get_color(self, cultivar: str) -> str:
        """ 品種名に紐づく色名を取得する """
        result = [x for x in self.cultivars if x['Name'] == cultivar]
        # 基本的に重複は無い前提
        return result[0]['Color']
