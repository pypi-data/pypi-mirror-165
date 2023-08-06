# Pixivery
[Github](https://github.com/VoidAsMad/Pixivery)
## Install
```py
$ pip install pixivery
```

## Example
```py
from pixivery import client

client = client.Pixiv()
print(client.get_ranking()) #limit = 1~50
print(client.get_artwork('100807849'))
```

이슈는 언제든지 환영입니다!