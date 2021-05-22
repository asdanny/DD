# DD
京东App 茅台

使用说明：
jdseckilAPI：
1. login_cookie，填入你自己的cookie。
2. reserve_maotai(self)，get_token_key(self)，get_token_key_by_fix_sign(self)请根据抓包的数据修改相应eid、uts与uuid参数。这些参数只要修改一次就行，保险起见先抓包一次，把你自己的数据带进去。
3 非抢购期间调试程序：get_seckill()里的flag取False，先运行一遍，看是否会报错。

