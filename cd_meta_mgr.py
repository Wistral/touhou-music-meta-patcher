from urllib.parse import quote
from requests import get
from bs4 import BeautifulSoup as BS
from pathlib import Path
from os import mkdir
from hashlib import md5
from pprint import pprint as pp

ua = 'touhou'
cache_dir = Path('.urlcache')


def str2hex(ss):
    if isinstance(ss, str):
        ss = ss.encode()
    return md5(ss).hexdigest()


def get_meta_raw_text(url):
    if not cache_dir.exists():
        mkdir(cache_dir)
    h = str2hex(url)
    cache_fn = cache_dir / f'{h}.html'
    if cache_fn.exists():
        print(f'Use cache {cache_fn}')
        with open(cache_fn, encoding='utf-8') as f:
            return f.read()
    else:
        req = get(url, headers={'User-Agent': ua})
        with open(cache_fn, 'w', encoding='utf-8') as f:
            print(req.text, file=f)
        return req.text


def get_meta_by_url(url, mode='thwiki'):
    bs = BS(get_meta_raw_text(url), 'lxml')

    def thwiki_proc(bs):
        return bs.html.body.find_all(attrs={'class': 'wikitable musicTable'})[0].tbody

    proc_dict = {
        'thwiki': thwiki_proc
    }
    meta_tbl = proc_dict[mode](bs)
    lines = list(meta_tbl)
    total_items = []
    item = {}
    for line in lines:
        objs = [o.text for o in line if not isinstance(o, str)]
        objs = [o for o in objs if o]
        if len(objs) == 3:
            item.update({
                'index': objs[0], 'title': objs[1], 'time': objs[2]
            })
        elif len(objs) == 2:
            try:
                item.update({objs[0]: objs[1]})
            except ValueError:
                print(f'Skip {objs}')
        elif len(objs) == 0:
            total_items.append(item)
            item = {}
    if item:
        total_items.append(item)

    pp(total_items)
    total_items.sort(key=lambda o: int(o['index']))
    return total_items


def get_meta_by_album(album_name):
    api = f'https://thwiki.cc/{quote(album_name)}'
    return get_meta_by_url(api)
