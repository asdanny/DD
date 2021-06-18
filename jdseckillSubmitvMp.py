from jdseckillAPIv1 import JDSecKillAPI
import datetime
from multiprocessing import Process
import time


class JDSecKillSubmit(JDSecKillAPI):
    def __init__(self, login_cookie):
        super().__init__(login_cookie=login_cookie)
        self.log_text = []

    def submit_task(self, submit_time, flag):
        """
        sign签名固定提供、多进程提交
        最后一步submit多次提交
        """
        start_time = datetime.datetime.strptime(
            str(datetime.datetime.now().date()) + submit_time, '%Y-%m-%d%H:%M:%S.%f')

        now_time = datetime.datetime.now()
        while True:
            if now_time >= start_time:
                break
            now_time = datetime.datetime.now()

        while True:
            token_params = self.get_token_key_by_fix_sign()
            try:
                divide_url = self.get_appjmp(token_params=token_params)
                captcha_url = self.get_divide(divide_url=divide_url)
                seckill_url = self.get_captcha(captcha_url=captcha_url)
            except Exception as e:
                print('error----> %s' % str(e))
                continue

            if 'skuId=' in seckill_url:  # 判断是否能够跳转到填写订单的页面
                print('%s: 跳转填写订单页面成功' % str(datetime.datetime.now()))
                break
            else:
                print('%s: fucking..........' % str(datetime.datetime.now()))
            if not flag:  # 调试用，抢购时flag必须为True
                break
        self.get_seckill(seckill_url=seckill_url)
        order_data = self.init_action()

        num = 50 if flag else 1
        for submit_time in range(num):
            try:
                print('第%d次提交结果：' % submit_time)
                # 2021.6.14 更新sk参数
                sk_val = self.get_tak()
                # print('python计算sk参数：%s' % sk_val)
                self.submit_order(order_data=order_data, sk=sk_val)
                time.sleep(0.15)
            except Exception as e:
                print('%s' % str(e))


if __name__ == '__main__':
    login_cookie_1 = {
        'pin': '',
        'wskey': '',
        'whwswswws': '',
        'unionwsws': ''
    }

    process_num = 1
    hour = '11'
    submit_times = ['%s:59:59.0' % hour] * process_num
    flag = True  # 调试用，抢购时flag必须为True
    p = []
    for i in range(process_num):
        JDsks = JDSecKillSubmit(login_cookie=login_cookie_1)
        p1 = Process(target=JDsks.submit_task, args=(submit_times[i], flag))
        p1.start()
        p.append(p1)

    for i in range(process_num):
        p[i].join()
