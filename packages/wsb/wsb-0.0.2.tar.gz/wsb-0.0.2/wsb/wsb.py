import random
def wsb(x):
    def z(s):
        import sys
        import time
        sys.stdout.write("")
        sys.stdout.flush()
        for u in s:
            sys.stdout.write(u)
            sys.stdout.flush()
            time.sleep(0.1)
        print("")
    z(x)
def games():
        import random
        bot = int(input('请设置数字的最小值（注意:请输入整数）\n'))
        top = int(input('请设置数字的最大值（注意:请输入整数）\n'))
        rand = random.randint(bot, top)
        print('随机数字生成范围' + str(bot) + '到' + str(top) + '设置成功!')
        num = int(input('开始\n'))
        cnt = 1
        while num != rand:
            if num < rand:
                print('比答案低！')
            else:
                print('比答案高！')
            num = int(input('继续\n'))
            cnt = cnt + 1
        print('恭喜你，猜对这个数字用了%d次！' % cnt)
def open(x):
    open(x)