from pathlib import Path
from mutagen.flac import Picture
from mutagen import File

from cd_meta_mgr import get_meta_by_album, turn_to_flac_meta


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
    song = File(fn)
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
        modify_fn_meta_by_meta(songs[i], turn_to_flac_meta(meta, album_name))


def set_music_cover_data(music_fp, image_data):
    music_fp = Path(music_fp)
    assert Path(music_fp).exists()
    song = File(music_fp)
    if song.pictures:
        print(f'Maybe already has cover, skip')
        return
    im = Picture()
    im.type = 3
    im.meme = 'image/jpeg'
    im.desc = 'front cover'
    im.data = image_data
    song.add_picture(im)
    song.save()


def set_album_cover(album_dir, image_fp):
    image_fp = Path(image_fp)
    album_dir = Path(album_dir)
    assert image_fp.exists()
    assert album_dir.exists()
    with open(image_fp, 'rb') as f:
        data = f.read()
    for song in album_dir.glob('*.flac'):
        set_music_cover_data(song, data)
        print(f'Set {song}.cover={image_fp}')
