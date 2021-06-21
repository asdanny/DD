import requests
# import json
# import re
# import datetime
import time
from urllib import parse
# import base64
# import urllib
# import json
# import jd_frida as gs
# import copy


def getUrlParams(url):
    res = dict(parse.parse_qsl(url))
    return res


def get_cookie_string(cookie):
    cookie_string = ''
    for cookie_key in cookie.keys():
        cookie_string += '%s=%s;' % (cookie_key, cookie[cookie_key])
    return cookie_string


def get_jd_time():
    response = requests.get(url='https://api.m.jd.com/client.action?functionId=queryMaterialProducts&client=wh5')
    print(response.json())


def get_sk(data):
    data_val = [val for val in data['data'].values()]
    n, o, p, q, r, s = data_val[0], data_val[1], data_val[2], data_val[3], data_val[4], data_val[5]
    sk_val = ''
    if n == 'cca':
        sk_val = p[14:19].lower() + o[5:15].upper()
    if n == 'ab':  # check ok
        sk_val = r[10:18] + s[2:13].lower()
    if n == 'ch':
        sk_val = q.upper() + r[6:10].upper()
    if n == 'cbc':  # check ok
        sk_val = q[3:13].upper() + p[10:19].lower()
    if n == 'by':
        sk_val = o[5:8] + p.replace('a', 'c')
    if n == 'xa':
        sk_val = o[1:16] + s[4:10]
    if n == 'cza':
        sk_val = q[6:19].lower() + s[5:11]
    if n == 'cb':
        sk_val = s[5:14] + p[2:13].upper()

    return sk_val


