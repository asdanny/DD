import requests
import re
import datetime
from urllib import parse
import JniSign
import time


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
        sk_val = o[5:8] + re.sub('a', 'c', p, flags=re.IGNORECASE)
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
        self.aid = ''
        self.eid = ''
        self.uuid = ''
        self.uts = ''
        self.wifiBssid = ''
        self.user_agent = ''

    def reserve_maotai(self):
        headers = {
            'user-agent': 'okhttp/3.12.',
            'content-type': 'application/x-www-form-urlencoded',
            'content-length': '3081',
            'cookie': self.token_cookie_string,
            'jdc-backup': self.token_cookie_string,
        }
        query_params = {
            'functionId': 'appoint',
            'clientVersion': '9.3.4',
            'build': '85134',
            'client': 'android',
            'd_brand': 'HUAWEI',
            'd_model': 'LIO-AN00',
            'osVersion': '7.1.2',
            'screen': '1920*1080',
            'partner': 'hhqj02',
            'aid': self.aid,
            'eid': self.eid,
            'sdkVersion': '25',
            'lang': 'zh_CN',
            'uuid': self.uuid,
            'area': '15_1213_3411_59341',
            'networkType': 'wifi',
            'wifiBssid': self.wifiBssid,
            'uts': self.uts
        }
        reserve_url = 'https://api.m.jd.com/client.action?' + parse.urlencode(query_params) + '&'
        body_string = '{"autoAddCart":"0","bsid":"","check":"0","ctext":"","isShowCode":"0","mad":"0","skuId":"100012043978","type":"1"}'
        data = {'body': body_string}

        plainTextDic = {
            'functionId': query_params['functionId'],
            'clientVersion': query_params['clientVersion'],
            'client': query_params['client'],
            'uuid': query_params['uuid'],
            'body': body_string,
            'st': int(round(time.time() * 1000)),
        }
        sign = JniSign.JDencrypt_version0(plainTextDic=plainTextDic, ran1=2)
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
        body_string = '{"action":"to","to":"https%3A%2F%2Fdivide.jd.com%2Fuser_routing%3FskuId%3D100012043978"}'
        query_params = {
            'functionId': 'genToken',
            'clientVersion': '9.2.0',
            'build': '85134',
            'client': 'android',
            'd_brand': 'HUAWEI',
            'd_model': 'LIO-AN00',
            'osVersion': '7.1.2',
            'screen': '1920*1080',
            'partner': 'hhqj02',
            'aid': self.aid,
            'eid': self.eid,
            'sdkVersion': '25',
            'lang': 'zh_CN',
            'uuid': self.uuid,
            'area': '15_1213_3411_59341',
            'networkType': 'wifi',
            'wifiBssid': self.wifiBssid,
            'uts': self.uts
        }
        token_key_url = 'https://api.m.jd.com/client.action?' + parse.urlencode(query_params) + '&'
        data = {'body': body_string}

        plainTextDic = {
            'functionId': query_params['functionId'],
            'clientVersion': query_params['clientVersion'],
            'client': query_params['client'],
            'uuid': query_params['uuid'],
            'body': data['body'],
            'st': int(round(time.time() * 1000)),
        }
        sign = JniSign.JDencrypt_version0(plainTextDic=plainTextDic, ran1=2)
        response = self.s.post(url=token_key_url + sign, data=data, headers=headers, timeout=1)
        # token_key = response.json()['tokenKey']
        # print('Token Key: ----------> %s' % response.json())
        # print(response.status_code)
        return response.json()

    def get_appjmp(self, token_params):
        headers = {
            'user-agent': self.user_agent
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
            'user-agent': self.user_agent
        }
        response = self.s.get(url=divide_url, allow_redirects=False, headers=headers)
        print('Get Divide跳转链接-------------->%s' % response.headers['Location'])
        return response.headers['Location']

    def get_captcha(self, captcha_url):
        headers = {
            'user-agent': self.user_agent
        }
        response = self.s.get(url=captcha_url, allow_redirects=False, headers=headers)
        print('Get Captcha跳转链接-------------->%s' % response.headers['Location'])
        return response.headers['Location']

    def get_seckill(self, seckill_url):
        headers = {
            'user-agent': self.user_agent
        }
        response = self.s.get(url=seckill_url, allow_redirects=False, headers=headers)

    def init_action(self, num=1):
        headers = {
            'user-agent': self.user_agent
        }
        init_action_url = 'https://marathon.jd.com/seckillnew/orderService/init.action'
        data = {
            'sku': self.skuId,
            'num': num,
            'isModifyAddress': False,
        }
        response = self.s.post(url=init_action_url, data=data, headers=headers)
        print('init action返回数据：%s' % response.text)
        return response.json()

    def get_tak(self):
        headers = {
            'user-agent': self.user_agent
        }
        tak_url = 'https://tak.jd.com/t/41CD2?_t=%d' % (int(round(time.time() * 1000)))
        response = self.s.get(url=tak_url, headers=headers)
        sk_val = get_sk(data=response.json())
        return sk_val

    def submit_order(self, order_data, sk):
        headers = {
            'user-agent': self.user_agent
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
            print('%s submit order返回数据：状态：%s，信息：%s' % (str(datetime.datetime.now()),
                                                       submit_result['success'], submit_result))

        except:
            print('%s submit order返回数据-非json格式：%s' % (str(datetime.datetime.now()), response.content))

        # return response


if __name__ == '__main__':
    login_cookie_186 = {
        'pin': '',
        'wskey': '',
        'whwswswws': '',
        'unionwsws': ''
    }

    JDska = JDSecKillAPI(login_cookie=login_cookie_186)
    print(JDska.reserve_maotai())
    token_params = JDska.get_token_key()
    divide_url = JDska.get_appjmp(token_params=token_params)
    captcha_url = JDska.get_divide(divide_url=divide_url)
    seckill_url = JDska.get_captcha(captcha_url=captcha_url)
    JDska.get_seckill(seckill_url=seckill_url)
    order_data = JDska.init_action()
    sk_val = JDska.get_tak()
    print('python计算sk参数：%s' % sk_val)
    JDska.submit_order(order_data=order_data, sk=sk_val)
    # print(JDska.s.cookies)
    # get_jd_time()
