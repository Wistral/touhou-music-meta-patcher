from pathlib import Path
from mutagen.flac import FLAC

from cd_meta_mgr import get_meta_by_album


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
        f.rename(des_fs[i])


def check_flac_meta(meta):
    '''TODO:'''
    pass


def modify_fn_meta_by_meta(fn, meta):
    song = FLAC(fn)
    check_flac_meta(meta)
    print(f'Add info {meta} for {fn}')
    song.update(meta)
    song.save()


def modify_fn_meta_by_album(album_dir, album_name):
    ad = Path(album_dir)
    assert ad.exists()
    m = get_meta_by_album(album_name)
    rename_by_meta(m, ad)
    songs = [f for f in ad.glob('*.flac')]
    songs.sort(key=lambda sf: sf.name)
    for i, meta in enumerate(m):
        artists = [meta.get(x) for x in ('编曲', '作曲', '演唱') if meta.get(x)]
        flac_meta = {
            'album': album_name, 'title': meta['title'], 'artist': artists
        }
        modify_fn_meta_by_meta(songs[i], flac_meta)
