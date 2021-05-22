import requests
import json
import re
import datetime
import time
from urllib import parse
import base64
import urllib
import json
import jd_frida as gs
import copy


def getUrlParams(url):
    res = dict(parse.parse_qsl(url))
    return res


def get_cookie(response):
    cookiejar = response.cookies
    cookiedict = requests.utils.dict_from_cookiejar(cookiejar)
    print(cookiejar)
    print(cookiedict)


def get_cookie_string(cookie):
    cookie_string = ''
    for cookie_key in cookie.keys():
        cookie_string += '%s=%s;' % (cookie_key, cookie[cookie_key])
    return cookie_string


class JDSecKillAPI:
    def __init__(self, login_cookie):
        self.skuId = '100012043978'
        self.s = requests.session()
        self.token_cookie = login_cookie
        self.token_cookie_string = get_cookie_string(cookie=self.token_cookie)

        self.function_id = 'genToken'
        self.uuid = '863064425269521-080027d76df4'
        self.body_string = '{"action":"to","to":"https%3A%2F%2Fdivide.jd.com%2Fuser_routing%3FskuId%3D100012043978"}'

    def reserve_maotai(self):
        headers = {
            'user-agent': 'okhttp/3.12.',
            'content-type': 'application/x-www-form-urlencoded',
            'content-length': '3081',
            'cookie': self.token_cookie_string,
            'jdc-backup': self.token_cookie_string,
        }
        # eid = json.loads(self.token_cookie['unionwsws'])['devicefinger']
        eid = ''
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
            'uts': '',
        }

        reserve_url = 'https://api.m.jd.com/client.action?' + parse.urlencode(query_params) + '&'
        body_string = '{"autoAddCart":"0","bsid":"","check":"0","ctext":"","isShowCode":"0","mad":"0","skuId":"100012043978","type":"1"}'

        data = {'body': body_string}
        sign = gs.get_sign('appoint', body_string, self.uuid)
        response = self.s.post(url=reserve_url + sign, data=data, headers=headers, timeout=1)
        return response.json()

    def get_token_key(self):
        headers = {
            'user-agent': 'okhttp/3.12.',
            'content-type': 'application/x-www-form-urlencoded',
            'content-length': '3081',
            'cookie': self.token_cookie_string,
            'jdc-backup': self.token_cookie_string,
        }
        # eid = json.loads(self.token_cookie['unionwsws'])['devicefinger']
        eid = ''
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
            'uts': ''
        }
        token_key_url = 'https://api.m.jd.com/client.action?' + parse.urlencode(query_params) + '&'

        data = {'body': self.body_string}
        sign = gs.get_sign(self.function_id, self.body_string, self.uuid)
        response = self.s.post(url=token_key_url + sign, data=data, headers=headers, timeout=1)
        # token_key = response.json()['tokenKey']
        # print('Token Key: ----------> %s' % response.json())
        # print(response.status_code)
        return response.json()

    def get_token_key_by_fix_sign(self):
        headers = {
            'user-agent': 'okhttp/3.12.',
            'content-type': 'application/x-www-form-urlencoded',
            'content-length': '3081',
            'cookie': self.token_cookie_string,
            'jdc-backup': self.token_cookie_string,
        }
        # eid = json.loads(self.token_cookie['unionwsws'])['devicefinger']
        eid = ''
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
            'uts': ''
        }
        token_key_url = 'https://api.m.jd.com/client.action?' + parse.urlencode(query_params) + '&'

        data = {'body': self.body_string}
        sign = 'st=1621562420817&sign=562bf2988bb077beacf6a8551af6490d&sv=101'
        response = self.s.post(url=token_key_url + sign, data=data, headers=headers, timeout=1)
        # token_key = response.json()['tokenKey']
        # print('Token Key: ----------> %s' % response.json())
        # print(response.status_code)
        return response.json()

    def update_sign(self):
        sign = gs.get_sign(self.function_id, self.body_string, self.uuid)
        print(sign)
        return sign

    def get_appjmp(self, token_params):
        # headers = {
        #     'cookie': self.login_cookie_string
        # }
        appjmp_url = token_params['url']
        params = {
            'to': 'https://divide.jd.com/user_routing?skuId=%s' % self.skuId,
            'tokenKey': token_params['tokenKey'],
            'lbs': '{"lat":"39.904585","lng":"116.407018","provinceId":"1","cityId":"2802","districtId":"54741","provinceName":"北京","cityName":"东城区","districtName":"东华门街道"}'
        }

        response = self.s.get(url=appjmp_url, params=params, allow_redirects=False)
        # print('Get Appjmp跳转链接-------------->%s' % response.headers['Location'])

        cookie_items = response.headers['set-cookie']
        pt_key = re.findall(r'pt_key=(.*?);', cookie_items)[0]
        pt_pin = re.findall(r'pt_pin=(.*?);', cookie_items)[0]
        pwdt_id = re.findall(r'pwdt_id=(.*?);', cookie_items)[0]
        sid = re.findall(r'sid=(.*?);', cookie_items)[0]
        appjmp_set_cookie = {
            'pt_key': pt_key,
            'pt_pin': pt_pin,
            'pwdt_id': pwdt_id,
            'sid': sid,
        }
        # print('Get Appjmp响应头Set Cookie-------------->%s' % appjmp_set_cookie)

        return response.headers['Location'], appjmp_set_cookie

    def get_divide(self, divide_url, cookie):
        headers = {
            'cookie': get_cookie_string(cookie)
        }
        response = self.s.get(url=divide_url, allow_redirects=False, headers=headers)
        print('Get Divide跳转链接-------------->%s' % response.headers['Location'])
        # print('Get Divide响应头Set Cookie-------------->%s' % response.headers['set-cookie'])
        return response.headers['Location']

    def get_captcha(self, captcha_url, cookie):
        headers = {
            'cookie': get_cookie_string(cookie)
        }
        response = self.s.get(url=captcha_url, allow_redirects=False, headers=headers)
        print('Get Captcha跳转链接-------------->%s' % response.headers['Location'])
        cookie_items = response.headers['set-cookie']

        mid = re.findall(r'mid=(.*?);', cookie_items)
        seckill100012043978 = re.findall(r'seckill100012043978=(.*?);', cookie_items)

        captcha_set_cookie = {
            'seckillSku': str(self.skuId),
            'seckillSid': '',
            'mid': mid[-1],
            'seckill100012043978': seckill100012043978[-1],
        }
        # print('Get Captcha响应头Set Cookie-------------->%s' % captcha_set_cookie)
        return response.headers['Location'], captcha_set_cookie
        # get_cookie(response)
        # print(response.status_code)

    def get_seckill(self, seckill_url, cookie, flag=True):
        headers = {
            'cookie': get_cookie_string(cookie)
        }
        response = self.s.get(url=seckill_url, allow_redirects=False, headers=headers)
        status_code = response.status_code

        if flag:
            cookie_items = response.headers['set-cookie']
        else:
            cookie_items = 'set-cookie: seckillSku=100012043978;domain=marathon.jd.com;path=/;expires=Fri, 02-Apr-21 04:02:02 GMTset-cookie: seckillSid=;domain=marathon.jd.com;path=/;expires=Fri, 02-Apr-21 04:02:02 GMTset-cookie: seckillSku=100012043978;domain=marathon.jd.com;path=/;expires=Fri, 02-Apr-21 04:02:02 GMTset-cookie: seckillSid=;domain=marathon.jd.com;path=/;expires=Fri, 02-Apr-21 04:02:02 GMTset-cookie: seckill100012043978=14powaYjMkEW1eoI2ADsF9FQ/js5c/TutngVU0lPrQ3I54v6TinvNdnB16xBLLVfxNLWbND6HW94h+KUFehtnITxUKFRtnF9iO0VizmcVXNV5Id7V0n74BcLhNdETZHo+T4tLLsdCdqKszhZJtZljuwSEFXSwHEpFt9En7THied57EyKyD7sYiJF12bCC7I7nsWClE936zLlVdb7;domain=marathon.jd.com;path=/;expires=Fri, 02-Apr-21 04:05:02 GMTcontent-language: zh-CN'
            status_code = 302
        seckill100012043978 = re.findall(r'seckill100012043978=(.*?);', cookie_items)
        seckill_set_cookie = {
            'seckill100012043978': seckill100012043978[-1],
        }
        # print('Get seckill响应头Set Cookie-------------->%s' % seckill_set_cookie)
        # print(response.text)
        return seckill_set_cookie

    def init_action(self, cookie):
        init_action_url = 'https://marathon.jd.com/seckillnew/orderService/init.action'
        data = {
            'sku': self.skuId,
            'num': '2',
            'isModifyAddress': False,
        }
        headers = {
            'cookie': get_cookie_string(cookie)
        }
        response = self.s.post(url=init_action_url, data=data, headers=headers)
        print('init action返回数据：%s' % response.text)
        return response.json()

    def submit_order(self, order_data, cookie):
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
            'email': address_info['email'],
            'invoiceTitle': invoice_info['invoiceTitle'],
            'invoiceContent': invoice_info['invoiceContentType'],
            'invoicePhone': invoice_info['invoicePhone'],
            'invoicePhoneKey': invoice_info['invoicePhoneKey'],
            'invoice': True,
            'codTimeType': '3',
            'paymentType': '4',
            'overseas': '0',
            'token': order_data['token'],
            'sk': 'tpr26spd5lzprMfHEtX',  # 没有也没关系
        }
        # print('submit order提交数据：%s' % data)
        headers = {
            'cookie': get_cookie_string(cookie)
        }

        response = self.s.post(url=submit_order_url, data=data, headers=headers)
        print('submit order返回数据：%s' % response.text)
        # return response


