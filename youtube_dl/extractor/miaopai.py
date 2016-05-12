# coding: utf-8
from __future__ import unicode_literals

from .common import InfoExtractor


class MiaopaiIE(InfoExtractor):
    _VALID_URL = r'https?://(www\.|)(m\.|)miaopai\.com/show/(channel\/|)(?P<id>.+)\.html?'

    _TEST = {
        'url': 'http://www.miaopai.com/show/wplYaViUNyWukb1dScu7Sg__.htm',
        'info_dict': {
            'id': 'wplYaViUNyWukb1dScu7Sg__',
            'ext': 'mp4',
            'url': 're:^http://gslb.miaopai.com/stream/wplYaViUNyWukb1dScu7Sg__.mp4',
            'title': '库里和联盟其他11位三分射手对比，简直是坐直升机',
        },
        'params': {
            'skip_download': True,
        },
    }

    # Additional example videos from different sites
    # http://www.miaopai.com/show/wplYaViUNyWukb1dScu7Sg__.htm
    # http://m.miaopai.com/show/channel/DUq3rIh8nO8OnutQf5d-pw__
    # http://miaopai.com/show/channel/DUq3rIh8nO8OnutQf5d-pw__
    def _real_extract(self, miaopai_url):
        identifier = self._match_id(miaopai_url)

        api_endpoint = 'http://api.miaopai.com/m/v2_channel.json?fillType=259&scid={0}&vend=miaopai'.format(
            identifier
        )
        content = self._download_json(api_endpoint, identifier, fatal=True)

        ext = content['result']['stream']['and']
        title = content['result']['ext']['t']
        full_video_url = content['result']['stream']['base']
        short_video_url = self._search_regex(r'(.+)\?vend', full_video_url, 'Video url', fatal=True)

        return {
            'id': identifier,
            'url': short_video_url,
            'title': title,
            'ext': ext,
        }
