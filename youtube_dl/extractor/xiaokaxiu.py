# coding: utf-8
from __future__ import unicode_literals

from .common import InfoExtractor


class XiaokaxiuIE(InfoExtractor):
    _VALID_URL = r'https?://(www\.|)(m|v)\.xiaokaxiu\.com\/(m|v)\/(?P<id>.+)\.html?'

    _TEST = {
        'url': 'http://v.xiaokaxiu.com/v/kLqmiaTKy4Ze3C5udtrD5g__.html',
        'info_dict': {
            'id': 'kLqmiaTKy4Ze3C5udtrD5g__',
            'ext': 'mp4',
            'url': 'http://gslb.miaopai.com/stream/kLqmiaTKy4Ze3C5udtrD5g__.mp4',
            'title': '康康哥哥你爸要弯死了',
        },
        'params': {
            'skip_download': True,
        },
    }

    # Additional example videos from different sites
    # http://v.xiaokaxiu.com/v/kLqmiaTKy4Ze3C5udtrD5g__.html
    # http://m.xiaokaxiu.com/m/kLqmiaTKy4Ze3C5udtrD5g__.html
    def _real_extract(self, miaopai_url):
        identifier = self._match_id(miaopai_url)

        api_endpoint = 'http://api.xiaokaxiu.com/video/web/get_play_video?scid={0}'.format(
            identifier
        )

        content = self._download_json(api_endpoint, identifier, fatal=True)

        video_url = content['data']['linkurl']
        title = content['data']['title']

        return {
            'id': identifier,
            'url': video_url,
            'title': title,
        }



