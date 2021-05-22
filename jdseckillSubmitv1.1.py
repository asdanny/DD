import copy
from jdseckillAPI import JDSecKillAPI
import datetime
from threading import Thread


class JDSecKillSubmit(JDSecKillAPI):
    def __init__(self, login_cookie):
        super().__init__(login_cookie=login_cookie)
        self.log_text = []

    def submit_task(self, submit_time, flag):
        """
        sign签名由frida提供、多线程提交
        """
        start_time = datetime.datetime.strptime(
            str(datetime.datetime.now().date()) + submit_time, '%Y-%m-%d%H:%M:%S.%f')

        now_time = datetime.datetime.now()
        while True:
            if now_time >= start_time:
                break
            now_time = datetime.datetime.now()
            # print('未到抢购时间，请耐心等待')

        while True:
            token_params = self.get_token_key()
            try:
                divide_url, appjmp_set_cookie = self.get_appjmp(token_params=token_params)
                captcha_url = self.get_divide(divide_url=divide_url, cookie=appjmp_set_cookie)
                seckill_url, captcha_set_cookie = self.get_captcha(captcha_url=captcha_url, cookie=appjmp_set_cookie)
            except Exception as e:
                print('error----> %s' % str(e))
                continue

            if 'mobile/koFail.html' in seckill_url:  # 判断是否能够跳转到填写订单的页面
                print('填写订单的页面尚未打开，正在重新提交--------->')
                if not flag:
                    break
            else:
                break

        seckill_cookie = dict(appjmp_set_cookie, **captcha_set_cookie)
        # print('seckill_cookie: %s' % seckill_cookie)
        # print('init_action_cookie: %s' % init_action_cookie)
        # print('submit_order_cookie: %s' % submit_order_cookie)

        seckill_val = self.get_seckill(seckill_url=seckill_url, cookie=seckill_cookie, flag=flag)

        init_action_cookie = copy.deepcopy(seckill_cookie)
        init_action_cookie['seckill100012043978'] = seckill_val['seckill100012043978']
        order_data = self.init_action(cookie=init_action_cookie)

        submit_order_cookie = copy.deepcopy(init_action_cookie)
        submit_order_cookie['unpl'] = ''
        self.submit_order(order_data=order_data, cookie=submit_order_cookie)

        self.log_text.append([seckill_cookie, init_action_cookie, submit_order_cookie])
        self.log_text.append([order_data])
        print(self.log_text)  # 输出日志


if __name__ == '__main__':
    login_cookie = {
        'pin': '',
        'wskey': '',
        'whwswswws': '',
        'unionwsws': ''
    }
    thread_num = 2
    hour = '01'
    submit_times = ['%s:59:50.0' % hour] * thread_num
    flag = False
    for i in range(thread_num):
        JDsks = JDSecKillSubmit(login_cookie=login_cookie)
        thread1 = Thread(target=JDsks.submit_task, args=(submit_times[i], flag))
        thread1.start()
