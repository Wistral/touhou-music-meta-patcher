from pathlib import Path
from os import rename


def check_album_fn_formated(album_dir):
    album_dir = Path(album_dir)
    origin = list(album_dir.glob('*.flac'))
    test_r = [f for f in origin
              if 'track' in f.name.lower()
              ]
    return len(test_r) != len(origin)


def rename_by_meta(meta, album_dir, album_fns=None):
    if check_album_fn_formated(album_dir):
        print(f'Maybe filenames in {album_dir} already formated, skip')
        return
    # TODO: rename filename format config
    des_fns = [
        f'{m["index"]}_{m["title"]}'
        for m in meta
    ]
    des_fns.sort()
    des_dir = Path(album_dir)
    if album_fns:
        origin_fs = [des_dir/fn for fn in album_fns]
    else:
        origin_fs = list(des_dir.glob('*.flac'))
    assert len(des_fns) == len(origin_fs)
    origin_fs.sort(key=lambda f: f.name)
    des_fs = [f.parent / (des_fns[i]+f.suffix)
              for i, f in enumerate(origin_fs)]

    for i, f in enumerate(origin_fs):
        print(f'{f.name} => {des_fs[i].name}')
        rename(f, des_fs[i])
