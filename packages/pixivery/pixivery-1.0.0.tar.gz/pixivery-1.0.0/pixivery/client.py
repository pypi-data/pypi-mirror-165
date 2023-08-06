from pixivery.http import PixivRequest
from typing import Dict
from pixivery.utils import ranking_tag
from pixivery.error import RankingModeException

class Pixiv(PixivRequest):
  def __init__(self):
    pass

  def get_artwork(self, id : str) -> Dict[str, str]:
    """작품의 아이디를 통해 정보를 가져옵니다."""
    tag = ['artwork' , id]
    result = self.requests(tag)
    return result

  def get_ranking(self, mode : str = 'daily', limit : int = None) -> Dict[str, str]:
    """1위~50위 작품의 정보를 가져옵니다<br>`mode` : daily, weekly, monthly, rookie"""
    if mode not in ranking_tag:
      raise RankingModeException(f"{mode}는 올바른 모드가 아닙니다.")
    tag = ['rank', mode, limit]
    result = self.requests(tag)
    return result

