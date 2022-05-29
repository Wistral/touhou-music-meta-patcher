## Touhou Music Meta Patcher

To solve the problem that flac files ripped from CD miss baisc meta info, come up with this small project.

### Install

```
python3 -m pip install -r requirements.txt
```

### Usage
You would better put track files by folders named with album name to simplify following instructions.

```python
from meta_process import auto_update_album_dir

album_dir = r'cd\東方華想神月'
auto_update_album_dir(album_dir)
```

If the folder name not agrees with the album, you can also overwrite it.

```python
album_dir = r'cd\simplefoldername'
auto_update_album_dir(album_dir, '東方華想神月')
```

### Effect

Before processing

![](https://cdn.staticaly.com/gh/Wistral/open-imgs/main/data/unseasoned.jpg)

After processing

![](https://cdn.staticaly.com/gh/Wistral/open-imgs/main/data/seasoned.jpg)
