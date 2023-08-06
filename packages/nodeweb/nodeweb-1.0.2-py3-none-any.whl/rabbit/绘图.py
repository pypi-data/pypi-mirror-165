from turtle import *


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