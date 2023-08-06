import random
import math
from turtle import *
try:
    from pgzrun import *
except Exception:
    pass
import time
def ascii编码(text: str):
    code = []
    for txt in text:
        code.append(bin(ord(txt)))
    return code


def ascii解码(code: list):
    text = ''
    for cd in code:
        text += chr(int(cd, 2))
    return text


def 添加(o, v):
    o.append(v)


def 插入(o, n, v):
    o.insert(n, v)


def 索引(o, v):
    return o.index(0)


def fun():
    pass


def 空代码():
    pass


def 导入(名称):
    mod = __import__(名称)
    exec(名称 + ' = mod')


def 当(条件, 代码):
    while 条件:
        代码()


def 遍历(变量, 对象, 代码):
    exec('for '+变量+' in '+对象+':\n'+代码)


def 如果(条件, 成立代码, 不成立代码=空代码):
    if 条件:
        成立代码()
    else:
        不成立代码()


def 返回(zhi):
    exec('return '+str(zhi))


序列 = range


def 函数(参数, 代码):
    global fun
    exec('def fun(' + 参数 + '):\n  ' + 代码)
    return fun


def 类(canshu, daima):
    global fun
    exec('class fun:\n  def __init__(self,' + canshu + '):\n        ' + daima)


def 删除(duixiang):
    del duixiang


长度 = len


def 存在于(a, b):
    return a in b


执行代码 = exec
表达式 = eval
时间 = time.gmtime
等待 = time.sleep


def 对象赋值(o, v, c):
    exec('with o as v:\nc()')


时间格式化 = time.strftime


def 开启或归零计时器():
    start = time.perf_counter()


计时器 = time.perf_counter()
字符串 = str
编码 = ord
解码 = chr


def 小写(string):
    return string.lower()


def 大写(string):
    return string.upper()


def 首字母大写(string):
    return string.title()


def 分开成列表(string, fen=None, ci=1):
    return string.split(fen, ci)


def 连接字符串(lian, List):
    return lian.join(List)

try:
    class Zk:
        def __init__(self):
            pass

        def 清空():
            screen.clear()

        def 填充(c):
            screen.fill(c)


    屏幕 = Zk()


    class 角色:
        def __init__(self, i, c=(0, 0)):
            self.s = Actor(i, center=c)

        def 移动(self, x, y):
            self.s.pos(x, y)

        def 距离(self, x, y):
            return self.s.distance_to((x, y))

        def 删除自己(self):
            self.s.remove()

        def 绘制自己(self):
            self.s.draw()

        def 碰到了(self, a):
            return self.s.collideactor(a)


    def 运行():
        pgzrun.go()


    宽 = 600
    高 = 800
    WIDTH = 宽
    HEIGHT = 高
    标题 = 'rabbit game'
    TITLE = 标题
except Exception:
    pass

class Zd:
    def __init__(self):
        self.输出 = print
        self.输入 = input


终端 = Zd()


设置背景色 = bgcolor
获得字符串输入 = textinput
获得数字输入 = numinput
停止运行 = done
鼠标点击事件 = onclick
鼠标释放事件 = onrelease
移动鼠标事件 = ondrag
监听事件 = listen
设置 = setup
键盘按下 = onkeypress
键盘释放 = onkeyrelease


class 画笔:
    def __init__(self):
        self.pen = Pen()
        self.向前 = self.pen.forward
        self.向后 = self.pen.backward
        self.右转 = self.pen.right
        self.左转 = self.pen.left
        self.移到 = self.pen.goto
        self.设置x = self.pen.setx
        self.设置y = self.pen.sety
        self.画弧 = self.pen.circle
        self.画点 = self.pen.dot
        self.书写 = self.pen.write
        self.面向 = self.pen.setheading
        self.抬笔 = self.pen.penup
        self.落笔 = self.pen.pendown
        self.设置粗细 = self.pen.pensize
        self.设置速度 = self.pen.speed
        self.x坐标 = self.pen.xcor
        self.y坐标 = self.pen.ycor
        self.隐藏 = self.pen.hideturtle
        self.显示 = self.pen.showturtle
        self.清空 = self.pen.clear
        self.设置颜色 = self.pen.pencolor
        self.设置填充色 = self.pen.fillcolor
        self.设置填充起点 = self.pen.begin_fill
        self.设置填充终点 = self.pen.end_fill


π = (math.pi)
e = (math.e)
绝对值 = abs
四舍五入 = round


def 且(a, b):
    return a and b


def 或(a, b):
    return a or b


def 不成立(a):
    return not a


def 是(a, b):
    return a is b


def 随机整数(a, b):
    return random.randint(a, b)


def 随机浮点数(a, b):
    return random.uniform(a, b)