if __name__ == '__main__':
    login_cookie = {
        'pin': '',
        'wskey': '',
        'whwswswws': '',
        'unionwsws': ''
    }

    JDska = JDSecKillAPI(login_cookie=login_cookie)

    token_params = JDska.get_token_key()
    # token_params = JDska.get_token_key_by_fix_sign()
    divide_url, appjmp_set_cookie = JDska.get_appjmp(token_params=token_params)
    captcha_url = JDska.get_divide(divide_url=divide_url, cookie=appjmp_set_cookie)
    seckill_url, captcha_set_cookie = JDska.get_captcha(captcha_url=captcha_url, cookie=appjmp_set_cookie)

    seckill_cookie = dict(appjmp_set_cookie, **captcha_set_cookie)
    print('seckill_cookie: %s' % seckill_cookie)

    # seckill_url = 'https://marathon.jd.com/seckillM/seckill.action?skuId=100012043978&num=1&rid=1621396801'
    seckill_val = JDska.get_seckill(seckill_url=seckill_url, cookie=seckill_cookie, flag=False)  # 返回seckill+id的cooki，flag调试标志，抢购期间改为True
    init_action_cookie = copy.deepcopy(seckill_cookie)
    init_action_cookie['seckill100012043978'] = seckill_val['seckill100012043978']
    print('init_action_cookie: %s' % init_action_cookie)
    order_data = JDska.init_action(cookie=init_action_cookie)

    submit_order_cookie = copy.deepcopy(init_action_cookie)
    submit_order_cookie['unpl'] = ''
    print('submit_order_cookie: %s' % submit_order_cookie)
    JDska.submit_order(order_data=order_data, cookie=submit_order_cookie)
