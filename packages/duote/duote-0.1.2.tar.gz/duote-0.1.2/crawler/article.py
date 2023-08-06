import requests
import json
from lxml import etree
from urllib.parse import unquote
import re




def get_ttwid():
    """头条cookie必须ttwid

    Returns:
        返回一个str cookie ， 作为headers['cookie']的值 
    """
    payload = {"aid": 24, "service": "www.toutiao.com", "region": "cn",
               "union": True, "needFid": False, "fid": "", "migrate_priority": 0}
    post_url = 'https://ttwid.bytedance.com/ttwid/union/register/'
    req = requests.post(post_url, data=json.dumps(payload))
    cookie = req.headers['set-cookie'].split(';')[0] 
    return cookie

def toutiao_header():
    toutiao_header = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'cookie': get_ttwid(),
        'dnt': '1',
        'pragma': 'no-cache',
        'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-site',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
    }
    return toutiao_header


def get_redirect_url(url):
    re_url = requests.get(url, headers=toutiao_header(
    ), allow_redirects=False).headers['location']
    if 'article' not in re_url:
        re_url = get_redirect_url(re_url)
    return re_url


def get_articles_url(keyword, exclude=None):
    """获取今日头条资讯频道关键词搜索结果

    Args:
        keyword (str): 需要搜索的关键词
        exclude (str): 排除的url,不带参数跳转后的最终url

    Returns:
        list: 返回List[List[url,title]]    
    """
    
    TTURL = F'https://so.toutiao.com/search?keyword={keyword}&pd=information&dvpf=pc'   
    req = requests.get(TTURL % keyword, headers=toutiao_header(), timeout=10)
    req.encoding = 'utf-8'
    dom = etree.HTML(req.text)
    result = []
    for r in range(10):
        title = dom.xpath('//div[@data-i="%s"]//a[contains(@class,"text-ellipsis")]//text()' % r)
        title = ''.join(title)
        article_url = get_toutiao_serp_url(dom.xpath('//div[@data-i="%s"]//a/@href' % r))
        redirect_url = get_redirect_url(article_url)
        if redirect_url != exclude:
            result.append([redirect_url, title])
    return result


def get_article_content(url,intro_lenth=100):
    """获取文章详情

    Args:
        url (_str_): 文章url
        intro_lenth (int, optional): _摘要长度,提取文章前100个字_. Defaults to 100.

    Raises:
        BaseException: _各种错误_
    Returns:
        _dict_: {'url':__str__,
                 'text':__list__,
                 'intro':__str__,
                 'title':__str__}
    """
    response = requests.get(url, headers=toutiao_header())
    if response.status_code != 200:
        raise BaseException(f'文章状态码错误,状态码为：{response.status_code}')
    if 'toutiao.com' not in response.url:
        raise BaseException(f'文章url错误，url为：{response.url}')
    dom = etree.HTML(response.text)
    title = dom.xpath('//h1/text()')[0]
    if '404' in title:
        raise BaseException(f'文章404,url为：{response.url}')
    contents_tag = dom.xpath(
        '//article[contains(@class,"syl-article-base")]/child::*')
    if len(contents_tag) == 1:
        contents_tag = dom.xpath(
            '//*[contains(@class,"syl-article-base")]/div/child::*')
    r = []
    for html_tag in contents_tag:
        if len(html_tag.xpath('.//text()')) == 0 and len(html_tag.xpath('.//@src')) == 0:
            continue
        r.append(''.join(html_tag.xpath('.//text()'))
                      if len(html_tag.xpath('.//@src')) == 0 else html_tag.xpath('.//@src')[0])
    intro_text = ''.join(contents_tag.xpath('.//text()'))
    result_dict = dict(text=r)
    result_dict['url'] = url
    result_dict['title'] = title
    result_dict['intro'] = intro_text[:intro_lenth]
    return result_dict



def get_toutiao_serp_url(xpath):
    # 拉取头条搜索结果页的跳转真实URL\
    urls = list(set(xpath))
    for url in urls:
        if 'jump' in url:
            enurl = unquote(url)
            return re.findall(r'=(.+?)\?', enurl)[0]
    raise BaseException('未能获得文章URL')


