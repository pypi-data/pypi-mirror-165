from typing import List, Dict
from bs4.element import Tag
import requests
from bs4 import BeautifulSoup
from pixivery.error import HTTPException

class PixivRequest:
  ranking_url = "https://www.pixiv.net/ranking.php?mode={}&content=illust"
  artwork_url = "http://www.pixiv.net/member_illust.php?mode=medium&illust_id="

  def __init__(self):
    pass

  def requests(self, tag : List[str]) -> str:
    if tag[0] == 'rank':
      URL = self.ranking_url.format(tag[1])
    else:
      URL = self.artwork_url + tag[1]
      
    response = requests.get(URL)
    if(response.status_code == 200):
      data = response.text
      data = self.soup(data, tag)
      return data
    else:
      raise HTTPException(f"Error Code : {response.status_code}!")

  def soup(self, data, tag : List[str]) -> List[Dict[str, str]]:
    bs = BeautifulSoup(data, features="html5lib")
    if tag[0] == 'rank':
      article_content = bs.find("div", class_="ranking-items-container")
      if isinstance(article_content, Tag):
        data = []
        image_element_list = article_content.find_all("img")
        if tag[2] != None:
          for i in range(tag[2]):
            img = "https://i.pixiv.cat" + image_element_list[i]["data-src"][29:]
            id = image_element_list[i]["data-id"]
            link = "https://www.pixiv.net/artworks/" + id
            result = {'img' : img, 'id' : id, "link" : link}
            data.append(result)
        else:
          for image_element in image_element_list:
            img = "https://i.pixiv.cat" + image_element["data-src"][29:]
            id = image_element["data-id"]
            link = "https://www.pixiv.net/artworks/" + id
            result = {'img' : img, 'id' : id, "link" : link}
            data.append(result)
        return data
    else:
      article_content = bs.find("head")
      if isinstance(article_content, Tag):
        result = []
        img = article_content.find("link", rel = "preload")
        img = "https://i.pixiv.cat" + img['href'][19:]
        link = article_content.find("link", rel = "canonical")['href']
        id = link.split("/")[4]
        result = {'img' : img, 'link' : link, 'id': id} 
        return result

    

    
      