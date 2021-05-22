from jdseckillAPI import JDSecKillAPI

if __name__ == '__main__':
    login_cookie = {
        'pin': '',
        'wskey': '',
        'whwswswws': '',
        'unionwsws': ''
    }
    JDska = JDSecKillAPI(login_cookie=login_cookie)
    print(JDska.reserve_maotai())


