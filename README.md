# DD

必备工具：模拟器MuMu或者夜神，安装frida-server，详细教程在吾爱破解里面我提供了思路。
https://www.52pojie.cn/thread-1444614-1-1.html


京东App 茅台

使用说明：
1. login_cookie，填入你自己的cookie。
2. reserve_maotai(self)，get_token_key(self)，get_token_key_by_fix_sign(self)请根据抓包的数据修改相应eid、uts与uuid参数。这些参数只要修改一次就行，保险起见先抓包一次，把你自己的数据带进去。
3. 如果安装好模拟器，且成功安装frida-server，建议使用get_token_key(self)获取tokenKey。如果条件不允许，请使用抓包软件获取sign签名，用get_token_key_by_fix_sign(self)来获取tokenKey。脚本中默认使用的方法是get_token_key(self)。
4. 非抢购期间调试程序：get_seckill()里的flag取False，先运行一遍，看是否会报错。
5. jdseckillSubmitv1.11（多进程）和jdseckillSubmitv1.1（多线程）为两类抢购脚本。 (a): 多进程脚本可以不依赖于frida-server和模拟器，但需要用charles抓到sign签名。(b): 多线程脚本依赖于frida-server和模拟器，sign签名有文件jd_frida.py生成。
6. 在jdseckilAPI这个文件调试通过后，jdseckillSubmitv1.11与jdseckillSubmitv1.1可以直接使用


7. 祝各位茅台多多，财源滚滚。有技术问题的可以加我的微信sy742727,一起交流下共同进步哦！
8. 如果抢到了的话，告知一下呗
