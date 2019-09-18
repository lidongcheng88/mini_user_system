import random

from pexpect.popen_spawn import PopenSpawn
from faker import Faker

from mini_system import Backend


class Simulate:
    def __init__(self, times=5):
        # 执行进程
        self.process = PopenSpawn('cmd', timeout=10)
        # 日志
        self.logFile = open("logfile.txt", 'wb')
        self.process.logfile = self.logFile
        # 功能序列
        self.d = self.reverse_dict()
        self.seq = ('login', 'register')
        # 测试次数
        self.times = times
        # self.choice = Backend.CHOICE

    # 功能与对应输入字符的映射（反转后台类对象字典）
    @staticmethod
    def reverse_dict():
        d = Backend.func_dict
        return dict(zip(d.values(), d.keys()))

    def common(self, choice):
        # 等待特定字符出现
        self.process.expect_exact("请输入您想使用的功能")
        # 命令行输入
        self.process.send(f'{choice}\n')

        self.process.expect_exact("请输入用户名")
        # 使用 faker 制造测试数据
        fake = Faker('zh_CN')
        self.process.send(fake.phone_number() + '\n')

        self.process.expect_exact("请输入密码")
        self.process.send(fake.password(length=random.randint(6, 16)) + '\n')

    # 模拟登录
    def login(self):
        self.common(self.d['login'])

    def register(self):
        self.common(self.d['register'])

    def exit(self):
        self.process.expect_exact("请输入您想使用的功能")
        self.process.send('q\n')
        # 不忘文件关闭
        self.logFile.close()

    def run(self):
        # 执行 homework, 开始测试
        self.process.sendline('python mini_system.py')
        # 输入 1 使用登录功能；输入 2 使用注册功能；输入 q 退出程序
        # File "K:\Anaconda\lib\site-packages\pexpect\spawnbase.py", line 138, in _coerce_expect_string
        #     return s.encode('ascii')
        for i in range(5):
            # 执行注册或登录测试
            exec(f'self.{random.choice(self.seq)}()')
        self.exit()


if __name__ == '__main__':
    moni = Simulate()
    moni.run()
