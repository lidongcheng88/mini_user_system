import re


# 用户类
class User:
    def __init__(self, name, pwd):
        self.name = name
        self.pwd = pwd
        # 三次密码尝试机会
        self.times = 3


# 后台类
class Backend:
    # 输入字符与对象函数映射
    func_dict = {
        '1': 'login',
        '2': 'register',
        'q': 'exit'
    }

    def __init__(self):
        self.user_list = []

    def create_user(self, name, pwd):
        new_user = User(name=name, pwd=pwd)
        self.user_list.append(new_user)

    def run(self):
        while True:
            print('\n\n输入 1 使用登录功能；输入 2 使用注册功能；输入 q 退出程序')
            func_choice = input('请输入您想使用的功能:')
            exec(f'self.{self.func_dict[func_choice]}()')

    def login(self):
        # 运行标识符
        flag = 0
        uname = input('请输入用户名：\n')
        upwd = input('请输入密码：\n')
        for user in self.user_list:
            if uname == user.name:
                while True:
                    if upwd == user.pwd:
                        print('登录成功')
                        # 重置试错机会
                        user.times = 3
                        flag = 1
                        break
                    else:
                        if user.times > 1:
                            user.times -= 1
                            print(f'密码错误，请重新输入\n\
                            （你还有 {3 - user.times} 次重新输入密码的机会，\
                            两次过后，只能重置密码')
                        else:
                            print('密码错误次数已达上限，系统自动为您转到找回密码界面...')
                            flag = 1
                            self.forgot_pwd()
            # 确保循环终止
            if flag == 1:
                return
        # 用户不存在时顺便帮其注册
        else:
            self.create_user(uname, upwd)
            print('注册成功')

    def register(self):
        # 打印提示信息
        print('为响应国家的实名号召，请输入手机号进行注册')
        uname = input('请输入用户名：\n')
        # TODO 校验用户名
        if not re.match(r"^1[35678]\d{9}$", uname):
            print('用户名格式错误')
            return
        for user in self.user_list:
            if uname == user.name:
                print('用户名已存在')
                break
        else:
            upwd = input('请输入密码：\n')
            # TODO 校验密码
            if not re.search("^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).*$", upwd) and len(upwd) >= 10:
                print('密码必须由大小写字母数字特殊字符组成')
                return
            self.create_user(uname, upwd)
            print('注册成功，已自动为您登录系统')

    def exit(self):
        exit()

    def forgot_pwd(self):
        pass

    def reset_pwd(self):
        pass


if __name__ == '__main__':
    backend = Backend()
    backend.run()
