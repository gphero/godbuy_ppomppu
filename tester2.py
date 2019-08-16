from urllib.parse import urlparse, parse_qs, parse_qsl
url  = 'http://m.ppomppu.co.kr/new/bbs_view.php?id=ppomppu&amp;no=326567&amp;page=1'
parsed_url = urlparse(url)
parsed_qs = parse_qs(parsed_url.query)
print(parsed_qs['no'])
