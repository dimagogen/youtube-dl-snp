# coding: utf-8
from __future__ import unicode_literals

import urlparse

from ..utils import (
    ExtractorError,
    sanitized_Request,
    compat_urllib_request,
)

from .common import InfoExtractor


class WeiboBaseInfoExtractor(InfoExtractor):
    @staticmethod
    def _build_mobile_request(url):
        request = sanitized_Request(url)

        request.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        request.add_header('Accept-Charset', 'UTF-8,*;q=0.5')
        request.add_header('Accept-Encoding', 'gzip,deflate,sdch')
        request.add_header('Accept-Language', 'en-US,en;q=0.8')
        request.add_header('User-Agent',
                           'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36')

        return request

    def _download_mobile_webpage(self, url, *args, **kwargs):
        request = self._build_mobile_request(url)

        return self._download_webpage(request, *args, **kwargs)

    def _download_page(self, url, name):
        self.report_download_webpage(name)
        try:
            request = compat_urllib_request.Request(url)
            response = compat_urllib_request.urlopen(request)

            data = response.read()
            data = data.decode('utf-8')

            return data
        except Exception:
            return None

    @staticmethod
    def _parse_url_from_weibo_passport(passport_url):
        parts = urlparse.urlsplit(passport_url)
        query_info = urlparse.parse_qs(
            qs=parts.query,
            keep_blank_values=True
        )
        try:
            return query_info['url'][0]
        except (Exception, KeyError):
            return None


class WeiboIE(WeiboBaseInfoExtractor):
    _VALID_URL = r'https?://(www\.|)(?P<type>(video\.|passport\.|))weibo\.com/(show\?fid=(?P<show>\d{4}:\w{32})\w*|p/230444(?P<id>\w+)|visitor)'

    _TESTS = [{
        'url': 'http://video.weibo.com/show?fid=1034:4fb153c58d835edacee289ebcecd1230',
        'info_dict': {
            'id': '1034:4fb153c58d835edacee289ebcecd1230',
            'title': 'weibo',
            'url': 're:^http://us.sinaimg.cn/002P26pijx06QWAy4VNt01040100rXqT0k01.mp4',
            'description': '那么问题来了，这么好的东西在哪里可以买到呢？[doge]',
            'ext': 'mp4',
        },
        'params': {
            'skip_download': True,
        },
    },
        {
            'url': 'http://weibo.com/p/2304441bb617415f2b107356e13b60df83fbb5',
            'info_dict': {
                'id': '1bb617415f2b107356e13b60df83fbb5',
                'url': 're:^http://us.sinaimg.cn/004Dr2Rfjx070XbnbRT205040100CZW10k01.mp4',
                'description': '#曼联足球俱乐部# 2015/16赛季最佳U21球员，现已接受投票！ 点击投票 http://www.manutd.com/en/poty 候选名单 http://www.manunited.com.cn/zh-CN/NewsAndFeatures/FootballNews/2016/Apr/VOTE-FOR-MANCHESTER-UNITEDS-201516-AWARDS.aspx',
                'ext': 'mp4',
                'title': 'weibo',
            },
            'params': {
                'skip_download': True,
            },
        },
    ]

    # Additional example videos from different sites
    # http://video.weibo.com/show?fid=1034:4fb153c58d835edacee289ebcecd1230
    # http://www.weibo.com/p/2304444fb153c58d835edacee289ebcecd1230
    # http://t.cn/Rqa5U43
    def _real_extract(self, weibo_url):
        url = weibo_url

        is_passport = self._search_regex(
            pattern=self._VALID_URL,
            string=weibo_url,
            name='Type',
            group='type'
        )
        is_passport = is_passport[:-1] == 'passport'

        if is_passport:
            url = self._parse_url_from_weibo_passport(weibo_url)

            if url is None:
                raise ExtractorError('Unable to extract weibo url from passport')

        identifier = self._match_id(url)

        if identifier:
            url = 'http://video.weibo.com/show?fid=1034:{0}'.format(identifier)
        else:
            identifier = self._search_regex(self._VALID_URL, url, 'identifier', group='show', fatal=True)

        url += '&type=mp4'

        mobile_page = self._download_mobile_webpage(url, identifier)

        video_url = self._html_search_regex(r'<video src="(.*?)\"\W', mobile_page, 'video_url', fatal=True)

        page = self._download_page(url, 'Title')

        title = self._html_search_meta('description', page, 'title', fatal=False)

        return {
            'id': identifier,
            'title': 'weibo',
            'url': video_url,
            'description': title
        }