class JDSecKillAPI:
    def __init__(self, login_cookie):
        self.skuId = '100012043978'
        self.s = requests.session()
        self.token_cookie = login_cookie
        self.token_cookie_string = get_cookie_string(cookie=self.token_cookie)

        self.function_id = 'genToken'
        self.uuid = '863064425269521-080027d76df4'
        self.body_string = '{"action":"to","to":"https%3A%2F%2Fdivide.jd.com%2Fuser_routing%3FskuId%3D100012043978"}'
        # # sk 参数初始化
        # with open("js_sk.js", "r", encoding='utf-8') as f:
        #     sk_fun = f.read()  # 读取js文件
        # self.sk = execjs.compile(sk_fun)  # 编译执行js代码

    def reserve_maotai(self):
        headers = {
            'user-agent': 'okhttp/3.12.',
            'content-type': 'application/x-www-form-urlencoded',
            'content-length': '3081',
            'cookie': self.token_cookie_string,
            'jdc-backup': self.token_cookie_string,
        }
        # eid = json.loads(self.token_cookie['unionwsws'])['devicefinger']
        eid = 'eidAcbd281217fsds90FMZ8DR9eXgoKSWRX3cLPdBqob2acW0R3rdAZI6jkW3OdlaugCNVppndb4UddGOyrt0Z1mN4AkQ/9CUAQFAp PnQY5raGSEnBC'
        query_params = {
            'functionId': 'appoint',
            'clientVersion': '9.2.0',
            'build': '85134',
            'client': 'android',
            'd_brand': 'HUAWEI',
            'd_model': 'LIO-AN00',
            'osVersion': '7.1.2',
            'screen': '1920*1080',
            'partner': 'hhqj02',
            'aid': '38af3fc36a99f737',
            'eid': eid,
            'sdkVersion': '25',
            'lang': 'zh_CN',
            'uuid': self.uuid,
            'area': '15_1213_3411_59341',
            'networkType': 'wifi',
            'wifiBssid': '43236c80b42dbe2ba38bd9ab1ae41eb7',
            'uts': '0f31TVRjBSvXOX4GIirb18C/XUfI66MM7yRSmIn6iXRphvR7wIhkSl7YMtpNaPzt+AYHOdGb2+I3UNtaI1xHToNhPc0EEF8B/68MhL+Ynl+b9/xVRwF7gjIw+uJLfPlEr/9SA6zPpqJBM6dY6Z5pp0IT20GgFG9vclum5JIoEj7o8iBYEDrfxR5+UPXaK81HLgF1rRgSYOkOL6fI8fdsSA==',
        }

        reserve_url = 'https://api.m.jd.com/client.action?' + parse.urlencode(query_params) + '&'
        body_string = '{"autoAddCart":"0","bsid":"","check":"0","ctext":"","isShowCode":"0","mad":"0","skuId":"100012043978","type":"1"}'

        data = {'body': body_string}
        sign = 'st=1624249321832&sign=626a3fc2565b2e8636605f8b10d04894&sv=120'
        response = self.s.post(url=reserve_url + sign, data=data, headers=headers, timeout=1)
        return response.json()

    # def get_token_key(self):
    #     headers = {
    #         'user-agent': 'okhttp/3.12.',
    #         'content-type': 'application/x-www-form-urlencoded',
    #         'content-length': '3081',
    #         'cookie': self.token_cookie_string,
    #         'jdc-backup': self.token_cookie_string,
    #     }
    #     eid = 'eidA115c812269sbwhdP0BiVTnWYIKVNymrSBMIXUUi5txupHPRalrjqhmB/P3C0Hg3eO0405ppb4QzevFJmNvw/PFslM/68LPvtaaTT/MCFQOsNUQhL'
    #     query_params = {
    #         'functionId': self.function_id,
    #         'clientVersion': '9.2.0',
    #         'build': '85134',
    #         'client': 'android',
    #         'd_brand': 'HUAWEI',
    #         'd_model': 'LIO-AN00',
    #         'osVersion': '7.1.2',
    #         'screen': '1920*1080',
    #         'partner': 'hhqj02',
    #         'aid': '38af3fc36a99f737',
    #         'eid': eid,
    #         'sdkVersion': '25',
    #         'lang': 'zh_CN',
    #         'uuid': self.uuid,
    #         'area': '2_2830_51811_0',
    #         'networkType': 'wifi',
    #         'wifiBssid': '43236c80b42dbe2ba38bd9ab1ae41eb7',
    #         'uts': '0f31TVRjBSsqndu4/jgUPz6uymy50MQJhQy4jAtAlh+n8GJiXoWP/9c8wP/+u4Xkbsf8iPUHrJ+nz8nXt+aGZXiPhZV6YXoLgZtI5OBNQe5SJGxU/1t661/3OQSsQaU0dG+4NuQHNRoIZo4dG3JxhCAuLrGelkGqZ7vmHNN/jFolcDLqtEBSFY7Fou5xPR7en5iaWp6tQJpCvsAaneoaYw=='
    #     }
    #     token_key_url = 'https://api.m.jd.com/client.action?' + parse.urlencode(query_params) + '&'
    #
    #     data = {'body': self.body_string}
    #     sign = gs.get_sign(self.function_id, self.body_string, self.uuid)
    #     response = self.s.post(url=token_key_url + sign, data=data, headers=headers, timeout=1)
    #     # token_key = response.json()['tokenKey']
    #     # print('Token Key: ----------> %s' % response.json())
    #     # print(response.status_code)
    #     return response.json()

    def get_token_key_by_fix_sign(self):
        headers = {
            'user-agent': 'okhttp/3.12.',
            'content-type': 'application/x-www-form-urlencoded',
            'content-length': '3081',
            'cookie': self.token_cookie_string,
            'jdc-backup': self.token_cookie_string,
        }
        # eid = json.loads(self.token_cookie['unionwsws'])['devicefinger']
        eid = 'eidA115c812269sbwhdP0BiVTnWYIKVNymrSBMIXUUi5txupHPRalrjqhmB/P3C0Hg3eO0405ppb4QzevFJmNvw/PFslM/68LPvtaaTT/MCFQOsNUQhL'
        query_params = {
            'functionId': self.function_id,
            'clientVersion': '9.2.0',
            'build': '85134',
            'client': 'android',
            'd_brand': 'HUAWEI',
            'd_model': 'LIO-AN00',
            'osVersion': '7.1.2',
            'screen': '1920*1080',
            'partner': 'hhqj02',
            'aid': '38af3fc36a99f737',
            'eid': eid,
            'sdkVersion': '25',
            'lang': 'zh_CN',
            'uuid': self.uuid,
            'area': '2_2830_51811_0',
            'networkType': 'wifi',
            'wifiBssid': '43236c80b42dbe2ba38bd9ab1ae41eb7',
            'uts': '0f31TVRjBSsqndu4/jgUPz6uymy50MQJhQy4jAtAlh+n8GJiXoWP/9c8wP/+u4Xkbsf8iPUHrJ+nz8nXt+aGZXiPhZV6YXoLgZtI5OBNQe5SJGxU/1t661/3OQSsQaU0dG+4NuQHNRoIZo4dG3JxhCAuLrGelkGqZ7vmHNN/jFolcDLqtEBSFY7Fou5xPR7en5iaWp6tQJpCvsAaneoaYw=='
        }
        token_key_url = 'https://api.m.jd.com/client.action?' + parse.urlencode(query_params) + '&'

        data = {'body': self.body_string}
        sign = 'st=1623726412643&sign=7463444f738401ce457f181d2f466723&sv=120'
        response = self.s.post(url=token_key_url + sign, data=data, headers=headers, timeout=1)
        # token_key = response.json()['tokenKey']
        # print('Token Key: ----------> %s' % response.json())
        # print(response.status_code)
        return response.json()

    # def update_sign(self):
    #     sign = gs.get_sign(self.function_id, self.body_string, self.uuid)
    #     print(sign)
    #     return sign

    def get_appjmp(self, token_params):
        headers = {
            'user-agent': 'jdapp;android;9.2.0;6.0.1;008796748981618-080027192572;network/wifi;model/MuMu;addressid/0;aid/aaaa97d5260b287a;oaid/;osVer/23;appBuild/85134;partner/hhqj02;jdSupportDarkMode/0;Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36'
        }
        appjmp_url = token_params['url']
        params = {
            'to': 'https://divide.jd.com/user_routing?skuId=%s' % self.skuId,
            'tokenKey': token_params['tokenKey'],
            'lbs': '{"lat":"39.904585","lng":"116.407018","provinceId":"1","cityId":"2802","districtId":"54741","provinceName":"北京","cityName":"东城区","districtName":"东华门街道"}'
        }

        response = self.s.get(url=appjmp_url, params=params, allow_redirects=False, headers=headers)
        # print('Get Appjmp跳转链接-------------->%s' % response.headers['Location'])
        return response.headers['Location']

    def get_divide(self, divide_url):
        headers = {
            'user-agent': 'jdapp;android;9.2.0;6.0.1;008796748981618-080027192572;network/wifi;model/MuMu;addressid/0;aid/aaaa97d5260b287a;oaid/;osVer/23;appBuild/85134;partner/hhqj02;jdSupportDarkMode/0;Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36'
        }
        response = self.s.get(url=divide_url, allow_redirects=False, headers=headers)
        print('Get Divide跳转链接-------------->%s' % response.headers['Location'])
        return response.headers['Location']

    def get_captcha(self, captcha_url):
        headers = {
            'user-agent': 'jdapp;android;9.2.0;6.0.1;008796748981618-080027192572;network/wifi;model/MuMu;addressid/0;aid/aaaa97d5260b287a;oaid/;osVer/23;appBuild/85134;partner/hhqj02;jdSupportDarkMode/0;Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36'
        }
        response = self.s.get(url=captcha_url, allow_redirects=False, headers=headers)
        print('Get Captcha跳转链接-------------->%s' % response.headers['Location'])
        return response.headers['Location']

    def get_seckill(self, seckill_url):
        headers = {
            'user-agent': 'jdapp;android;9.2.0;6.0.1;008796748981618-080027192572;network/wifi;model/MuMu;addressid/0;aid/aaaa97d5260b287a;oaid/;osVer/23;appBuild/85134;partner/hhqj02;jdSupportDarkMode/0;Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36'
        }
        response = self.s.get(url=seckill_url, allow_redirects=False, headers=headers)

    def init_action(self):
        headers = {
            'user-agent': 'jdapp;android;9.2.0;6.0.1;008796748981618-080027192572;network/wifi;model/MuMu;addressid/0;aid/aaaa97d5260b287a;oaid/;osVer/23;appBuild/85134;partner/hhqj02;jdSupportDarkMode/0;Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36'
        }
        init_action_url = 'https://marathon.jd.com/seckillnew/orderService/init.action'
        data = {
            'sku': self.skuId,
            'num': '1',
            'isModifyAddress': False,
        }
        response = self.s.post(url=init_action_url, data=data, headers=headers)
        print('init action返回数据：%s' % response.text)
        return response.json()

    def get_tak(self):
        headers = {
            'user-agent': 'jdapp;android;9.2.0;6.0.1;008796748981618-080027192572;network/wifi;model/MuMu;addressid/0;aid/aaaa97d5260b287a;oaid/;osVer/23;appBuild/85134;partner/hhqj02;jdSupportDarkMode/0;Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36'
        }
        tak_url = 'https://tak.jd.com/t/41CD2?_t=%d' % (int(round(time.time() * 1000)))
        response = self.s.get(url=tak_url, headers=headers)
        sk_val = get_sk(data=response.json())
        return sk_val

    def submit_order(self, order_data, sk):
        headers = {
            'user-agent': 'jdapp;android;9.2.0;6.0.1;008796748981618-080027192572;network/wifi;model/MuMu;addressid/0;aid/aaaa97d5260b287a;oaid/;osVer/23;appBuild/85134;partner/hhqj02;jdSupportDarkMode/0;Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36'
        }
        submit_order_url = 'https://marathon.jd.com/seckillnew/orderService/submitOrder.action?skuId=%s' % self.skuId
        address_info = order_data['addressList'][0]
        invoice_info = order_data['invoiceInfo']
        data = {
            'num': order_data['seckillSkuVO']['num'],
            'addressId': address_info['id'],
            'yuShou': True,
            'isModifyAddress': False,
            'name': address_info['name'],
            'provinceId': address_info['provinceId'],
            'provinceName': address_info['provinceName'],
            'cityId': address_info['cityId'],
            'cityName': address_info['cityName'],
            'countyId': address_info['countyId'],
            'countyName': address_info['countyName'],
            'townId': address_info['townId'],
            'townName': address_info['townName'],
            'addressDetail': address_info['addressDetail'],
            'mobile': address_info['mobile'],
            'mobileKey': address_info['mobileKey'],
            'email': '',
            'invoiceTitle': invoice_info['invoiceTitle'],
            'invoiceContent': invoice_info['invoiceContentType'],
            'invoicePhone': invoice_info['invoicePhone'],
            'invoicePhoneKey': invoice_info['invoicePhoneKey'],
            'invoice': True,
            'codTimeType': '3',
            'paymentType': '4',
            'overseas': '0',
            'token': order_data['token'],
            'sk': sk,
        }

        # print('submit提交数据： %s' % data)

        response = self.s.post(url=submit_order_url, data=data, headers=headers)
        try:
            submit_result = response.json()
            print('submit order返回数据：状态：%s，信息：%s' % (submit_result['success'], submit_result))
        except:
            print('submit order返回数据-非json格式：%s' % response.content)

        # return response

        