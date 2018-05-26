from common_util import call_funcs


# ====================================================
# 1101 http 요청 보내기
#      urllib.request.urlopen
#       - urlopen(url_w_encoded_querystring)
#       - urlopen(url, encoded_post_data)
#       - urlopen(request.Request) : can add custom header
#      requests
# ----------------------------------------------------
def test_1101():
    from urllib import request, parse

    # get request w/ urllib.request.urlopen
    get_url = 'http://httpbin.org/get'  # test server
    #  - prepare param data w/ dict
    get_params = {
        'name1': 'value1',
        'name1': 'value1',
    }

    #  - urlencode querystring w/ parse
    querystring = parse.urlencode(get_params)

    #  - space as '%02' instead of '+'
    #    - python bug로 알려져 있는듯?
    import urllib
    querystring = parse.urlencode(get_params,
                                  quote_via=urllib.parse.quote)

    #  - send get req w/ urlopen
    res = request.urlopen(get_url + '?' + querystring)
    resp = res.read()
    print(resp)

    # post request w/ urllib.request.urlopen
    post_url = 'http://httpbin.org/post'
    post_params = {
        'name1': 'value1',
        'name1': 'value1',
    }

    querystring = parse.urlencode(post_params)

    #  - send post req w/ urlopen : add post data w/ 2nd param
    res = request.urlopen(post_url, querystring.encode('ascii'))
    resp = res.read()
    print(resp)

    # add custom http headers in request
    #  - prepare header data w/ dict
    headers = {
        'User-agent': 'none/ofyourbusiness',
        'Spam': 'Eggs'
    }

    #  - use urllib.request.Request object to add headers
    req = request.Request(post_url,
                          querystring.encode('ascii'),
                          headers=headers)
    res = request.urlopen(req)
    resp = res.read()
    print(resp)

    # use requests package
    import requests

    #  - requests.post
    res = requests.post(post_url, data=post_params, headers=headers)
    text = res.text  # res is diff from urlopen's result
    print(text)


if __name__ == '__main__':
    call_funcs(vars(), lambda s: s.startswith('test_'))
