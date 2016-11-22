# coding: utf-8
from __future__ import unicode_literals

import json

from youtube_dl.utils import ExtractorError
from .common import InfoExtractor


class QQVideoIE(InfoExtractor):
    _VALID_URL = r'https?://(www\.|)(kuaibao|v)\.qq\.com'

    _TEST = {
        'url': 'http://v.qq.com/page/e/g/3/e0179tn8eg3.html',
        'info_dict': {
            'id': 'e0179tn8eg3',
            'ext': 'mp4',
            'title': 'qqvideo',
        },
        'params': {
            'skip_download': True,
        },
    }

    def _video_info(self, identifier):
        api = 'http://h5vv.video.qq.com/getinfo?otype=json&platform=10901&vid={0}'.format(
            identifier
        )
        content = self._download_webpage(api, identifier)

        data = self._search_regex(
            r'QZOutputJson=(?P<json>.*)',
            content,
            'json_data',
            group='json',
            fatal=True
        )

        json_data = json.loads(data[:-1])

        if 'vl' not in json_data:
            raise ExtractorError('Unable to extract qqvideo, {0}'.format(
                json_data['msg'])
            )

        url = json_data['vl']['vi'][0]['ul']['ui'][0]['url']
        fvkey = json_data['vl']['vi'][0]['fvkey']
        mp4 = json_data['vl']['vi'][0]['cl'].get('ci', None)

        if mp4:
            mp4 = mp4[0]['keyid'].replace('.10', '.p') + '.mp4'
        else:
            mp4 = json_data['vl']['vi'][0]['fn']

        url = '{0}/{1}?vkey={2}'.format(url, mp4, fvkey)

        return url, mp4

    # Support url's
    # http://v.qq.com/iframe/player.html?vid=h01596s8r6k&tiny=0
    # http://v.qq.com/cover/t/tw2rs9d4mpzkicy.html?vid=0198z5z7ad
    # http://v.qq.com/page/e/g/3/e0179tn8eg3.html
    def _real_extract(self, qq_url):
        identifier = None
        title = 'qqvideo'

        if 'v.qq.com/page' in qq_url:
            identifier = self._search_regex(
                r'\b(\w+).html',
                qq_url,
                'Page identifier',
                fatal=True
            )
        elif 'kuaibao.qq.com' in qq_url:
            content = self._download_webpage(
                qq_url,
                'Download kuaibao page',
                fatal=True,
            )
            identifier = self._search_regex(
                r'vid\s*=\s*"\s*([^"]+)"',
                content,
                'Search page id',
                fatal=True,
            )
            raw_title = self._search_regex(
                r'title">([^"]+)</p>',
                content,
                'Search title'
            )
            title = raw_title.strip() if raw_title else title
        elif 'iframe/player.html' in qq_url:
            identifier = self._search_regex(
                r'\bvid=(\w+)',
                qq_url,
                'Page identifier',
                fatal=True
            )
        else:
            content = self._download_webpage(
                qq_url,
                identifier,
                fatal=True,
                note='Download page by url'
            )
            identifier = self._search_regex(
                r'vid\s*:\s*"\s*([^"]+)"',
                content,
                'Page identifier',
                fatal=True
            )
            # print identifier
        video_url, ext = self._video_info(identifier)

        return {
            'id': identifier,
            'url': video_url,
            'title': title
        }
