from pgzrun import *
class Zk:
    def __init__(self):
        pass
    def 清空():
        screen.clear()
    def 填充(c):
        screen.fill(c)
    
屏幕 = Zk()

class 角色:
    def __init__(self,i,c=(0,0)):
        self.s = Actor(i,center=c)
    def 移动(self,x,y):
        self.s.pos(x,y)
    def 距离(self,x,y):
        return self.s.distance_to((x,y))
    def 删除自己(self):
        self.s.remove()
    def 绘制自己(self):
        self.s.draw()
    def 碰到了(self,a):
        return self.s.collideactor(a)

def 运行():
    pgzrun.go()

宽 = 600
高 = 800
WIDTH = 宽
HEIGHT = 高
标题 = 'rabbit game'
TITLE = 标题